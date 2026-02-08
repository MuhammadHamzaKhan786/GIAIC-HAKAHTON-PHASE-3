from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from datetime import timedelta
from ..database import engine
from ..models.user import User, UserCreate
from .jwt_handler import get_password_hash, verify_password, create_access_token
from typing import Annotated

router = APIRouter()

@router.post("/signup")
def signup(user_create: UserCreate):
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Create new user
        db_user = User(
            email=user_create.email,
            password_hash=get_password_hash(user_create.password)
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": str(db_user.id)}, expires_delta=access_token_expires
        )

        # Return success and token
        return {"success": True, "token": access_token}

@router.post("/signin")
def signin(user_data: UserCreate):
    with Session(engine) as session:
        # Find user by email
        user = session.exec(select(User).where(User.email == user_data.email)).first()

        if not user or not verify_password(user_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        return {"success": True, "token": access_token}

@router.post("/signout")
def signout():
    # In a real application, you might implement token blacklisting here
    # For now, we just return success
    return {"success": True}