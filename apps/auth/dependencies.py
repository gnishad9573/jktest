from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.users import User
from auth.auth import SECRET_KEY, ALGORITHM, decode_access_token, verify_password
from schemas.users_create import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str =Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    payload = decode_access_token(token)  # Implement JWT decoding
    username: str = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username
