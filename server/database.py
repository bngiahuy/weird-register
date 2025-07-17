from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User # Import User model

DATABASE_URL = "sqlite:///./test.db" # Tên file SQLite

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()