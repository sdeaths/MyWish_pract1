from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body
from ad_service.service.ads_service import AdsService
from ad_service.models.Wishlist import Wishlist
from ad_service.models.Gift import Gift
from typing import List

ads_router = APIRouter(prefix='/ads', tags=['Ads'])


@ads_router.get('/wishlists')
def get_wishlists(ads_service: AdsService = Depends(AdsService)) -> List[Wishlist]:
    """Получить все вишлисты"""
    return ads_service.get_wishlists()


@ads_router.post('/wishlists')
def create_wishlist(
    user_id: UUID = Body(..., embed=True),
    ads_service: AdsService = Depends(AdsService)
) -> Wishlist:
    """Создать новый вишлист для пользователя"""
    try:
        wishlist = ads_service.create_wishlist(user_id)
        return wishlist.dict()
    except Exception as e:
        raise HTTPException(400, str(e))


@ads_router.get('/gifts/{wishlist_id}')
def get_gifts(wishlist_id: UUID, ads_service: AdsService = Depends(AdsService)) -> List[Gift]:
    """Получить список подарков в вишлисте"""
    try:
        return ads_service.get_gifts(wishlist_id)
    except KeyError:
        raise HTTPException(404, f'Wishlist with id={wishlist_id} not found')


@ads_router.post('/gifts')
def add_gift(
    wishlist_id: UUID = Body(..., embed=True),
    name: str = Body(..., embed=True),
    ads_service: AdsService = Depends(AdsService)
) -> Gift:
    """Добавить подарок в вишлист"""
    try:
        gift = ads_service.add_gift(wishlist_id, name)
        return gift.dict()
    except KeyError:
        raise HTTPException(404, f'Wishlist with id={wishlist_id} not found')
    except Exception as e:
        raise HTTPException(400, str(e))


@ads_router.delete('/gifts/{gift_id}')
def delete_gift(gift_id: UUID, ads_service: AdsService = Depends(AdsService)) -> None:
    """Удалить подарок из вишлиста"""
    try:
        ads_service.delete_gift(gift_id)
        return {"message": f"Gift with id={gift_id} has been deleted"}
    except KeyError:
        raise HTTPException(404, f'Gift with id={gift_id} not found')


@ads_router.post('/wishlists/interests')
def create_wishlist_with_interests(
    interests: str = Body(..., embed=True),
    ads_service: AdsService = Depends(AdsService)
) -> Wishlist:
    """Создать вишлист с названием 'Interests' и фейковыми подарками"""
    try:
        # Фейковая функция для генерации подарков на основе интересов
        def generate_fake_gifts(interests: str) -> List[Gift]:
            interests_list = interests.split(", ")
            return [Gift(id=UUID(), wishlist_id=UUID(), name=f"Fake {interest}") for interest in interests_list]

        # Генерация фейковых подарков
        fake_gifts = generate_fake_gifts(interests)
        wishlist = Wishlist(id=UUID(), user_id=UUID(), gifts=fake_gifts)
        return wishlist.dict()
    except Exception as e:
        raise HTTPException(400, str(e))
