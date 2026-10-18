from fastapi import Depends, FastAPI, HTTPException
from fastapi import APIRouter

from database import get_db
from sqlalchemy.orm import Session
from models import User
from schemas.users import UserRegisterSchema, UserSchema, UserResponseSchema,LoginSchema, UserCreateSchema, UserUpdateSchema
from utilities import hash_password, verify_password

userrouter = APIRouter(prefix="/users", tags=["users"] )

@userrouter.get("/all", response_model=UserResponseSchema)
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"user": users}

@userrouter.post("/register" , response_model=UserResponseSchema)
def register_user(user: UserRegisterSchema, db: Session = Depends(get_db)):

    db_user = User(username=user.name, email=user.email, password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"user": [db_user]}

@userrouter.post("/login")
def login_user(user: LoginSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {"message": "Login successful"}
