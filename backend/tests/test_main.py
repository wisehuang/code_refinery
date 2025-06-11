import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from main import app
from models import RefactorResponse

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns correct response"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Code Refinery API"
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_supported_languages():
    """Test supported languages endpoint"""
    response = client.get("/supported-languages")
    assert response.status_code == 200
    data = response.json()
    assert "languages" in data
    assert isinstance(data["languages"], list)
    assert "python" in data["languages"]
    assert "javascript" in data["languages"]


def test_refactor_empty_code():
    """Test refactor endpoint with empty code"""
    response = client.post("/refactor", json={
        "code": "",
        "language": "python"
    })
    assert response.status_code == 400
    assert "Code field cannot be empty" in response.json()["detail"]


def test_refactor_empty_language():
    """Test refactor endpoint with empty language"""
    response = client.post("/refactor", json={
        "code": "print('hello')",
        "language": ""
    })
    assert response.status_code == 400
    assert "Language field cannot be empty" in response.json()["detail"]


@patch('main.refactor_service.refactor_code')
def test_refactor_success(mock_refactor):
    """Test successful refactoring"""
    mock_response = RefactorResponse(
        refactored_code="print('Hello, World!')",
        language="python",
        success=True
    )
    mock_refactor.return_value = mock_response
    
    response = client.post("/refactor", json={
        "code": "print('hello')",
        "language": "python"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["refactored_code"] == "print('Hello, World!')"
    assert data["language"] == "python"


@patch('main.refactor_service.refactor_code')
def test_refactor_failure(mock_refactor):
    """Test refactoring failure"""
    mock_response = RefactorResponse(
        refactored_code="print('hello')",
        language="python",
        success=False,
        error="All LLM providers failed"
    )
    mock_refactor.return_value = mock_response
    
    response = client.post("/refactor", json={
        "code": "print('hello')",
        "language": "python"
    })
    
    assert response.status_code == 500
    assert "All LLM providers failed" in response.json()["detail"]


@patch('main.refactor_service.refactor_code')
def test_refactor_exception(mock_refactor):
    """Test refactoring with unexpected exception"""
    mock_refactor.side_effect = Exception("Unexpected error")
    
    response = client.post("/refactor", json={
        "code": "print('hello')",
        "language": "python"
    })
    
    assert response.status_code == 500
    assert "Internal server error" in response.json()["detail"] 