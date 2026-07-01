from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import or_
from sqlalchemy.orm import Session
from pathlib import Path
import bcrypt
import shutil, uuid, os
from backend import models, schemas, database, ai_filter


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AI Araç Kiralama API")
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# bcrypt en fazla 72 baytlık şifre kabul eder; daha uzununu keseriz
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8")[:72], bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8")[:72], hashed.encode("utf-8"))
    except ValueError:
        return False


@app.get("/kayit", response_class=FileResponse)
def get_register_page(): return FileResponse("backend/static/register.html")

@app.get("/giris", response_class=FileResponse)
def get_login_page(): return FileResponse("backend/static/login.html")

@app.post("/api/register/", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kayıtlı.")
    
    hashed_pw = hash_password(user.password)

    new_user = models.User(
        first_name=user.first_name, 
        last_name=user.last_name, 
        email=user.email, 
        phone_number=user.phone_number, 
        age=user.age, 
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# main.py dosyasında, register fonksiyonunun hemen altına bunu ekle:

@app.post("/api/login/")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    # 1. Kullanıcıyı e-posta adresinden bul
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    # 2. Kullanıcı yoksa veya şifre eşleşmiyorsa hata ver
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="E-posta veya şifre hatalı. Lütfen tekrar deneyin.")
    
    # 3. Giriş başarılıysa kullanıcı bilgilerini frontend'e (localStorage) gönder
    return {
        "message": "Giriş başarılı", 
        "user": {
            "first_name": user.first_name, 
            "last_name": user.last_name,
            "email": user.email
        }
    }

@app.get("/", response_class=HTMLResponse)
def read_index(): return Path("backend/static/index.html").read_text(encoding="utf-8")

@app.get("/cars/", response_model=List[schemas.CarOut])
def list_cars(db: Session = Depends(database.get_db)):
    return db.query(models.Car).filter(models.Car.available == "Kiralık").all()

@app.post("/cars/", response_model=schemas.CarOut)
def create_car(car: schemas.CarCreate, db: Session = Depends(database.get_db)):
    db_car = models.Car(**car.model_dump())
    db.add(db_car); db.commit(); db.refresh(db_car)
    return db_car


@app.post("/filter/prompt", response_model=schemas.PromptResponse)
def filter_by_prompt(request: schemas.FilterRequest, db: Session = Depends(database.get_db)):
    try:
        parsed_filter = ai_filter.prompt_to_filter(request.prompt)
    except RuntimeError as e:
        print("AI filtre hatası:", e)
        raise HTTPException(status_code=503, detail="Akıllı arama şu anda kullanılamıyor. Lütfen daha sonra tekrar deneyin veya 'Tümünü Göster' ile ilanlara göz atın.")
    matched_cars = build_car_query(db, parsed_filter)
    return {"parsed_filter": parsed_filter, "matched_cars": matched_cars}

@app.post("/upload-images/")
async def upload_images(files: List[UploadFile] = File(...)):
    saved_urls = []
    os.makedirs("backend/static/images", exist_ok=True)
    for file in files:
        file_name = f"{uuid.uuid4().hex}.{file.filename.split('.')[-1]}"
        with open(f"backend/static/images/{file_name}", "wb") as buffer: shutil.copyfileobj(file.file, buffer)
        saved_urls.append(f"/static/images/{file_name}")
    return {"urls": saved_urls}


def build_car_query(db: Session, filters: dict):
    query = db.query(models.Car).filter(models.Car.available == "Kiralık")
    
    # Metin aramaları (ilike ile içinde geçiyorsa bul)
    if filters.get("city"):
        query = query.filter(models.Car.city.ilike(f"%{filters['city']}%"))
    if filters.get("district"):
        query = query.filter(models.Car.district.ilike(f"%{filters['district']}%"))
    if filters.get("brand"):
        query = query.filter(models.Car.brand.ilike(f"%{filters['brand']}%"))
    if filters.get("model"):
        query = query.filter(models.Car.model.ilike(f"%{filters['model']}%"))
        
    # Liste aramaları (in_ ile AI'dan gelen listeyi eşleştir)
    if filters.get("fuel_type"): 
        query = query.filter(models.Car.fuel_type.in_(filters["fuel_type"]))
    if filters.get("transmission"): 
        query = query.filter(models.Car.transmission.in_(filters["transmission"]))
    if filters.get("body_type"): 
        query = query.filter(models.Car.body_type.in_(filters["body_type"]))
    if filters.get("color"): 
        query = query.filter(models.Car.color.in_(filters["color"]))
        
    # Fiyat filtreleri (AI fiyat sınırı koyduysa uygula)
    if filters.get("price_min") and filters["price_min"] > 0:
        query = query.filter(models.Car.price >= filters["price_min"])
    if filters.get("price_max") and filters["price_max"] < 10000000:
        query = query.filter(models.Car.price <= filters["price_max"])

    # Yıl filtreleri (AI model yılı sınırı koyduysa uygula)
    if filters.get("year_min") and filters["year_min"] > 1970:
        query = query.filter(models.Car.year >= filters["year_min"])
    if filters.get("year_max") and filters["year_max"] < 2030:
        query = query.filter(models.Car.year <= filters["year_max"])

    # Kilometre filtreleri (AI km sınırı koyduysa uygula)
    if filters.get("km_min") and filters["km_min"] > 0:
        query = query.filter(models.Car.km >= filters["km_min"])
    if filters.get("km_max") and filters["km_max"] < 9999999:
        query = query.filter(models.Car.km <= filters["km_max"])

    return query.all()