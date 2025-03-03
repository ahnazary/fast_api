from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from postgres_interface import get_db
from security import create_access_token, hash_password, verify_password
from sqlalchemy.orm import Session

router = APIRouter()

# Dummy admin credentials, in real world, this should be stored in a database
users_db = {
    "admin": {"username": "admin", "hashed_password": hash_password("admin123")}
}


@router.post("/token")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=timedelta(weeks=100)
    )
    return {"access_token": access_token, "token_type": "bearer"}
