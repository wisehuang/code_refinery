import os
import logging
from typing import Optional
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger(__name__)

# Initialize the security scheme
security = HTTPBearer(auto_error=False)

class TokenAuth:
    """Simple token-based authentication"""
    
    def __init__(self):
        self.api_token = os.getenv("API_TOKEN")
        self.auth_enabled = os.getenv("AUTH_ENABLED", "true").lower() == "true"
        
        if self.auth_enabled:
            if not self.api_token:
                logger.warning("⚠️  AUTH_ENABLED is true but API_TOKEN is not set. Authentication will fail.")
            else:
                logger.info("🔐 Authentication enabled")
        else:
            logger.info("🔓 Authentication disabled")
    
    def verify_token(self, token: str) -> bool:
        self.api_token = os.getenv("API_TOKEN")
        self.auth_enabled = os.getenv("AUTH_ENABLED", "true").lower() == "true"
        
        """Verify if the provided token is valid"""
        if not self.auth_enabled:
            return True
            
        if not self.api_token:
            logger.error("❌ API_TOKEN not configured")
            return False
            
        return token == self.api_token
    
    def get_current_user(self, credentials: Optional[HTTPAuthorizationCredentials] = Security(security)):
        """FastAPI dependency to verify authentication"""
        # If authentication is disabled, allow access
        if not self.auth_enabled:
            return {"authenticated": False, "reason": "auth_disabled"}
        
        if not credentials:
            logger.warning("🚫 No authorization header provided")
            raise HTTPException(
                status_code=401,
                detail="Authorization header required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not self.verify_token(credentials.credentials):
            self.api_token = os.getenv("API_TOKEN")
            
            # TODO: Add logging for the token
            logger.warning(f"🚫 Invalid token provided: {credentials.credentials[:10]}...")
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        logger.debug("✅ Authentication successful")
        return {"authenticated": True, "token": credentials.credentials}

# Global instance
token_auth = TokenAuth()

# Dependency function for easy use
def get_authenticated_user(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)):
    """Dependency function to get authenticated user"""
    return token_auth.get_current_user(credentials) 