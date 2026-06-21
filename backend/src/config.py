from pwdlib import PasswordHash

DATABASE_URL = "postgresql+psycopg2://appuser:apppassword@db:5432/appdb"
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ORIGINS = [
    "http://localhost:5173",
    "https://b5f7dz71-5173.uks1.devtunnels.ms",
	"*"
	
]
password_hash = PasswordHash.recommended()

