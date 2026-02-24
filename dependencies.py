from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
import os
from database import SessionLocal
import security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# 2. Dependency: Get a database session for each request
def get_db():
    db = SessionLocal() # this bind to database.py 
    try:
        yield db
    finally:
        db.close()
        
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
        return email
    except:
        raise HTTPException(status_code=401, detail="Invalid Token")
