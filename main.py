from database import engine
from models import models

# Crear todas las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

print("✅ Tablas creadas correctamente en la base de datos MotoYa")

