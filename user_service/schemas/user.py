from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from user_service.schemas.base_schema import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True)
    login = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
