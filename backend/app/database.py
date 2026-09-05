import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Mặc định sử dụng SQLite để chạy được ngay không cần cấu hình, sẵn sàng đổi sang PostgreSQL qua biến môi trường DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tam_giao.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

