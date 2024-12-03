from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from user_service.schemas.base_schema import Base

class Interests(Base):
    __tablename__ = 'interests'

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)  # Ссылка на пользователя
    list = Column(String, nullable=False)  # Интересы в виде строки, разделённой запятыми
