from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from user_service.schemas.base_schema import Base

class Friend(Base):
    __tablename__ = 'friends'

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)  # Ссылка на пользователя
    friend_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)  # Ссылка на друга
