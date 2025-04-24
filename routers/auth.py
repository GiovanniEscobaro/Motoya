from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.models import Usuario
from schemas.auth_schemas import UsuarioCreate, LoginData, Token
from utils.security import hash_password, verify_password, create_access_token

router = APIRouter(tags=["Auth"])

# Obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Registro de nuevo usuario
@router.post("/registro", response_model=Token)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Correo ya registrado")

    hashed_pwd = hash_password(usuario.contraseña)
    nuevo_usuario = Usuario(nombre=usuario.nombre, email=usuario.email, contraseña=hashed_pwd)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    token = create_access_token({"sub": nuevo_usuario.email})
    return {"access_token": token}

# Login de usuario
@router.post("/login", response_model=Token)
def login(data: LoginData, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == data.email).first()
    if not usuario or not verify_password(data.contraseña, usuario.contraseña):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token({"sub": usuario.email})
    return {"access_token": token}
