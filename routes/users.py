from fastapi import FastAPI
from fastapi import APIRouter

from database import get_db
from sqlalchemy.orm import Session

userrouter = APIRouter()

@userrouter.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users