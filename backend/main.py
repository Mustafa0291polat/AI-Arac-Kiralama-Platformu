from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import or_
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pathlib import Path
import shutil, uuid, os
from backend import models, schemas, database, ai_filter


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AI Araç Kiralama API")
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.get("/kayit", response_class=FileResponse)
def get_register_page(): return FileResponse("backend/static/register.html")

@app.get("/giris", response_class=FileResponse)
def get_login_page(): return FileResponse("backend/static/login.html")

@app.post("/api/register/", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kayıtlı.")
    new_user = models.User(first_name=user.first_name, last_name=user.last_name, email=user.email, phone_number=user.phone_number, age=user.age, hashed_password=pwd_context.hash(user.password))
    db.add(new_user); db.commit(); db.refresh(new_user)
    return new_user


@app.get("/", response_class=HTMLResponse)
def read_index(): return Path("backend/static/index.html").read_text(encoding="utf-8")

@app.get("/cars/", response_model=List[schemas.CarOut])
def list_cars(db: Session = Depends(database.get_db)):
    return db.query(models.Car).filter(models.Car.available == "Kiralık").all()

@app.post("/cars/", response_model=schemas.CarOut)
def create_car(car: schemas.CarCreate, db: Session = Depends(database.get_db)):
    db_car = models.Car(**car.dict())
    db.add(db_car); db.commit(); db.refresh(db_car)
    return db_car


@app.post("/filter/prompt", response_model=schemas.PromptResponse)
def filter_by_prompt(request: schemas.FilterRequest, db: Session = Depends(database.get_db)):
    try:
        parsed_filter = ai_filter.prompt_to_filter(request.prompt)
        matched_cars = build_car_query(db, parsed_filter)
        return {"parsed_filter": parsed_filter, "matched_cars": matched_cars}
    except Exception as e:
        print("Hata detayı:", e)
        raise HTTPException(status_code=500, detail=str(e))

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
    if filters.get("city"): query = query.filter(models.Car.city.ilike(f"%{filters['city']}%"))
    if filters.get("brand"): query = query.filter(models.Car.brand.ilike(f"%{filters['brand']}%"))
    if filters.get("model"): query = query.filter(models.Car.model.ilike(f"%{filters['model']}%"))
    if filters.get("fuel_type"): query = query.filter(models.Car.fuel_type.ilike(f"%{filters['fuel_type']}%"))
    
    return query.all()