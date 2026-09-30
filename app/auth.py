from typing import Optional, List
from pydantic import BaseModel
from jose import jwt, JWTError
from fastmcp.server.auth import AuthContext

# Hardcoded secret key for local development (Use Env variables in production)
JWT_SECRET = "YOUR_ENTERPRISE_ECC_OR_RSA_HS256_SECRET_KEY"
JWT_ALGORITHM = "HS256"

class TokenClaims(BaseModel):
    sub: str  # User identifier (e.g., "user_01J")
    scopes: List[str]  # App permission scopes (e.g., ["audit:read", "admin:write"])

def decode_and_verify_token(token: str) -> Optional[TokenClaims]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return TokenClaims(
            sub=payload.get("sub"),
            scopes=payload.get("scopes", [])
        )
    except JWTError:
        return None

# Custom structural Scoping Interceptor Check
def require_scope(required_scope: str):
    """
    Evaluates dynamic runtime context claims before allowing the LLM client 
    to trigger the underlying tool logic.
    """
    def scope_checker(ctx: AuthContext) -> bool:
        # If running via local stdio for debugging, token defaults to None, let it pass
        if ctx.token is None:
            return True
            
        # Parse and verify network bearer string token
        claims = decode_and_verify_token(ctx.token)
        if not claims:
            return False
            
        # Verify if user token contains the target scope required for this component
        return required_scope in claims.scopes
        
    return scope_checker
