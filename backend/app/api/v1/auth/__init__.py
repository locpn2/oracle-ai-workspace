from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from typing import Optional, List
import hashlib
import secrets
from ....models.user import LoginRequest, LoginResponse, User, Token, UserCreate, UserResponse
from ....core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
)
from ....core.config import get_settings
from ....db.postgres import vector_db

router = APIRouter()
settings = get_settings()

DEMO_USERS = {
    "demo@oraclevision.com": {
        "id": "1",
        "email": "demo@oraclevision.com",
        "name": "Demo User",
        "password": "demo123",
        "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NAomW1IFK3H.",
        "is_active": True,
    }
}

refresh_tokens: List[dict] = []
audit_logs: List[dict] = []

def log_audit(user_id: str, action: str, details: dict = None, ip: str = None):
    """Log action to audit trail"""
    audit_logs.append({
        "user_id": user_id,
        "action": action,
        "details": details,
        "ip_address": ip,
        "created_at": datetime.utcnow().isoformat()
    })


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    """User registration"""
    if user.email in DEMO_USERS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user_id = str(len(DEMO_USERS) + 1)
    hashed_pw = get_password_hash(user.password)
    
    DEMO_USERS[user.email] = {
        "id": user_id,
        "email": user.email,
        "name": user.name,
        "password": user.password,
        "hashed_password": hashed_pw,
        "is_active": True,
    }
    
    log_audit(user_id, "register", {"email": user.email})
    
    return UserResponse(
        id=user_id,
        email=user.email,
        name=user.name,
    )


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, ip: Optional[str] = None):
    """Login with access token + refresh token"""
    user = DEMO_USERS.get(request.email)
    
    if not user or not verify_password(request.password, user.get("hashed_password", "")):
        if user:
            log_audit(user["id"], "login_failed", {"reason": "invalid_password"}, ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    access_token = create_access_token(
        data={"sub": user["id"], "email": user["email"]},
        expires_delta=timedelta(minutes=15),
    )
    
    refresh_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    
    refresh_tokens.append({
        "token_hash": token_hash,
        "user_id": user["id"],
        "expires_at": (datetime.utcnow() + timedelta(days=7)).isoformat(),
        "revoked": False,
    })
    
    log_audit(user["id"], "login", {"email": user["email"]}, ip)
    
    return LoginResponse(
        access_token=access_token,
        user=User(
            id=user["id"],
            email=user["email"],
            name=user["name"],
        ),
    )


@router.post("/logout")
async def logout(refresh_token: str, user_id: Optional[str] = None):
    """Logout - revoke refresh token"""
    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    
    for token in refresh_tokens:
        if token["token_hash"] == token_hash:
            token["revoked"] = True
            if user_id:
                log_audit(user_id, "logout", {"token_revoked": True})
            break
    
    return {"message": "Logged out successfully"}


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    """Refresh access token with token rotation"""
    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    
    token_data = None
    for token in refresh_tokens:
        if token["token_hash"] == token_hash and not token["revoked"]:
            token_data = token
            break
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or revoked refresh token",
        )
    
    expires = datetime.fromisoformat(token_data["expires_at"])
    if expires < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
        )
    
    user_id = token_data["user_id"]
    
    for user in DEMO_USERS.values():
        if user["id"] == user_id:
            token_data["revoked"] = True
            
            new_access_token = create_access_token(
                data={"sub": user["id"], "email": user["email"]},
                expires_delta=timedelta(minutes=15),
            )
            
            new_refresh = secrets.token_urlsafe(32)
            new_hash = hashlib.sha256(new_refresh.encode()).hexdigest()
            
            refresh_tokens.append({
                "token_hash": new_hash,
                "user_id": user_id,
                "expires_at": (datetime.utcnow() + timedelta(days=7)).isoformat(),
                "revoked": False,
            })
            
            log_audit(user_id, "token_refresh", {"rotated": True})
            
            return Token(access_token=new_access_token)
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found",
    )


@router.get("/me", response_model=User)
async def get_current_user(token: str = Depends(lambda: None)):
    """Get current user info"""
    return User(
        id="1",
        email="demo@oraclevision.com",
        name="Demo User",
    )


@router.get("/audit-logs")
async def get_audit_logs(limit: int = 50):
    """Get audit logs (admin only - for demo returns all)"""
    return audit_logs[:limit]
