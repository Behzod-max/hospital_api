# SQLAlchemy'dan kerakli funksiyalarni chaqiramiz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# .env faylidagi ma'lumotlarni o'qish uchun
from dotenv import load_dotenv

# Operatsion tizimdan .env ma'lumotlarini olish uchun
import os


# .env faylini yuklaymiz
load_dotenv()


# .env faylidan PostgreSQL ulanish manzilini olamiz
DATABASE_URL = os.getenv("DATABASE_URL")


# PostgreSQL bilan ulanishni yaratamiz
engine = create_engine(DATABASE_URL)


# Database bilan ishlash uchun sessiya yaratamiz
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Barcha modellarimiz uchun asosiy klass
Base = declarative_base()


# Har bir API so'rovi uchun database sessiyasini beramiz
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        # Ish tugagandan keyin sessiyani yopamiz
        db.close()