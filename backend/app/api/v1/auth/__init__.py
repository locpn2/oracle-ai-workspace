from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ....models.user import LoginRequest, LoginResponse, User, Token
from ....core.security import (
    verify_password,
    create_access_token,
    verify_token,
)
from ....core.config import get_settings

router = APIRouter()
settings = get_settings()

DEMO_USERS = {
    "demo@oraclevision.com": {
        "id": "1",
        "email": "demo@oraclevision.com",
        "name": "Demo User",
        "password": "demo123",
    }
}


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    user = DEMO_USERS.get(request.email)
    
    if not user or user["password"] != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    access_token = create_access_token(
        data={"sub": user["id"], "email": user["email"]},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    
    return LoginResponse(
        access_token=access_token,
        user=User(
            id=user["id"],
            email=user["email"],
            name=user["name"],
        ),
    )


@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}


@router.post("/refresh", response_model=Token)
async def refresh_token(token: str):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    new_token = create_access_token(
        data={"sub": payload.get("sub"), "email": payload.get("email")},
    )
    
    return Token(access_token=new_token)
