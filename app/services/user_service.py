from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.schema import UserCreate


class UserService:
    def __init__(self, session: Session):
        self._db = session

    def list_users(self) -> list[User]:
        return self._db.query(User).all()

    def get_user(self, user_id: int) -> User | None:
        return self._db.query(User).filter(User.id == user_id).first()

    def create_user(self, payload: UserCreate) -> User:
        user = User(name=payload.name)
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def update_user(self, user_id: int, name: str) -> User | None:
        user = self.get_user(user_id)
        if user is None:
            return None
        user.name = name
        self._db.commit()
        self._db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        if user is None:
            return False
        self._db.delete(user)
        self._db.commit()
        return True