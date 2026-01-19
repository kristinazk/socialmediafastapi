from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user_input: schemas.UserCreate, db: Session = Depends(get_db)):
    print(user_input.password)
    # hash password
    hashed_password = utils.hash_pass(user_input.password)
    user_input.password = hashed_password

    new_user = models.User(**user_input.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    all_users = db.query(models.User).all()

    return all_users

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")

    return user