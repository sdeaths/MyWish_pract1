from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Получение URL базы данных из переменных окружения
import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@ad_db/ad_db")

# Создание двигателя базы данных
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
