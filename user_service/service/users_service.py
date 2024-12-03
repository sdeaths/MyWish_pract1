from uuid import UUID
from user_service.models.User import User
from user_service.models.Friend import Friend
from user_service.models.Interests import Interests 
from user_service.repositories.local_user_repo import UserRepo, FriendRepo, InterestsRepo


class UserService:
    user_repo: UserRepo
    friend_repo: FriendRepo
    interests_repo: InterestsRepo

    def __init__(self) -> None:
        self.user_repo = UserRepo()
        self.friend_repo = FriendRepo()
        self.interests_repo = InterestsRepo()

    def get_users(self) -> list[User]:
        """Получить список всех пользователей"""
        return self.user_repo.get_users()

    def create_user(self, login: str, password_hash: str) -> User:
        """Создать нового пользователя"""
        user = User(id=UUID(), login=login, password_hash=password_hash)
        return self.user_repo.create_user(user)

    def get_user_by_id(self, user_id: UUID) -> User:
        """Получить пользователя по ID"""
        return self.user_repo.get_user_by_id(user_id)

    def add_friend(self, user_id: UUID, friend_id: UUID) -> Friend:
        """Добавить друга пользователю"""
        if not self.user_repo.get_user_by_id(user_id) or not self.user_repo.get_user_by_id(friend_id):
            raise ValueError("User or Friend not found")
        
        friend = Friend(id=UUID(), user_id=user_id, friend_id=friend_id)
        return self.friend_repo.create_friend(friend)

    def get_friends(self, user_id: UUID) -> list[Friend]:
        """Получить список друзей пользователя"""
        return self.friend_repo.get_friends_by_user_id(user_id)

    def set_interests(self, user_id: UUID, interests_list: str) -> Interests:
        """Установить интересы пользователя"""
        if not self.user_repo.get_user_by_id(user_id):
            raise ValueError("User not found")
        
        interests = Interests(id=UUID(), user_id=user_id, list=interests_list)
        return self.interests_repo.set_interests(interests)

    def get_interests(self, user_id: UUID) -> Interests:
        """Получить интересы пользователя"""
        return self.interests_repo.get_interests_by_user_id(user_id)
