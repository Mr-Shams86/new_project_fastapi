from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    
    
class UserCreate(UserBase):
    password: str
    
class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True
        
        
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Optional[str] = None                   