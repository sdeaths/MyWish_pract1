from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from ad_service.schemas.base_schema import Base

class Gift(Base):
    __tablename__ = 'gifts'

    id = Column(UUID(as_uuid=True), primary_key=True)
    wishlist_id = Column(UUID(as_uuid=True), ForeignKey('wishlists.id'), nullable=False)  # Связь с вишлистом
    name = Column(String, nullable=False)
