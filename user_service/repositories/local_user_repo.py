from uuid import UUID
from user_service.models.User import User
from user_service.models.Friend import Friend
from user_service.models.Interests import Interests

# Локальные хранилища данных
users: list[User] = [
    User(id=UUID('1d3b4e2f-6c3f-4a94-9c3c-7a2b34e5d002'), login='john_doe', password_hash='hashed_password_1'),
    User(id=UUID('5e2a1f8b-1d6f-45e9-92f3-32d34f3c78d2'), login='jane_doe', password_hash='hashed_password_2'),
]

friends: list[Friend] = []

interests: list[Interests] = []

class UserRepo:
    def get_users(self) -> list[User]:
        """Получить список всех пользователей"""
        return users

    def get_user_by_id(self, id: UUID) -> User:
        """Получить пользователя по ID"""
        for user in users:
            if user.id == id:
                return user
        raise KeyError(f"User with id={id} not found")

    def create_user(self, user: User) -> User:
        """Создать нового пользователя"""
        if any(u.id == user.id for u in users):
            raise KeyError(f"User with id={user.id} already exists")
        users.append(user)
        return user


class FriendRepo:
    def get_friends_by_user_id(self, user_id: UUID) -> list[Friend]:
        """Получить список друзей пользователя"""
        return [friend for friend in friends if friend.user_id == user_id]

    def create_friend(self, friend: Friend) -> Friend:
        """Добавить друга"""
        if any(f.id == friend.id for f in friends):
            raise KeyError(f"Friend with id={friend.id} already exists")
        friends.append(friend)
        return friend


class InterestsRepo:
    def get_interests_by_user_id(self, user_id: UUID) -> Interests:
        """Получить интересы пользователя"""
        for interest in interests:
            if interest.user_id == user_id:
                return interest
        raise KeyError(f"Interests for user with id={user_id} not found")

    def set_interests(self, interests_obj: Interests) -> Interests:
        """Установить интересы пользователя"""
        existing_interests = next((i for i in interests if i.user_id == interests_obj.user_id), None)
        if existing_interests:
            interests.remove(existing_interests)
        interests.append(interests_obj)
        return interests_obj
