#!/usr/bin/env python3
"""
Test script: Verify logging functionality works correctly
"""

import asyncio
import logging
import os
from services.llm_service import LLMService
from services.refactor_service import RefactorService
from models import RefactorRequest

# Set logging level to INFO to see all logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def test_logging():
    """Test logging functionality"""
    
    logger.info("🧪 Starting logging functionality test...")
    
    # Check environment variables
    logger.info("🔍 Checking API Keys...")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY") 
    google_key = os.getenv("GOOGLE_API_KEY")
    
    logger.info(f"OpenAI Key: {'✅ Set' if openai_key else '❌ Not set'}")
    logger.info(f"Anthropic Key: {'✅ Set' if anthropic_key else '❌ Not set'}")
    logger.info(f"Google Key: {'✅ Set' if google_key else '❌ Not set'}")
    
    # Initialize services (this will trigger initialization logs)
    logger.info("🔧 Initializing services...")
    refactor_service = RefactorService()
    
    # Test simple code refactoring request
    logger.info("📝 Preparing test code...")
    test_code = """def hello():
    print("hello world")

hello()"""
    
    request = RefactorRequest(
        code=test_code,
        language="python"
    )
    
    logger.info("🚀 Starting refactoring test...")
    try:
        result = await refactor_service.refactor_code(request)
        
        if result.success:
            logger.info("✅ Test completed! Refactoring successful")
            logger.info(f"📏 Input length: {len(test_code)} characters")
            logger.info(f"📏 Output length: {len(result.refactored_code)} characters")
        else:
            logger.error(f"❌ Refactoring failed: {result.error}")
            
    except Exception as e:
        logger.error(f"💥 Error occurred during testing: {str(e)}")
    
    logger.info("🏁 Test completed!")

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run test
    asyncio.run(test_logging()) 