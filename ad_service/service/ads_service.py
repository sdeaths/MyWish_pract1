from uuid import UUID
from typing import List
from ad_service.models.Wishlist import Wishlist
from ad_service.models.Gift import Gift
from ad_service.repositories.local_gift_repo import GiftRepo
from ad_service.repositories.local_wishlist_repo import WishlistRepo


class AdsService:
    wishlist_repo: WishlistRepo
    gift_repo: GiftRepo

    def __init__(self) -> None:
        self.wishlist_repo = WishlistRepo()
        self.gift_repo = GiftRepo()

    def get_wishlists(self) -> List[Wishlist]:
        """Получить список всех вишлистов"""
        return self.wishlist_repo.get_wishlists()

    def create_wishlist(self, user_id: UUID) -> Wishlist:
        """Создать новый вишлист для пользователя"""
        wishlist = Wishlist(id=UUID(), user_id=user_id, gifts=[])
        return self.wishlist_repo.create_wishlist(wishlist)

    def get_gifts(self, wishlist_id: UUID) -> List[Gift]:
        """Получить список подарков в вишлисте"""
        return self.gift_repo.get_gifts_by_wishlist_id(wishlist_id)

    def add_gift(self, wishlist_id: UUID, name: str) -> Gift:
        """Добавить подарок в вишлист"""
        wishlist = self.wishlist_repo.get_wishlist_by_id(wishlist_id)
        if not wishlist:
            raise ValueError("Wishlist not found")
        
        gift = Gift(id=UUID(), wishlist_id=wishlist_id, name=name)
        return self.gift_repo.create_gift(gift)

    def delete_gift(self, gift_id: UUID) -> None:
        """Удалить подарок из вишлиста"""
        self.gift_repo.delete_gift_by_id(gift_id)
