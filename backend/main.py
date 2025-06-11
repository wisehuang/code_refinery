import os
import logging
import time
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models import RefactorRequest, RefactorResponse
from services.refactor_service import RefactorService
from auth import get_authenticated_user

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Code Refinery",
    description="AI-powered code refactoring service using multiple LLM providers with token-based authentication",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize refactor service
refactor_service = RefactorService()

logger.info("🚀 Code Refinery API started successfully")


@app.get("/")
async def root():
    """Root endpoint for health check - no authentication required"""
    return {
        "message": "Code Refinery API",
        "status": "healthy",
        "version": "1.0.0",
        "authentication": "Bearer token required for protected endpoints"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint - no authentication required"""
    logger.info("💚 Health check requested")
    return {"status": "healthy"}


@app.post("/refactor", response_model=RefactorResponse)
async def refactor_code(
    request: RefactorRequest,
    current_user: dict = Depends(get_authenticated_user)
):
    """
    Refactor code using multiple LLM providers and return the best synthesized version.
    
    **Authentication Required**: This endpoint requires a valid Bearer token in the Authorization header.
    
    This endpoint:
    1. Sends the code to OpenAI GPT-4.1, Anthropic Claude Sonnet 4, and Google Gemini 2.5 Pro concurrently
    2. Collects their refactoring suggestions
    3. Uses GPT-4.1 to synthesize the results into a single best version
    4. Returns the final refactored code
    """
    request_start_time = time.time()
    
    logger.info("="*80)
    logger.info("🎯 NEW REFACTOR REQUEST")
    logger.info(f"🔐 Authentication: {current_user}")
    logger.info(f"📝 Language: {request.language}")
    logger.info(f"📏 Code length: {len(request.code)} characters")
    logger.info(f"📄 Code preview: {request.code[:100]}{'...' if len(request.code) > 100 else ''}")
    logger.info("="*80)
    
    try:
        # Validate input
        if not request.code or not request.code.strip():
            logger.warning("⚠️  Empty code field received")
            raise HTTPException(
                status_code=400,
                detail="Code field cannot be empty"
            )
        
        if not request.language or not request.language.strip():
            logger.warning("⚠️  Empty language field received")
            raise HTTPException(
                status_code=400,
                detail="Language field cannot be empty"
            )
        
        logger.info("✅ Input validation passed")
        
        # Perform refactoring
        logger.info("🔄 Starting refactoring process...")
        result = await refactor_service.refactor_code(request)
        
        request_end_time = time.time()
        total_request_duration = round(request_end_time - request_start_time, 2)
        
        # Return error response if refactoring failed
        if not result.success:
            logger.error(f"❌ Refactoring failed: {result.error}")
            logger.info(f"⏱️  Total request duration: {total_request_duration}s")
            logger.info("="*80)
            raise HTTPException(
                status_code=500,
                detail=result.error or "Refactoring failed"
            )
        
        logger.info("🎉 REFACTOR REQUEST COMPLETED SUCCESSFULLY!")
        logger.info(f"⏱️  Total request duration: {total_request_duration}s")
        logger.info(f"📏 Final result: {len(result.refactored_code)} characters")
        logger.info("="*80)
        
        return result
    
    except HTTPException:
        request_end_time = time.time()
        total_request_duration = round(request_end_time - request_start_time, 2)
        logger.info(f"⏱️  Request duration (failed): {total_request_duration}s")
        logger.info("="*80)
        raise
    except Exception as e:
        request_end_time = time.time()
        total_request_duration = round(request_end_time - request_start_time, 2)
        
        logger.error(f"💥 Unexpected error in refactor endpoint: {str(e)}")
        logger.error(f"⏱️  Request duration (error): {total_request_duration}s")
        logger.info("="*80)
        
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/supported-languages")
async def get_supported_languages(current_user: dict = Depends(get_authenticated_user)):
    """Get list of supported programming languages - authentication required"""
    logger.info("📋 Supported languages requested")
    logger.info(f"🔐 Authentication: {current_user}")
    return {
        "languages": [
            "python",
            "javascript",
            "typescript",
            "java",
            "cpp",
            "c",
            "csharp",
            "go",
            "rust",
            "php",
            "ruby",
            "swift",
            "kotlin",
            "scala",
            "r",
            "sql",
            "html",
            "css"
        ]
    }


@app.get("/auth/status")
async def get_auth_status(current_user: dict = Depends(get_authenticated_user)):
    """Get authentication status - for testing authentication"""
    logger.info("🔐 Authentication status requested")
    return {
        "authenticated": True,
        "user": current_user,
        "message": "Authentication successful"
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("🌟 Starting Code Refinery server...")
    uvicorn.run(app, host="0.0.0.0", port=8000) 