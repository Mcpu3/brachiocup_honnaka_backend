import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.v1 import cruds, models, schemas
from api.v1.dependencies import get_database, get_current_user


api_router = APIRouter(tags=["Users"])

@api_router.post("/signup")
def signup(request: schemas.users.Signup, database: Session=Depends(get_database)):
    user = cruds.users.read_user(database, username=request.usernane)
    if user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    user = cruds.users.create_user(database, request)
    if not user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    return status.HTTP_201_CREATED

@api_router.post("/signin", response_model=schemas.users.Token)
def signin(request: OAuth2PasswordRequestForm=Depends(), database: Session=Depends(get_database)) -> schemas.users.Token:
    user = cruds.users.read_user(database, username=request.username)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if not CryptContext(["bcrypt"]).verify(request.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    token = schemas.users.Token(
        access_token = jwt.encode({"sub": request.username}, os.getenv("SECRET_KEY"), "HS256")
    )

    return token

@api_router.get("/me", response_model=schemas.users.User)
def get_me(current_user: models.User=Depends(get_current_user)) -> schemas.users.User:
    return current_user
