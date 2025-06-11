import asyncio
import os
import time
import logging
from typing import List, Optional
import openai
import anthropic
import google.generativeai as genai
from models import LLMResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with multiple LLM providers"""
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.gemini_model = None
        self._initialize_clients()
    
    def _initialize_clients(self) -> None:
        """Initialize all LLM clients with API keys"""
        logger.info("🔧 Initializing LLM clients...")
        
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        google_key = os.getenv("GOOGLE_API_KEY")
        
        if openai_key:
            self.openai_client = openai.AsyncOpenAI(api_key=openai_key)
            logger.info("✅ OpenAI client initialized")
        else:
            logger.warning("⚠️  OpenAI API key not found")
        
        if anthropic_key:
            self.anthropic_client = anthropic.AsyncAnthropic(api_key=anthropic_key)
            logger.info("✅ Anthropic client initialized")
        else:
            logger.warning("⚠️  Anthropic API key not found")
        
        if google_key:
            genai.configure(api_key=google_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
            logger.info("✅ Google Gemini client initialized")
        else:
            logger.warning("⚠️  Google API key not found")
    
    def _create_refactor_prompt(self, code: str, language: str) -> str:
        """Create a consistent prompt for code refactoring"""
        return f"""Please refactor and improve the following {language} code with a focus on:
1. Readability and clear naming conventions
2. Maintainability and modular design
3. Defensive programming with proper error handling
4. Modern and best practices for {language}
5. Code efficiency where applicable
6. KISS and DRY principles

Original code:
```{language}
{code}
```

Please provide only the improved code without any explanations or comments about the changes."""
    
    async def call_openai_gpt4(self, code: str, language: str) -> LLMResponse:
        """Call OpenAI GPT-4.1 for code refactoring"""
        provider_name = "OpenAI GPT-4.1"
        start_time = time.time()
        
        logger.info(f"🚀 Starting {provider_name} API call for {language} code ({len(code)} chars)")
        
        try:
            if not self.openai_client:
                raise ValueError("OpenAI client not initialized")
            
            prompt = self._create_refactor_prompt(code, language)
            logger.info(f"📤 Sending request to {provider_name}...")
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",  # Using a more stable model
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=4000
            )
            
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            refactored_code = response.choices[0].message.content.strip()
            
            logger.info(f"✅ {provider_name} API call successful!")
            logger.info(f"⏱️  Duration: {duration}s")
            logger.info(f"📏 Input: {len(code)} chars → Output: {len(refactored_code)} chars")
            logger.info(f"💰 Usage: {response.usage.prompt_tokens} prompt + {response.usage.completion_tokens} completion = {response.usage.total_tokens} total tokens")
            
            return LLMResponse(
                provider=provider_name,
                refactored_code=refactored_code,
                success=True
            )
        
        except Exception as e:
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            logger.error(f"❌ {provider_name} API call failed!")
            logger.error(f"⏱️  Duration: {duration}s")
            logger.error(f"🔥 Error: {str(e)}")
            
            return LLMResponse(
                provider=provider_name,
                refactored_code="",
                success=False,
                error=str(e)
            )
    
    async def call_anthropic_claude(self, code: str, language: str) -> LLMResponse:
        """Call Anthropic Claude Sonnet 4 for code refactoring"""
        provider_name = "Anthropic Claude Sonnet 3.5"
        start_time = time.time()
        
        logger.info(f"🚀 Starting {provider_name} API call for {language} code ({len(code)} chars)")
        
        try:
            if not self.anthropic_client:
                raise ValueError("Anthropic client not initialized")
            
            prompt = self._create_refactor_prompt(code, language)
            logger.info(f"📤 Sending request to {provider_name}...")
            
            response = await self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",  # Using a stable model version
                max_tokens=4000,
                temperature=0.1,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            refactored_code = response.content[0].text.strip()
            
            logger.info(f"✅ {provider_name} API call successful!")
            logger.info(f"⏱️  Duration: {duration}s")
            logger.info(f"📏 Input: {len(code)} chars → Output: {len(refactored_code)} chars")
            logger.info(f"💰 Usage: {response.usage.input_tokens} input + {response.usage.output_tokens} output tokens")
            
            return LLMResponse(
                provider=provider_name,
                refactored_code=refactored_code,
                success=True
            )
        
        except Exception as e:
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            logger.error(f"❌ {provider_name} API call failed!")
            logger.error(f"⏱️  Duration: {duration}s")
            logger.error(f"🔥 Error: {str(e)}")
            
            return LLMResponse(
                provider=provider_name,
                refactored_code="",
                success=False,
                error=str(e)
            )
    
    async def call_google_gemini(self, code: str, language: str) -> LLMResponse:
        """Call Google Gemini 2.5 Pro for code refactoring"""
        provider_name = "Google Gemini 1.5 Pro"
        start_time = time.time()
        
        logger.info(f"🚀 Starting {provider_name} API call for {language} code ({len(code)} chars)")
        
        try:
            if not self.gemini_model:
                raise ValueError("Gemini model not initialized")
            
            prompt = self._create_refactor_prompt(code, language)
            logger.info(f"📤 Sending request to {provider_name}...")
            
            response = await asyncio.to_thread(
                self.gemini_model.generate_content,
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=4000
                )
            )
            
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            refactored_code = response.text.strip()
            
            logger.info(f"✅ {provider_name} API call successful!")
            logger.info(f"⏱️  Duration: {duration}s")
            logger.info(f"📏 Input: {len(code)} chars → Output: {len(refactored_code)} chars")
            
            # Google API doesn't provide token usage in the same way
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                logger.info(f"💰 Usage: {response.usage_metadata.prompt_token_count} prompt + {response.usage_metadata.candidates_token_count} completion tokens")
            
            return LLMResponse(
                provider=provider_name,
                refactored_code=refactored_code,
                success=True
            )
        
        except Exception as e:
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            logger.error(f"❌ {provider_name} API call failed!")
            logger.error(f"⏱️  Duration: {duration}s")
            logger.error(f"🔥 Error: {str(e)}")
            
            return LLMResponse(
                provider=provider_name,
                refactored_code="",
                success=False,
                error=str(e)
            )
    
    async def get_all_refactors(self, code: str, language: str) -> List[LLMResponse]:
        """Get refactored code from all LLM providers concurrently"""
        logger.info("🎯 Starting concurrent calls to all LLM providers...")
        overall_start_time = time.time()
        
        tasks = [
            self.call_openai_gpt4(code, language),
            self.call_anthropic_claude(code, language),
            self.call_google_gemini(code, language)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        overall_end_time = time.time()
        overall_duration = round(overall_end_time - overall_start_time, 2)
        
        # Handle any exceptions that occurred
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                provider_names = ["OpenAI GPT-4.1", "Anthropic Claude Sonnet 3.5", "Google Gemini 1.5 Pro"]
                logger.error(f"💥 Exception in {provider_names[i]}: {str(result)}")
                processed_results.append(LLMResponse(
                    provider=provider_names[i],
                    refactored_code="",
                    success=False,
                    error=str(result)
                ))
            else:
                processed_results.append(result)
        
        # Summary statistics
        successful_calls = [r for r in processed_results if r.success]
        failed_calls = [r for r in processed_results if not r.success]
        
        logger.info(f"📊 Summary of concurrent API calls:")
        logger.info(f"⏱️  Total duration: {overall_duration}s")
        logger.info(f"✅ Successful: {len(successful_calls)}/{len(processed_results)}")
        logger.info(f"❌ Failed: {len(failed_calls)}/{len(processed_results)}")
        
        if successful_calls:
            logger.info("✅ Successful providers:")
            for result in successful_calls:
                logger.info(f"   - {result.provider}")
        
        if failed_calls:
            logger.warning("❌ Failed providers:")
            for result in failed_calls:
                logger.warning(f"   - {result.provider}: {result.error}")
        
        return processed_results
    
    def _create_synthesis_prompt(self, responses: List[LLMResponse], language: str) -> str:
        """Create prompt for synthesizing multiple refactored versions"""
        successful_responses = [r for r in responses if r.success and r.refactored_code.strip()]
        
        if not successful_responses:
            raise ValueError("No successful refactoring responses to synthesize")
        
        prompt = f"""Please analyze and synthesize the following {language} code refactoring suggestions into a single, best version.
