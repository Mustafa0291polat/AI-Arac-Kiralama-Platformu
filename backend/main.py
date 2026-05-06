from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import models, schemas, database

# Veritabanı tablolarını otomatik oluştur
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AI Araç Kiralama API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Geliştirme aşamasında her yerden gelen isteklere izin ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# bcrypt__ident="2b" ekleyerek kütüphane çakışmasını engelledik
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten alınmış.")
    
    hashed_pwd = get_password_hash(user.password)
    new_user = models.User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_pwd,
        age=user.age
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Kullanıcı başarıyla oluşturuldu", "username": new_user.username}

@app.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre.")
    
    return {"message": "Giriş başarılı", "token": "fake-jwt-token"}