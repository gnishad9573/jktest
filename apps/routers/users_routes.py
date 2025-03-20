from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users_create import  UserCreate, UserLogin, Token
from database import get_db
from sqlalchemy.exc import SQLAlchemyError
from repositories.user_repository import UserRepository
from services.users_service import UserService


router = APIRouter(prefix="/users", tags=["users"])

async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))

@router.post("/", status_code=201)
async def regirster_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    """Create a new user"""
    try:
        return await service.create_user(user)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

