from uuid import UUID
from sqlalchemy.orm import Session
from user_service.database import get_db
from user_service.models.User import User
from user_service.models.Friend import Friend
from user_service.models.Interests import Interests
from user_service.schemas.user import User as DBUser
from user_service.schemas.friend import Friend as DBFriend
from user_service.schemas.interests import Interests as DBInterests


class UsersRepo:
    def __init__(self) -> None:
        self.db = next(get_db)

    def get_users(self) -> list[User]:
        """Получить всех пользователей"""
        users = []
        for u in self.db.query(DBUser).all():
            users.append(User.from_orm(u))
        return users

    def get_user_by_id(self, id: UUID) -> User:
        """Получить пользователя по ID"""
        user = self.db.query(DBUser).filter(DBUser.id == id).first()
        if user is None:
            raise KeyError(f"User with id={id} not found")
        return User.from_orm(user)

    def create_user(self, user: User) -> User:
        """Создать пользователя"""
        db_user = DBUser(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return User.from_orm(db_user)

    def get_friends_by_user_id(self, user_id: UUID) -> list[Friend]:
        """Получить друзей пользователя"""
        friends = []
        for f in self.db.query(DBFriend).filter(DBFriend.user_id == user_id).all():
            friends.append(Friend.from_orm(f))
        return friends

    def create_friend(self, friend: Friend) -> Friend:
        """Добавить друга"""
        db_friend = DBFriend(**friend.dict())
        self.db.add(db_friend)
        self.db.commit()
        self.db.refresh(db_friend)
        return Friend.from_orm(db_friend)

    def get_interests_by_user_id(self, user_id: UUID) -> Interests:
        """Получить интересы пользователя"""
        interests = self.db.query(DBInterests).filter(DBInterests.user_id == user_id).first()
        if interests is None:
            raise KeyError(f"Interests for user with id={user_id} not found")
        return Interests.from_orm(interests)

    def set_interests(self, interests: Interests) -> Interests:
        """Установить интересы пользователя"""
        existing_interests = self.db.query(DBInterests).filter(DBInterests.user_id == interests.user_id).first()
        if existing_interests:
            self.db.delete(existing_interests)
        db_interests = DBInterests(**interests.dict())
        self.db.add(db_interests)
        self.db.commit()
        self.db.refresh(db_interests)
        return Interests.from_orm(db_interests)
