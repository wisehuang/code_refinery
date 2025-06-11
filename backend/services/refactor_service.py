import logging
import time
from typing import List
from models import RefactorRequest, RefactorResponse, LLMResponse
from services.llm_service import LLMService

# Configure logging
logger = logging.getLogger(__name__)


class RefactorService:
    """Service for orchestrating code refactoring using multiple LLMs"""
    
    def __init__(self):
        self.llm_service = LLMService()
        logger.info("🏭 RefactorService initialized")
    
    def _extract_code_from_markdown(self, code: str) -> str:
        """Extract code from markdown code blocks if present"""
        lines = code.strip().split('\n')
        
        # Check if wrapped in markdown code blocks
        if len(lines) >= 2 and lines[0].startswith('```') and lines[-1] == '```':
            logger.debug("📝 Extracting code from markdown blocks")
            return '\n'.join(lines[1:-1])
        
        return code
    
    async def refactor_code(self, request: RefactorRequest) -> RefactorResponse:
        """Main method to refactor code using multiple LLMs and synthesis"""
        logger.info("🎯 Starting code refactoring process")
        logger.info(f"📄 Input: {len(request.code)} chars of {request.language} code")
        
        start_time = time.time()
        
        try:
            # Get refactored versions from all LLM providers concurrently
            logger.info("🚀 Calling all LLM providers...")
            llm_responses = await self.llm_service.get_all_refactors(
                request.code, 
                request.language
            )
            
            llm_end_time = time.time()
            llm_duration = round(llm_end_time - start_time, 2)
            logger.info(f"⏱️  LLM calls completed in {llm_duration}s")
            
            # Log response summary
            summary = self.get_llm_responses_summary(llm_responses)
            logger.info(f"📊 LLM Results: {summary['successful_responses']}/{summary['total_responses']} successful")
            
            # Check if we have at least one successful response
            successful_responses = [r for r in llm_responses if r.success and r.refactored_code.strip()]
            
            if not successful_responses:
                logger.error("❌ All LLM providers failed!")
                return RefactorResponse(
                    refactored_code=request.code,
                    language=request.language,
                    success=False,
                    error="All LLM providers failed to refactor the code"
                )
            
            # If only one successful response, return it directly
            if len(successful_responses) == 1:
                logger.info(f"✅ Single successful response from {successful_responses[0].provider}")
                refactored_code = self._extract_code_from_markdown(
                    successful_responses[0].refactored_code
                )
                
                end_time = time.time()
                total_duration = round(end_time - start_time, 2)
                logger.info(f"🎉 Refactoring completed successfully in {total_duration}s (single provider)")
                logger.info(f"📏 Final output: {len(refactored_code)} chars")
                
                return RefactorResponse(
                    refactored_code=refactored_code,
                    language=request.language,
                    success=True
                )
            
            # Synthesize multiple successful responses
            logger.info(f"🧪 Multiple successful responses ({len(successful_responses)}), starting synthesis...")
            synthesis_start = time.time()
            
            try:
                synthesized_code = await self.llm_service.synthesize_refactors(
                    successful_responses, 
                    request.language
                )
                
                synthesis_end = time.time()
                synthesis_duration = round(synthesis_end - synthesis_start, 2)
                
                final_code = self._extract_code_from_markdown(synthesized_code)
                
                end_time = time.time()
                total_duration = round(end_time - start_time, 2)
                
                logger.info(f"🎉 Refactoring with synthesis completed successfully!")
                logger.info(f"⏱️  Total duration: {total_duration}s (LLMs: {llm_duration}s + Synthesis: {synthesis_duration}s)")
                logger.info(f"📏 Final output: {len(final_code)} chars")
                
                return RefactorResponse(
                    refactored_code=final_code,
                    language=request.language,
                    success=True
                )
            
            except Exception as synthesis_error:
                logger.warning(f"⚠️  Synthesis failed: {str(synthesis_error)}")
                logger.info(f"🔄 Falling back to {successful_responses[0].provider} response")
                
                # Fallback to the first successful response if synthesis fails
                refactored_code = self._extract_code_from_markdown(
                    successful_responses[0].refactored_code
                )
                
                end_time = time.time()
                total_duration = round(end_time - start_time, 2)
                
                logger.info(f"🎉 Refactoring completed with fallback in {total_duration}s")
                logger.info(f"📏 Final output: {len(refactored_code)} chars")
                
                return RefactorResponse(
                    refactored_code=refactored_code,
                    language=request.language,
                    success=True,
                    error=f"Synthesis failed, using first successful result: {str(synthesis_error)}"
                )
        
        except Exception as e:
            end_time = time.time()
            total_duration = round(end_time - start_time, 2)
            
            logger.error(f"💥 Refactoring process failed after {total_duration}s")
            logger.error(f"🔥 Error: {str(e)}")
            
            return RefactorResponse(
                refactored_code=request.code,
                language=request.language,
                success=False,
                error=f"Refactoring failed: {str(e)}"
            )
    
    def get_llm_responses_summary(self, responses: List[LLMResponse]) -> dict:
        """Get a summary of all LLM responses for debugging"""
        summary = {
            "total_responses": len(responses),
            "successful_responses": len([r for r in responses if r.success]),
            "failed_responses": len([r for r in responses if not r.success]),
            "providers": [
                {
                    "provider": r.provider,
                    "success": r.success,
                    "error": r.error,
                    "code_length": len(r.refactored_code) if r.refactored_code else 0
                }
                for r in responses
            ]
        }
        
        # Log detailed provider results
        for provider_info in summary["providers"]:
            if provider_info["success"]:
                logger.info(f"   ✅ {provider_info['provider']}: {provider_info['code_length']} chars")
            else:
                logger.warning(f"   ❌ {provider_info['provider']}: {provider_info['error']}")
        
        return summary 