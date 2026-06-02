from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from backend.database import SessionLocal, engine
from backend import models


models.Base.metadata.create_all(bind=engine)


with engine.connect() as connection:
    result = connection.execute(text("PRAGMA table_info(cars)"))
    existing_columns = {row[1] for row in result}
    if "brand" not in existing_columns:
        connection.execute(text("ALTER TABLE cars ADD COLUMN brand VARCHAR(50)"))
    if "model" not in existing_columns:
        connection.execute(text("ALTER TABLE cars ADD COLUMN model VARCHAR(50)"))
    if "image_url" not in existing_columns:
        connection.execute(text("ALTER TABLE cars ADD COLUMN image_url VARCHAR(255)"))
    if "image_urls" not in existing_columns:
        connection.execute(text("ALTER TABLE cars ADD COLUMN image_urls VARCHAR(1000)"))
    if "phone_number" not in existing_columns:
        connection.execute(text("ALTER TABLE cars ADD COLUMN phone_number VARCHAR(20)"))
    if "available" not in existing_columns:
        connection.execute(text("ALTER TABLE cars ADD COLUMN available VARCHAR(20) NOT NULL DEFAULT 'Kiralık'"))
    if "weekly_price" not in existing_columns:
        connection.execute(text("ALTER TABLE cars ADD COLUMN weekly_price INTEGER"))
    if "monthly_price" not in existing_columns:
        connection.execute(text("ALTER TABLE cars ADD COLUMN monthly_price INTEGER"))


sample_cars = [
    {
        "owner_username": "serkan", "brand": "Fiat", "model": "Egea", "city": "İstanbul", "district": "Bakırköy",
        "price": 850, "weekly_price": 5100, "monthly_price": 16800, "year": 2021, "fuel_type": "Dizel",
        "transmission": "Manuel", "km": 54000, "body_type": "Sedan", "power_range": "76 - 100 HP", "engine_size": "1301 - 1600 cm3",
        "drive_type": "Önden Çekiş", "color": "Beyaz", "warranty": "Hayır", "heavy_damage": "Hayır", "seller_type": "Sahibinden",
        "image_url": "/static/images/egea1.jpg",
        "image_urls": "/static/images/egea1.jpg|/static/images/egea2.jpg|/static/images/egea3.webp", 
        "phone_number": "0532 111 22 33", "available": "Kiralık", "description": "Ekonomik yakıtlı Fiat Egea. Şehir içi ve uzun yol için ideal."
    },
    {
        "owner_username": "ayse", "brand": "Renault", "model": "Clio", "city": "Ankara", "district": "Çankaya",
        "price": 780, "weekly_price": 4680, "monthly_price": 15500, "year": 2020, "fuel_type": "Benzinli",
        "transmission": "Otomatik", "km": 62000, "body_type": "Hatchback 5 kapı", "power_range": "76 - 100 HP", "engine_size": "1300 cm3' e kadar",
        "drive_type": "Önden Çekiş", "color": "Beyaz", "warranty": "Hayır", "heavy_damage": "Hayır", "seller_type": "Sahibinden",
       
        "image_url": "/static/images/clio1.png",
        "image_urls": "/static/images/clio1.png|/static/images/clio2.png|/static/images/clio3.png",
        "phone_number": "0532 222 33 44", "available": "Kiralık", "description": "Renault Clio otomatik vites, az yakar, parkı kolaydır."
    },
    {
        "owner_username": "mehmet", "brand": "Renault", "model": "Megane", "city": "İzmir", "district": "Güzelyalı",
        "price": 1100, "weekly_price": 6600, "monthly_price": 22000, "year": 2022, "fuel_type": "Dizel",
        "transmission": "Otomatik", "km": 36000, "body_type": "Sedan", "power_range": "101 - 125 HP", "engine_size": "1301 - 1600 cm3",
        "drive_type": "Önden Çekiş", "color": "Beyaz", "warranty": "Evet", "heavy_damage": "Hayır", "seller_type": "Kurumdan",
       
        "image_url": "/static/images/megane1.png",
        "image_urls": "/static/images/megane1.png|/static/images/megane2.png|/static/images/megane3.png",
        "phone_number": "0532 333 44 55", "available": "Kiralık", "description": "Konforlu aile aracı Renault Megane. Geniş bagaj hacmi."
    },
    {
        "owner_username": "burak", "brand": "Dacia", "model": "Duster", "city": "Antalya", "district": "Konyaaltı",
        "price": 1300, "weekly_price": 7800, "monthly_price": 25000, "year": 2021, "fuel_type": "Dizel",
        "transmission": "Manuel", "km": 42000, "body_type": "SUV", "power_range": "101 - 125 HP", "engine_size": "1301 - 1600 cm3",
        "drive_type": "4WD (Sürekli)", "color": "Beyaz", "warranty": "Hayır", "heavy_damage": "Hayır", "seller_type": "Sahibinden",
        
        "image_url": "/static/images/dacia1.png",
        "image_urls": "/static/images/dacia1.png|/static/images/dacia2.png|/static/images/dacia3.png",
        "phone_number": "0532 444 55 66", "available": "Kiralık", "description": "Dacia Duster SUV, dağ yolları ve kamp rotaları için uygun."
    },
    {
        "owner_username": "can", "brand": "Volkswagen", "model": "Polo", "city": "İstanbul", "district": "Kadıköy",
        "price": 950, "weekly_price": 5700, "monthly_price": 19000, "year": 2021, "fuel_type": "Benzinli",
        "transmission": "Otomatik", "km": 45000, "body_type": "Hatchback 5 kapı", "power_range": "76 - 100 HP", "engine_size": "1300 cm3' e kadar",
        "drive_type": "Önden Çekiş", "color": "Beyaz", "warranty": "Hayır", "heavy_damage": "Hayır", "seller_type": "Sahibinden",
       
        "image_url": "/static/images/polo1.png",
        "image_urls": "/static/images/polo1.png|/static/images/polo2.png|/static/images/polo3.png",
        "phone_number": "0533 999 88 77", "available": "Kiralık", "description": "Volkswagen Polo DSG şanzıman. Alman konforu."
    },
    {
        "owner_username": "aylin", "brand": "Toyota", "model": "Corolla", "city": "Adana", "district": "Seyhan",
        "price": 1050, "weekly_price": 6300, "monthly_price": 20000, "year": 2020, "fuel_type": "Hibrit",
        "transmission": "Otomatik", "km": 48000, "body_type": "Sedan", "power_range": "101 - 125 HP", "engine_size": "1601 - 1800 cm3",
        "drive_type": "Önden Çekiş", "color": "Beyaz", "warranty": "Hayır", "heavy_damage": "Hayır", "seller_type": "Sahibinden",
        
        "image_url": "/static/images/toyota1.png",
        "image_urls": "/static/images/toyota1.png|/static/images/toyota2.png|/static/images/toyota3.png",
        "phone_number": "0532 777 88 99", "available": "Kiralık", "description": "Toyota Corolla Hibrit. Şehir içinde çok az yakar ve sessizdir."
    }
]

if __name__ == '__main__':
    db = SessionLocal()
    try:
        db.query(models.Car).delete() 
        db.commit()

        for car_data in sample_cars:
            db.add(models.Car(**car_data)) 

        db.commit()
        print('Çoklu fotoğrafa sahip yeni araçlar başarıyla veritabanına eklendi!')
    except Exception as e:
        db.rollback()
        print('Hata oluştu:', e)
    finally:
        db.close()