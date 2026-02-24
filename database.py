from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# 1. Create the Database URL (This is for SQLite)
# Later, for AWS, we just change this string to a Postgres URL.
SQLALCHEMY_DATABASE_URL = "sqlite:///./market.db"

# 2. Create the Engine (The thing that actually talks to the DB)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a Session (A temporary workspace for DB operations)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create a Base (The blueprint for all our models)
Base = declarative_base()