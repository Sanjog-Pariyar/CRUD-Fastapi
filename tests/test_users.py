from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import pytest
from app.database import get_db, Base


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine, autocommit=False)

@pytest.fixture
def session():

  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)

  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()

@pytest.fixture
def client(session):
  def override_get_db():
    try:
      yield session
    finally:
      session.close()

  app.dependency_overrides[get_db] = override_get_db
  
  yield TestClient(app)


def test_main_read(client):
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == { "message": "Hello World" }


def test_create_user(client):
  res = client.post("/users", json={
    "email": "sanjog@gmail.com",
    "password": "sanjog123"
  })

  new_user = schemas.UserOut(**res.json())

  assert new_user.email == "sanjog@gmail.com"
  assert res.status_code == status.HTTP_201_CREATED