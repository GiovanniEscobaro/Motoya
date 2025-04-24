from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

# Cifrado de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Clave secreta y algoritmo para los tokens
SECRET_KEY = "clave_secreta_motoya"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_minutes: int = 60):
    data_copy = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    data_copy.update({"exp": expire})
    return jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
