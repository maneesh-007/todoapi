from fastapi import Depends, FastAPI, HTTPException
from fastapi import APIRouter

from database import get_db
from sqlalchemy.orm import Session
from models import User
from schemas.users import UserRegisterSchema, UserSchema, UserResponseSchema,loginSchema, UserCreateSchema, UserUpdateSchema
from utilities import hash_password, verify_password

userrouter = APIRouter(prefix="/users", tags=["users"] )

@userrouter.get("/all", response_model=UserResponseSchema)
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"user": users}

@userrouter.post("/register")
def register_user(user: UserRegisterSchema, db: Session = Depends(get_db)):

    db_user = User(name=user.name, email=user.email, password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"user": [db_user]}
