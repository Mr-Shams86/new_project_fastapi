from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)