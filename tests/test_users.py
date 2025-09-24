from .database import client, session
from app import schemas
from fastapi import status
from app.config import settings
import jwt
import pytest

def test_main_read(client):
	response = client.get("/")
	assert response.status_code == 200
	assert response.json() == { "message": "posts api" }

@pytest.fixture
def test_user(client):
    user_data = {"email": "sanjog112@gmail.com", "password": "sanjog123"}
    res = client.post('/users', json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


def test_create_user(client):
	res = client.post("/users", json={
		"email": "sanjog@gmail.com",
		"password": "sanjog123"
	})

	new_user = schemas.UserOut(**res.json())

	assert new_user.email == "sanjog@gmail.com"
	assert res.status_code == status.HTTP_201_CREATED


def test_login_user(client, test_user):
    res = client.post("/auth/login", json={
        "email": test_user["email"],
		"password": test_user["password"]
    })

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    email: str = payload.get("user_email")
    user_id: int = payload.get("user_id")

    assert res.status_code == 200
    assert email == test_user["email"]
    assert user_id == test_user["id"]


# def test_incorrect_login(test_user, client):
#     res = client.post("/auth/login", json={
#         "email": test_user["email"],
# 		"password": "wrongpassword"
#     })
#     print(res.json())
    # assert res.status_code == 403
    # assert res.json().get("detail") == "Invalid Credentials"