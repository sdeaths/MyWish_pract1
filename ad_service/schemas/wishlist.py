from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ad_service.schemas.base_schema import Base

class Wishlist(Base):
    __tablename__ = 'wishlists'

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # Связь с пользователем
    name = Column(String, nullable=False)

    # Связь с подарками
    gifts = relationship("Gift", back_populates="wishlist")
