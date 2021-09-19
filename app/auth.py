from app.db import EMPTY_USER
import os

from passlib.context import CryptContext
from jose import jwt

from . import db

APP_SECRET_KEY = os.environ.get("APP_SECRET_KEY", "DefaultPassword")
crypt_context = CryptContext(schemes=["bcrypt"])


def is_auth_user(email, password):
    try:
        return crypt_context.verify(password, db.get_user(email).password)
    except:
        return False


def get_jwt_token_from_email(email: str) -> str:
    return jwt.encode({"email": email}, APP_SECRET_KEY)


def get_hashed_password(password: str) -> str:
    return crypt_context.hash(password)


def get_user_from_jwt_token(token: str) -> db.User:
    try:
        return db.get_user(jwt.decode(token, APP_SECRET_KEY)["email"])
    except Exception as e:
        return db.EMPTY_USER


def is_valid_user(email: str, password: str):
    if is_auth_user(email, password):
        return True
    elif db.get_user(email).id == db.EMPTY_USER.id:
        db.set_user(db.User(email=email, password=get_hashed_password(password)))
        return True
    else:
        return False
