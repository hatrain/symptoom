# user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import User, UserCreate
from database import get_db


router = APIRouter()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    from auth import pwd_context
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, 
                   email=user.email, 
                   name=user.name, 
                   hashed_password=hashed_password, 
                   family_history=user.family_history, 
                   medications=user.medications,
                    phone_number=user.phone_number
                   )
    db.add(db_user)
    db.commit()
    return "complete"

#TODO: modify to include extra fields
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)