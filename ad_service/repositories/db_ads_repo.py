from uuid import UUID
from sqlalchemy.orm import Session
from ad_service.database import get_db
from ad_service.models.Wishlist import Wishlist
from ad_service.models.Gift import Gift
from ad_service.schemas.wishlist import Wishlist as DBWishlist
from ad_service.schemas.gift import Gift as DBGift


class AdsRepo:
    def __init__(self) -> None:
        self.db = next(get_db)

    def get_wishlists(self) -> list[Wishlist]:
        """Получить все вишлисты"""
        wishlists = []
        for w in self.db.query(DBWishlist).all():
            wishlists.append(Wishlist.from_orm(w))
        return wishlists

    def get_wishlist_by_id(self, id: UUID) -> Wishlist:
        """Получить вишлист по ID"""
        wishlist = self.db.query(DBWishlist).filter(DBWishlist.id == id).first()
        if wishlist is None:
            raise KeyError(f"Wishlist with id={id} not found")
        return Wishlist.from_orm(wishlist)

    def create_wishlist(self, wishlist: Wishlist) -> Wishlist:
        """Создать новый вишлист"""
        db_wishlist = DBWishlist(**wishlist.dict())
        self.db.add(db_wishlist)
        self.db.commit()
        self.db.refresh(db_wishlist)
        return Wishlist.from_orm(db_wishlist)

    def get_gifts_by_wishlist_id(self, wishlist_id: UUID) -> list[Gift]:
        """Получить подарки из вишлиста"""
        gifts = []
        for g in self.db.query(DBGift).filter(DBGift.wishlist_id == wishlist_id).all():
            gifts.append(Gift.from_orm(g))
        return gifts

    def create_gift(self, gift: Gift) -> Gift:
        """Добавить подарок в вишлист"""
        db_gift = DBGift(**gift.dict())
        self.db.add(db_gift)
        self.db.commit()
        self.db.refresh(db_gift)
        return Gift.from_orm(db_gift)

    def delete_gift_by_id(self, id: UUID) -> None:
        """Удалить подарок по ID"""
        gift = self.db.query(DBGift).filter(DBGift.id == id).first()
        if gift is None:
            raise KeyError(f"Gift with id={id} not found")
        self.db.delete(gift)
        self.db.commit()
