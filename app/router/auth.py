from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils
from . import oauth2

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"])

@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

  if not utils.verify_password(user_credentials.password, user.password):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

  token = oauth2.create_access_token(data={ "user_email": user.email, "user_id": user.id })

  return { "access_token": token, "token_type": "bearer" }