# from fastapi import FastAPI
# from pydantic import BaseModel
# app = FastAPI()
# db = []

# @app.get("/")
# def home():
#     return {"message": "I am learning Backend"}
# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: bool = None
    
# @app.post("/items")
# def create_item(item: Item): # The Bouncer checks "item" here
#     item_dict = item.model_dump()
#     db.append(item_dict)
#     return {"message": "Item created", "item_name": item.name, "price": item.price}

# @app.get("/items")
# def get_items():
#     # Show everything in the list
#     return {"items": db}
# @app.get("/all-items")
# def get_all_items():
#     return {"items": db}

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas, security, dependencies
from database import engine
from datetime import datetime, timezone
from jose import jwt
from datetime import datetime, timedelta
# 1. Create the Database Tables (Run the migration)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# API
## items API
@app.post("/items/")
def create_item(item: schemas.ItemCreate, db: Session = Depends(dependencies.get_db), current_user: str = Depends(dependencies.get_current_user)):
    # Create the DB object
    db_item = models.ItemDB(name=item.name, price=item.price, description=item.description)
    # Add to the "staging area"
    db.add(db_item)
    # Commit (Save to file)
    db.commit()
    # Refresh (Get the ID that was just generated)
    db.refresh(db_item)
    return db_item

@app.get("/items/")
def read_items(db: Session = Depends(dependencies.get_db)):
    # SQL translation: "SELECT * FROM items"
    items = db.query(models.ItemDB).all()
    return items

## users API
@app.post("/register/")
def register_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    # check if then username existed
    existing_user = db.query(models.UserDB).filter(models.UserDB.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # 1. Hash the password
    hashed_pwd = security.pwd_context.hash(user.password)
    
    # 2. Create the Database object (Notice we use hashed_pwd, NOT user.password)
    db_user = models.UserDB(email=user.email, hashed_password=hashed_pwd)
    
    # 3. Save it
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # 4. Return success (NEVER return the password to the user)
    return {"message": "User created successfully!", "user_email": db_user.email}

## debug users API
@app.get("/debug-users")
def get_users_debug(db: Session = Depends(dependencies.get_db)):
    users = db.query(models.UserDB).all()
    return users

@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    # 1. Find the user by email
    db_user = db.query(models.UserDB).filter(models.UserDB.email == user.email).first()
    
    # 2. Check if user exists AND if password is correct
    if not db_user or not security.pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # 3. Create the "Digital Passport" (Token)
    # We set it to expire in 300 minutes for security
    access_token_expires = timedelta(minutes=300)
    expire = datetime.now(timezone.utc) + access_token_expires
    
    data_to_encode = {"sub": db_user.email, "exp": expire}
    encoded_jwt = jwt.encode(data_to_encode, security.SECRET_KEY, algorithm=security.ALGORITHM)

    return {"access_token": encoded_jwt, "token_type": "bearer"}



