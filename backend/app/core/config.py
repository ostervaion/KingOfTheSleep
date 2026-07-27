import os
from pathlib import Path

from dotenv import load_dotenv
from pwdlib import PasswordHash

# Load variables from .env into os.environ
load_dotenv()

POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB=os.getenv("POSTGRES_DB")
LOG = os.getenv("LOG_VERBOSE")
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ORIGINS = [
    "http://localhost:5173",
    "https://b5f7dz71-5173.uks1.devtunnels.ms",
	"*"
	
]

DAY_NAMES = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
UPLOAD_BASE_DIR = Path(__file__).resolve().parent.parent / "uploads" #maybe is only one parent, it was changed due to file moved to core
AVATAR_DIR = UPLOAD_BASE_DIR / "avatars"
AVATAR_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_SCORE = 70

password_hash = PasswordHash.recommended()

