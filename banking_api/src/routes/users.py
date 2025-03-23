from fastapi import APIRouter, Depends, HTTPException, status
from postgres_interface import get_db
from postgres_models import Users
from pydantic_models import UsersCreate
from security import get_current_user, hash_password
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/create/")
def create_new_user(
    user: UsersCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """
    Route for creating a new user
    Only the admin user can create a new user
    """
    if current_user != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin can create a new user",
        )
    new_user = Users(
        username=user.username, hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"username": new_user.username}
