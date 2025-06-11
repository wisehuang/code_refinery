import pytest
from unittest.mock import AsyncMock, patch
from models import RefactorRequest, LLMResponse
from services.llm_service import LLMService
from services.refactor_service import RefactorService


class TestRefactorService:
    """Test cases for RefactorService"""
    
    def test_extract_code_from_markdown(self):
        """Test extraction of code from markdown blocks"""
        service = RefactorService()
        
        # Test with markdown wrapper
        markdown_code = "```python\nprint('hello')\n```"
        extracted = service._extract_code_from_markdown(markdown_code)
        assert extracted == "print('hello')"
        
        # Test without markdown wrapper
        plain_code = "print('hello')"
        extracted = service._extract_code_from_markdown(plain_code)
        assert extracted == "print('hello')"
    
    @patch('services.refactor_service.LLMService')
    async def test_refactor_code_success(self, mock_llm_service_class):
        """Test successful code refactoring"""
        mock_llm_service = AsyncMock()
        mock_llm_service_class.return_value = mock_llm_service
        
        mock_responses = [
            LLMResponse(
                provider="OpenAI GPT-4.1",
                refactored_code="print('Hello, World!')",
                success=True
            )
        ]
        
        mock_llm_service.get_all_refactors.return_value = mock_responses
        
        service = RefactorService()
        request = RefactorRequest(code="print('hello')", language="python")
        
        result = await service.refactor_code(request)
        
        assert result.success is True
        assert result.refactored_code == "print('Hello, World!')"
        assert result.language == "python" 