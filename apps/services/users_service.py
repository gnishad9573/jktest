from schemas.users_create import UserCreate, UserLogin
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, user: UserCreate):
        """Create a new book"""
        return await self.user_repo.register(user)
    
    
