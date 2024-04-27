from app.db.models import User, SubUser
from app.schemas.schemas import UserModel


class SubUsersManager(object):
    async def create_subuser(self, user: User, sub_user: SubUser):
        pass


class UsersManager(SubUsersManager):
    def __init__(self) -> None:
        super().__init__()
    
    async def user_is_admin(self, user: User | UserModel) -> bool:
        return True if user.is_admin else False
    
    async def user_is_active(self, user: User | UserModel) -> bool:
        return True if user.is_active else False
    
    async def user_is_owner(self, user: User | UserModel) -> bool:
        return True if user.is_owner else False
    

