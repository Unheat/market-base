from pwdlib import PasswordHash
from config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

pwd_context = PasswordHash.recommended()