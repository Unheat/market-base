import os
from dotenv import load_dotenv# 1. Import the 'on switch'

load_dotenv() # 2. Run the 'on switch' to load the .env file

class Settings:
    # 3. Use the 'grabber' function to get these from your .env
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256") # The second part is a "default"
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()