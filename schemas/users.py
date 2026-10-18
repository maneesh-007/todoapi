from pydantic import BaseModel, EmailStr
from typing import List

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserSchema(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserUpdateSchema(BaseModel):
    name: str | None = None
    password: str | None = None

class UserResponseSchema(BaseModel):

    user: List[UserSchema]

class UserRegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str   