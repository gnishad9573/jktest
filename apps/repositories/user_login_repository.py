from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.users import User
from auth.auth import verify_password, create_access_token
from schemas.users_create import  UserLogin


class UserLoginRepository:
    def __init__(self, db:AsyncSession):
        self.db = db
    
    async def login(self, user_data: UserLogin):
        """Authenticate user and return JWT"""
        result = await self.db.execute(select(User).filter(User.username == user_data.username))
        user = result.scalar_one_or_none()

        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        token = create_access_token(data={"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}