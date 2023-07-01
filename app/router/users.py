from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User as UserModel
from ..schemas import CreateUser, User, UpdateUser
from ..utils import hash_password
from ..oauth2 import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[User])
def get_users(db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    all_users = db.query(UserModel).all()
    return all_users

    # return {"everything is OK"}


@router.get("/{id}", response_model=User, status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exists")
    return user


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = UserModel(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except exc.IntegrityError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with email {user.email} already exists !")

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return new_user


@router.put("/{id}", response_model=User, status_code=status.HTTP_200_OK)
def update_user(id: int, user: UpdateUser, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    try:
        hashed_password = hash_password(user.password)
        user.password = hashed_password

        user_query = db.query(UserModel).filter(UserModel.id == id)
        users_updated = user_query.update(user.dict())
        db.commit()
    except exc.IntegrityError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with email {user.email} already exists !")

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if not users_updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exists")

    return user_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    users_deleted = db.query(UserModel).filter(UserModel.id == id).delete()
    db.commit()

    if not users_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exists")
