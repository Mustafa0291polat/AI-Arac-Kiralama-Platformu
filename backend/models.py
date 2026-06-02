from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    hashed_password = Column(String(255), nullable=False)

class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    owner_username = Column(String(50), nullable=False, index=True)
    brand = Column(String(50), index=True, nullable=False)
    model = Column(String(50), index=True, nullable=False)
    city = Column(String(50), index=True, nullable=False)
    district = Column(String(50), index=True, nullable=True)
    price = Column(Integer, index=True, nullable=False)
    weekly_price = Column(Integer, nullable=True)
    monthly_price = Column(Integer, nullable=True)
    year = Column(Integer, index=True, nullable=False)
    fuel_type = Column(String(50), nullable=True)
    transmission = Column(String(50), nullable=True)
    km = Column(Integer, nullable=True)
    body_type = Column(String(50), nullable=True)
    power_range = Column(String(50), nullable=True)
    engine_size = Column(String(50), nullable=True)
    drive_type = Column(String(50), nullable=True)
    color = Column(String(50), nullable=True)
    warranty = Column(String(10), nullable=True)
    heavy_damage = Column(String(10), nullable=True)
    seller_type = Column(String(20), nullable=True)
    image_url = Column(String(255), nullable=True)
    image_urls = Column(String(1000), nullable=True)
    phone_number = Column(String(20), nullable=True)
    available = Column(String(20), nullable=False, default="Kiralık")
    description = Column(String(255), nullable=True)