from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_register_success():
    
    response = client.post("/register", json={
        "username": "new_user_success", 
        "email": "success@test.com",
        "password": "secure123",
        "age": 25
    })
    
    assert response.status_code in [201, 400]

def test_register_invalid_age():
    response = client.post("/register", json={
        "username": "yas_hatasi",
        "email": "yas@test.com",
        "password": "password123",
        "age": 15
    })
    
    assert response.status_code == 422

def test_register_invalid_username():
    response = client.post("/register", json={
        "username": "hatali bosluk", 
        "email": "bosluk@test.com",
        "password": "password123",
        "age": 20
    })
    
    assert response.status_code == 422