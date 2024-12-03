from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body
from user_service.service.users_service import UserService
from user_service.models.User import User
from user_service.models.Friend import Friend
from user_service.models.Interests import Interests
# from ad_service.models.Wishlist import Wishlist, Gift
from typing import List

users_router = APIRouter(prefix='/users', tags=['Users'])


@users_router.get('/')
def get_users(user_service: UserService = Depends(UserService)) -> List[User]:
    """Получить список всех пользователей"""
    return user_service.get_users()


@users_router.get('/{user_id}')
def get_user(user_id: UUID, user_service: UserService = Depends(UserService)) -> User:
    """Получить пользователя по ID"""
    try:
        return user_service.get_user_by_id(user_id)
    except KeyError:
        raise HTTPException(404, f'User with id={user_id} not found')


@users_router.post('/')
def create_user(
    login: str = Body(..., embed=True),
    password_hash: str = Body(..., embed=True),
    user_service: UserService = Depends(UserService)
) -> User:
    """Создать нового пользователя"""
    try:
        user = user_service.create_user(login, password_hash)
        return user.dict()
    except Exception as e:
        raise HTTPException(400, str(e))


@users_router.post('/friends')
def add_friend(
    user_id: UUID = Body(..., embed=True),
    friend_id: UUID = Body(..., embed=True),
    user_service: UserService = Depends(UserService)
) -> Friend:
    """Добавить друга пользователю"""
    try:
        friend = user_service.add_friend(user_id, friend_id)
        return friend.dict()
    except KeyError:
        raise HTTPException(404, f'User or friend not found')
    except Exception as e:
        raise HTTPException(400, str(e))


@users_router.get('/{user_id}/interests')
def get_interests(user_id: UUID, user_service: UserService = Depends(UserService)) -> Interests:
    """Получить интересы пользователя"""
    try:
        return user_service.get_interests(user_id)
    except KeyError:
        raise HTTPException(404, f'Interests for user with id={user_id} not found')


@users_router.post('/{user_id}/interests')
def set_interests(
    user_id: UUID,
    interests: str = Body(..., embed=True),
    user_service: UserService = Depends(UserService)
) -> Interests:
    """Установить интересы пользователя"""
    try:
        return user_service.set_interests(user_id, interests).dict()
    except Exception as e:
        raise HTTPException(400, str(e))


# @users_router.post('/{user_id}/wishlist/interests')
# def create_wishlist_with_interests(
#     user_id: UUID,
#     interests: str = Body(..., embed=True),
#     user_service: UserService = Depends(UserService)
# ) -> Wishlist:
#     """Создать вишлист с названием 'Interests' на основе интересов пользователя"""
#     try:
#         # Фейковая функция для генерации подарков на основе интересов
#         def generate_fake_gifts(interests: str) -> List[Gift]:
#             interests_list = interests.split(", ")
#             return [Gift(id=UUID(), wishlist_id=UUID(), name=f"Fake {interest}") for interest in interests_list]

#         # Генерация фейковых подарков
#         fake_gifts = generate_fake_gifts(interests)
#         wishlist = Wishlist(id=UUID(), user_id=user_id, gifts=fake_gifts)
#         return wishlist.dict()
#     except Exception as e:
#         raise HTTPException(400, str(e))
