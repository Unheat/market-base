from pwdlib import PasswordHash
import os
from dotenv import load_dotenv


load_dotenv() # This loads the variables from .env into Python
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = PasswordHash.recommended()