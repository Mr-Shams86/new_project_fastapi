import os
from typing import Annotated
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from . import crud
from . import models
from . import schemas
from .database import SessionLocal
from .database import engine
from .security import create_access_token
from .security import verify_password
from .security import decode_access_token


models.Base.metadata.create_all(bind=engine)

load_dotenv()

database_url = os.getenv("DATABASE_URL")

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_UNAUTHORIZED, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"www-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# @app.get("/users/me", response_model=schemas.User)
# #def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     #token_data = decode_access_token(token)
# def read_users_me(authorization: str | None = Header(default=None), db: Session=Depends(get_db)):
#     authorization = authorization.split(' ')[1]
#     token_data = decode_access_token(authorization)    
#     if token_data is None:
#         raise HTTPException(status_code=401, detail="Invalid authentication credentials")
#     user = crud.get_user_by_username(db, username=token_data.username)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user        

@app.get("/users/me", response_model=schemas.User)
def read_users_me(authorization: str = Header(None), db: Session = Depends(get_db)):
    if authorization is None or ' ' not in authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header format")
    
    try:
        token = authorization.split(' ')[1]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid format of Authorization header")
    
    token_data = decode_access_token(token)
    if token_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user


# @app.get("/users/me", response_model=schemas.User)
# def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     token_data = decode_access_token(token)
#     if token_data is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    
#     user = crud.get_user_by_username(db, username=token_data.username)
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
#     return user