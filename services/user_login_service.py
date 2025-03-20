from schemas.users_create import  UserLogin
from repositories.user_login_repository import UserLoginRepository 

class UserLoginService:
    def __init__(self, user_repo: UserLoginRepository):
        self.user_repo = user_repo
    
    async def login(self, userlogin: UserLogin):
        """Create a new book"""
        return await self.user_repo.login(userlogin)