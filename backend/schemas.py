from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    age: int

    @field_validator('username')
    def username_must_not_contain_spaces(cls, v):
        if ' ' in v:
            raise ValueError('Kullanıcı adında boşluk olamaz.')
        return v

    @field_validator('age')
    def check_age_limit(cls, v):
        if v < 18:
            raise ValueError('Kayıt olmak için en az 18 yaşında olmalısınız.')
        if v < 0:
            raise ValueError('Yaş negatif olamaz.')
        return v

class UserLogin(BaseModel):
    username: str
    password: str