Focus on combining the best aspects of each version with emphasis on:
1. Readability and maintainability
2. Defensive programming and error handling
3. Modern, and best practices for {language}
4. Code efficiency and performance
5. KISS and DRY principles

Here are the refactored versions:

"""
        
        for i, response in enumerate(successful_responses, 1):
            prompt += f"Version {i} ({response.provider}):\n```{language}\n{response.refactored_code}\n```\n\n"
        
        prompt += f"Please provide only the final, best synthesized {language} code without explanations."
        
        return prompt
    
    async def synthesize_refactors(self, responses: List[LLMResponse], language: str) -> str:
        """Use GPT-4.1 to synthesize multiple refactored versions into one best version"""
        logger.info("🧪 Starting synthesis of multiple refactored versions...")
        start_time = time.time()
        
        try:
            if not self.openai_client:
                raise ValueError("OpenAI client not initialized for synthesis")
            
            successful_responses = [r for r in responses if r.success and r.refactored_code.strip()]
            logger.info(f"📝 Synthesizing {len(successful_responses)} successful responses")
            
            prompt = self._create_synthesis_prompt(responses, language)
            logger.info("📤 Sending synthesis request to OpenAI...")
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=4000
            )
            
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            synthesized_code = response.choices[0].message.content.strip()
            
            logger.info("✅ Code synthesis completed successfully!")
            logger.info(f"⏱️  Synthesis duration: {duration}s")
            logger.info(f"📏 Final output: {len(synthesized_code)} chars")
            logger.info(f"💰 Synthesis usage: {response.usage.total_tokens} tokens")
            
            return synthesized_code
        
        except Exception as e:
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            logger.error("❌ Code synthesis failed!")
            logger.error(f"⏱️  Duration: {duration}s")
            logger.error(f"🔥 Error: {str(e)}")
            
            # Fallback: return the first successful refactor if synthesis fails
            successful_responses = [r for r in responses if r.success and r.refactored_code.strip()]
            if successful_responses:
                logger.info(f"🔄 Falling back to {successful_responses[0].provider} response")
                return successful_responses[0].refactored_code
            raise e 