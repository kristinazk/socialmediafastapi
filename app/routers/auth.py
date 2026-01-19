from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database
from ..models import User
from ..utils import verify_pass
from ..oauth2 import create_access_token
from ..schemas import Token

router = APIRouter(tags=['Authentification'])

@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials.")

    if not verify_pass(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials.")

    # create a token
    access_token = create_access_token(data = {"user_id": user.id}) # payload

    return {"access_token" : access_token, "token_type" : "bearer"}