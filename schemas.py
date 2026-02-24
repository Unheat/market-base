# 3. Pydantic Model (Data Validation - what the USER sends)
from pydantic import BaseModel
class ItemCreate(BaseModel):
    name: str
    price: float
    description: str = None
    
class UserCreate(BaseModel):
    email: str
    password: str