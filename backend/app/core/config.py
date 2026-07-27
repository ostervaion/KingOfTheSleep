from pathlib import Path

from pwdlib import PasswordHash

DATABASE_URL = "postgresql+psycopg2://appuser:apppassword@db:5432/appdb"
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600
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

