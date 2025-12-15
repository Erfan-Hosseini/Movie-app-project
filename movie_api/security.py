from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .database import get_db
from .models import UserDB
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
pwd_context = CryptContext(schemes= ["bcrypt"], deprecated = "auto")

def hash_password(password : str):
    hashed_password = pwd_context.hash(password)
    return hashed_password

def verify_password(plain : str, stored_hashed_password : str):
    password = pwd_context.verify(plain, stored_hashed_password)
    return password

def get_current_user(token: str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    try:
     
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id : int = payload.get("sub")
    except JWTError as e:
        print(f"JWT Verification Error: {e}")
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
  
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


SECRET_KEY = "super_long_and_boring_useless_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
