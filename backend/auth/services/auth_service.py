from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from fastapi import HTTPException, status
import httpx

from models.user import User
from schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from shared.auth.jwt import create_access_token, create_refresh_token
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def register_user(db: AsyncSession, data: RegisterRequest) -> User:
    # Check if email exists
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        email=data.email,
        hashed_password=pwd_context.hash(data.password),
        full_name=data.full_name,
    )
    db.add(user)
    await db.flush()
    return user

async def login_user(db: AsyncSession, data: LoginRequest) -> TokenResponse:
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    # Fetch roles & permissions from RBAC service
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{settings.RBAC_SERVICE_URL}/rbac/users/{user.id}/roles")
        rbac_data = resp.json() if resp.status_code == 200 else {"roles": [], "permissions": []}

    access_token = create_access_token(
        user_id=str(user.id),
        email=user.email,
        roles=rbac_data.get("roles", []),
        permissions=rbac_data.get("permissions", []),
    )
    refresh_token = create_refresh_token(user_id=str(user.id))

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)