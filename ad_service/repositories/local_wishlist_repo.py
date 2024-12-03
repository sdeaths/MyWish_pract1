from uuid import UUID
from ad_service.models.Wishlist import Wishlist
from ad_service.models.Gift import Gift

# Локальное хранилище данных
wishlists: list[Wishlist] = []

class WishlistRepo:
    def get_wishlists(self) -> list[Wishlist]:
        """Получить все вишлисты"""
        return wishlists

    def get_wishlist_by_id(self, id: UUID) -> Wishlist:
        """Получить вишлист по ID"""
        for wishlist in wishlists:
            if wishlist.id == id:
                return wishlist
        raise KeyError(f"Wishlist with id={id} not found")

    def create_wishlist(self, wishlist: Wishlist) -> Wishlist:
        """Создать новый вишлист"""
        if len([w for w in wishlists if w.id == wishlist.id]) > 0:
            raise KeyError(f"Wishlist with id={wishlist.id} already exists")
        
        wishlists.append(wishlist)
        return wishlist
