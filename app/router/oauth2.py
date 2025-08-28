import jwt
from datetime import datetime, timedelta
from .. import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
  to_encode = data.copy()

  expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
  to_encode.update({"exp": expire})

  encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

  return encoded_jwt

def verify_access_token(token: str, credentials_exception):
  try:
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    email: str = payload.get("user_email")
    user_id: int = payload.get("user_id")

    if email is None or user_id is None:
      raise credentials_exception
    token_data = schemas.TokenData(email=email, id=user_id)
  except jwt.PyJWTError:
    raise credentials_exception
  
  return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

  return verify_access_token(token, credentials_exception)
