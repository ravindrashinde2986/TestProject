from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends, Header
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . schemas import TokenData
from .database import get_db
from . models import User as UserModel
import time

ALGORITHM = "HS256"
SECRET = "Super Secret key"
EXPIRATION_TIME = 30


def create_access_token(data: dict):
    token_data = data.copy()
    expiration_time = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME)
    token_data.update({"exp": expiration_time})
    encoded_jwt = jwt.encode(token_data, SECRET, ALGORITHM)
    return encoded_jwt


def validate_access_token(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        exp_time = payload.get('exp')
        if not user_id or not exp_time:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        token_data = TokenData(id=user_id)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired")
    except JWTError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return token_data


def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="login")), db: Session = Depends(get_db)):
    token_data = validate_access_token(token)
    user = db.query(UserModel).filter(UserModel.id == token_data.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


