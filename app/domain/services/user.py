from typing import Optional

from app.domain.repository.user_repository import UserRepository
from app.domain.model.user import User, Profile


class UserService:
    __user_repository: UserRepository = UserRepository

    @classmethod
    def get_user(cls, email: str) -> Optional[User]:
        user = cls.__user_repository.get_user_by_email(email)
        if not user:
            return None
        return User(email=user.email)

    @classmethod
    def get_profile(cls, email: str) -> Optional[Profile]:
        user = cls.get_user(email=email)
        if not user:
            return None
        return Profile(email=user.email)

    @classmethod
    def update_user_last_name(cls, email: str) -> Optional[Profile]:
        user = cls.__user_repository.update_user(email=email)
        if not user:
            return None
        return Profile(email=user.email)
