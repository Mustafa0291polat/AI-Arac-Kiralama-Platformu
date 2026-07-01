from typing import List, Optional
from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str  # @gmail.com kısıtlaması için özel kontrol yazacağız
    phone_number: str
    age: int
    password: str

    @field_validator('first_name', 'last_name')
    @classmethod
    def check_names(cls, v):
        if ' ' in v:
            raise ValueError('İsim ve soyisimde boşluk bırakılamaz.')
        if len(v) > 30:
            raise ValueError('İsim ve soyisim 30 karakterden uzun olamaz.')
        return v

    @field_validator('email')
    @classmethod
    def check_email(cls, v):
        if ' ' in v:
            raise ValueError('E-posta adresinde boşluk bırakılamaz.')
        if len(v) > 50:
            raise ValueError('E-posta adresi 50 karakterden uzun olamaz.')
        if not v.endswith('@gmail.com'):
            raise ValueError('Sadece @gmail.com uzantılı mail adresleri ile kayıt olabilirsiniz.')
        return v
    @field_validator('password')
    @classmethod
    def check_password(cls, v):
        if len(v) < 8:
            raise ValueError('Şifre en az 8 karakter olmalıdır.')
        if len(v) > 20:
            raise ValueError('Şifre 20 karakterden uzun olamaz.')
        return v

    @field_validator('age')
    @classmethod
    def check_age_limit(cls, v):
        if v < 18:
            raise ValueError('Kayıt olmak için en az 18 yaşında olmalısınız.')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    class Config:
        from_attributes = True

class CarBase(BaseModel):
    owner_username: str
    brand: str
    model: str
    city: str
    district: Optional[str] = None
    price: int
    weekly_price: Optional[int] = None
    monthly_price: Optional[int] = None
    year: int
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    km: Optional[int] = None
    body_type: Optional[str] = None
    power_range: Optional[str] = None
    engine_size: Optional[str] = None
    drive_type: Optional[str] = None
    color: Optional[str] = None
    warranty: Optional[str] = None
    heavy_damage: Optional[str] = None
    seller_type: Optional[str] = None
    image_url: Optional[str] = None
    image_urls: Optional[str] = None
    phone_number: Optional[str] = None
    available: Optional[str] = "Kiralık"
    description: Optional[str] = None

class CarCreate(CarBase):
    pass

class CarOut(CarBase):
    id: int
    class Config:
        from_attributes = True

class FilterRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    parsed_filter: dict
    matched_cars: List[CarOut]