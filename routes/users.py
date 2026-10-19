from fastapi import Depends, FastAPI, HTTPException
from fastapi import APIRouter

from database import get_db
from sqlalchemy.orm import Session
from models import User
from schemas.users import UserRegisterSchema, UserSchema, UserResponseSchema,LoginSchema, UserCreateSchema, UserUpdateSchema
from utilities import hash_password, verify_password, get_current_user,create_access_token, create_refresh_token

userrouter = APIRouter(prefix="/users", tags=["users"] )



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

    access_token = create_access_token(data={"user_id": db_user.id, "type": "access"})
    refresh_token = create_refresh_token(data={"user_id": db_user.id, "type": "refresh"})

    
    return {"message": "Login successful", "access_token": access_token, "refresh_token": refresh_token}


@userrouter.get("/update-user", response_model=UserResponseSchema)
def update_user(user_update: UserUpdateSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.username = user_update.name
    db_user.email = user_update.email
    if user_update.password:
        db_user.password = hash_password(user_update.password)

    db.commit()
    db.refresh(db_user)
    return {"user": [db_user]}