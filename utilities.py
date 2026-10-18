from pwdlib import PasswordHash
import jwt
from fastapi.security import HttpBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status

# Password hashing

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)





SECRET_KEY = "ARnWTBfL9v8j0gYtfssLGFceiZZX3xjjw"
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7




