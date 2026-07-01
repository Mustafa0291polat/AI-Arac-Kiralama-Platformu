"""API testleri.

Gerçek veritabanına dokunmamak için testler bellek içi (in-memory) SQLite kullanır.
Yapay zeka filtresi testi, OpenAI'ye bağımlı olmamak için mock'lanır.

Çalıştırma (proje kökünden):
    python -m pytest backend/test_main.py -v
"""
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend import models, database, ai_filter
from backend.main import app

# --- Test veritabanı kurulumu ---
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
models.Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[database.get_db] = override_get_db
client = TestClient(app)


def make_user(**overrides):
    user = {
        "first_name": "Deneme",
        "last_name": "Kullanici",
        "email": "deneme@gmail.com",
        "phone_number": "05321112233",
        "age": 25,
        "password": "sifre1234",
    }
    user.update(overrides)
    return user


def make_car(**overrides):
    car = {
        "owner_username": "test_sahibi",
        "brand": "Fiat",
        "model": "Egea",
        "city": "İstanbul",
        "price": 900,
        "year": 2021,
        "fuel_type": "Dizel",
        "transmission": "Manuel",
        "body_type": "Sedan",
        "available": "Kiralık",
    }
    car.update(overrides)
    return car


# --- Kayıt testleri ---

def test_register_success():
    response = client.post("/api/register/", json=make_user(email="basarili@gmail.com"))
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "basarili@gmail.com"
    assert data["first_name"] == "Deneme"
    assert "id" in data


def test_register_duplicate_email():
    payload = make_user(email="tekrar@gmail.com")
    assert client.post("/api/register/", json=payload).status_code == 200
    response = client.post("/api/register/", json=payload)
    assert response.status_code == 400
    assert "zaten kayıtlı" in response.json()["detail"]


def test_register_underage():
    response = client.post("/api/register/", json=make_user(email="genc@gmail.com", age=15))
    assert response.status_code == 422


def test_register_name_with_space():
    response = client.post("/api/register/", json=make_user(email="bosluk@gmail.com", first_name="Ad Soyad"))
    assert response.status_code == 422


def test_register_non_gmail():
    response = client.post("/api/register/", json=make_user(email="kisi@hotmail.com"))
    assert response.status_code == 422


def test_register_short_password():
    response = client.post("/api/register/", json=make_user(email="kisa@gmail.com", password="123"))
    assert response.status_code == 422


# --- Giriş testleri ---

def test_login_success():
    client.post("/api/register/", json=make_user(email="giris@gmail.com", password="dogrusifre1"))
    response = client.post("/api/login/", json={"email": "giris@gmail.com", "password": "dogrusifre1"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Giriş başarılı"
    assert data["user"]["email"] == "giris@gmail.com"


def test_login_wrong_password():
    client.post("/api/register/", json=make_user(email="yanlis@gmail.com", password="dogrusifre1"))
    response = client.post("/api/login/", json={"email": "yanlis@gmail.com", "password": "yanlissifre"})
    assert response.status_code == 401


def test_login_unknown_email():
    response = client.post("/api/login/", json={"email": "yok@gmail.com", "password": "birsifre123"})
    assert response.status_code == 401


# --- Araç ilanı testleri ---

def test_create_and_list_car():
    response = client.post("/cars/", json=make_car(brand="Renault", model="TestClio"))
    assert response.status_code == 200
    created = response.json()
    assert created["brand"] == "Renault"

    response = client.get("/cars/")
    assert response.status_code == 200
    models_listed = [car["model"] for car in response.json()]
    assert "TestClio" in models_listed


def test_list_cars_hides_unavailable():
    client.post("/cars/", json=make_car(model="GizliArac", available="Kiralandı"))
    response = client.get("/cars/")
    assert response.status_code == 200
    models_listed = [car["model"] for car in response.json()]
    assert "GizliArac" not in models_listed


# --- Yapay zeka filtre testleri (OpenAI mock'lanır) ---

def test_filter_prompt_with_mock(monkeypatch):
    client.post("/cars/", json=make_car(model="FiltreSUV", city="Antalya", body_type="SUV"))
    client.post("/cars/", json=make_car(model="FiltreSedan", city="Antalya", body_type="Sedan"))

    def fake_prompt_to_filter(prompt):
        parsed = dict(ai_filter.DEFAULT_FILTER)
        parsed.update({"city": "Antalya", "body_type": ["SUV"]})
        return parsed

    monkeypatch.setattr(ai_filter, "prompt_to_filter", fake_prompt_to_filter)

    response = client.post("/filter/prompt", json={"prompt": "Antalya'da arazi aracı lazım"})
    assert response.status_code == 200
    data = response.json()
    assert data["parsed_filter"]["city"] == "Antalya"
    models_matched = [car["model"] for car in data["matched_cars"]]
    assert "FiltreSUV" in models_matched
    assert "FiltreSedan" not in models_matched


def test_filter_prompt_ai_unavailable(monkeypatch):
    def broken_prompt_to_filter(prompt):
        raise RuntimeError("OPENAI_API_KEY bulunamadı")

    monkeypatch.setattr(ai_filter, "prompt_to_filter", broken_prompt_to_filter)

    response = client.post("/filter/prompt", json={"prompt": "herhangi bir araç"})
    assert response.status_code == 503
    assert "Akıllı arama" in response.json()["detail"]
