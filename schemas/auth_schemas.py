from pydantic import BaseModel, EmailStr

# Esquema para registrar usuario
class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    contraseña: str

# Esquema para login
class LoginData(BaseModel):
    email: EmailStr
    contraseña: str

# Token devuelto al loguearse
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
