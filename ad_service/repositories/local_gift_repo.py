from uuid import UUID
from ad_service.models.Gift import Gift

# Локальное хранилище данных
gifts: list[Gift] = []

class GiftRepo:
    def get_gifts_by_wishlist_id(self, wishlist_id: UUID) -> list[Gift]:
        """Получить список подарков из вишлиста"""
        return [gift for gift in gifts if gift.wishlist_id == wishlist_id]

    def create_gift(self, gift: Gift) -> Gift:
        """Добавить подарок в вишлист"""
        if len([g for g in gifts if g.id == gift.id]) > 0:
            raise KeyError(f"Gift with id={gift.id} already exists")
        
        gifts.append(gift)
        return gift

    def delete_gift_by_id(self, id: UUID) -> None:
        """Удалить подарок по ID"""
        for gift in gifts:
            if gift.id == id:
                gifts.remove(gift)
                return
        raise KeyError(f"Gift with id={id} not found")
