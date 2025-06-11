from pydantic import BaseModel, Field
from typing import Optional


class RefactorRequest(BaseModel):
    """Request model for code refactoring"""
    code: str = Field(..., description="Source code to refactor")
    language: str = Field(..., description="Programming language of the code")


class RefactorResponse(BaseModel):
    """Response model for refactored code"""
    refactored_code: str = Field(..., description="Refactored and improved code")
    language: str = Field(..., description="Programming language of the code")
    success: bool = Field(default=True, description="Whether the refactoring was successful")
    error: Optional[str] = Field(default=None, description="Error message if any")


class LLMResponse(BaseModel):
    """Response model for individual LLM calls"""
    provider: str = Field(..., description="LLM provider name")
    refactored_code: str = Field(..., description="Refactored code from this provider")
    success: bool = Field(default=True, description="Whether the call was successful")
    error: Optional[str] = Field(default=None, description="Error message if any") 