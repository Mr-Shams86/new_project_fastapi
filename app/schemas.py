from pydantic import BaseModel
from pydantic import HttpUrl
from typing import List
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    image_url: HttpUrl
    
class PostCreate(PostBase):
    pass    

class Post(PostBase):
    id: int
    author_id: int
    
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    posts: List[Post] = []
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Optional[str] = None  
            