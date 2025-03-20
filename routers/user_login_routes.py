from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.users import User
from database import get_db
from auth.auth import verify_password, create_access_token
from schemas.users_create import Token

router = APIRouter(prefix="/login", tags=["login"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

async def authenticate_user(db: AsyncSession, username: str, password: str):
    """Verify user credentials"""
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(password, user.hashed_password):
        return None  # Invalid login
    
    return user  # Return authenticated user


@router.post("/", response_model=Token, status_code=200)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return JWT"""
    user = await authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_access_token(data={"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}

    