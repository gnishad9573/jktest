from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from models.users import User
from auth.auth import hash_password, verify_password, create_access_token
from schemas.users_create import UserCreate, UserLogin, Token


class UserRepository:
    def __init__(self, db:AsyncSession):
        self.db = db
    
    async def register(self, user_data: UserCreate) -> User:
        """Create a new user in the database"""
        existing_user = await self.db.execute(select(User).filter(User.username == user_data.username))
        if existing_user.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already exists")
        new_user = User(username=user_data.username, email=user_data.email, hashed_password=hash_password(user_data.password))
        self.db.add(new_user)
        await self.db.commit()
        return {"message": "User registered successfully"}
