from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Geçici SQLite Veritabanı (Proje klasöründe sql_app.db adında bir dosya oluşturur)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# SQLite, FastAPI ile aynı anda birden fazla istek alırken sorun çıkarmasın diye check_same_thread False yapıyoruz.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()