from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# This class = One Table in your Database
class ItemDB(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String, nullable=True)
    
    owner_id = Column(Integer, ForeignKey("users.id")) # this ForeignKey determine this is the childDB
    owner = relationship("UserDB", back_populates="items")
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True) # unique=True means no duplicate emails
    hashed_password = Column(String) # We store the HASH, not the password
    
    items = relationship("ItemDB", back_populates="owner")