from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import User, UserCreate, UserLogin
from ..models import UserDB
from ..security import hash_password, verify_password
from ..auth import create_access_token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from ..auth import create_access_token, SECRET_KEY, ALGORITHM

# This tells FastAPI that the token comes from the /login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 1. Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # 2. Extract the user ID (we saved it as "sub" in the login function)
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # 3. Find the user in the database
    # Note: user_id is a string in the token, but might be an int in DB. Cast if needed.
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    
    if user is None:
        raise credentials_exception
        
    return user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=User)
def read_users_me(current_user: UserDB = Depends(get_current_user)):
    """
    Returns the current logged-in user's details.
    """
    return current_user

@router.post("/create-user", response_model=User)
def create_user(user : UserCreate, db : Session = Depends(get_db)):
    existing_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exist")
    else:
        username = user.username
        hashed_password = hash_password(user.password)
        email = user.email
        db_user = UserDB(username = username,
                        hashed_password = hashed_password,
                        email = email)
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
@router.post("/login")
def login(form_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == form_data.username).first()
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token({"sub": str(db_user.id)})
    return {
        "access_token" : access_token,
        "token_type" : "bearer"

    }

