from typing import Optional
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Optional
from jose import JWTError, jwt
from .schemas import TokenData


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class JWTService:

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        print(f"Verifying password: {plain_password} against hash: {hashed_password}")
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> Optional[TokenData]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            print(f"Decoded payload: {payload}")
            username: str = payload.get("sub")
            if username is None:
                return None
            return TokenData(username=username)
        except JWTError as e:
            print(f"JWT