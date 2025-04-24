# models/models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, DECIMAL, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum

# Enum para tipo de usuario
class TipoUsuarioEnum(enum.Enum):
    pasajero = "pasajero"
    admin = "admin"

# Enum para estado de viaje
class EstadoViajeEnum(enum.Enum):
    pendiente = "pendiente"
    aceptado = "aceptado"
    finalizado = "finalizado"
    cancelado = "cancelado"

# Enum para métodos de pago
class MetodoPagoEnum(enum.Enum):
    efectivo = "efectivo"
    nequi = "nequi"
    daviplata = "daviplata"

# Tabla usuarios
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    tipo = Column(Enum(TipoUsuarioEnum), default=TipoUsuarioEnum.pasajero)
    creado_en = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    viajes = relationship("Viaje", back_populates="usuario")

# Tabla conductores
class Conductor(Base):
    __tablename__ = "conductores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20))
    cedula = Column(String(20), nullable=False)
    moto_placa = Column(String(20), nullable=False)
    moto_modelo = Column(String(50))
    activo = Column(Boolean, default=True)
    ubicacion_lat = Column(DECIMAL(10, 6))
    ubicacion_lng = Column(DECIMAL(10, 6))
    creado_en = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    viajes = relationship("Viaje", back_populates="conductor")

# Tabla viajes
class Viaje(Base):
    __tablename__ = "viajes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    conductor_id = Column(Integer, ForeignKey("conductores.id"))
    origen_lat = Column(DECIMAL(10, 6), nullable=False)
    origen_lng = Column(DECIMAL(10, 6), nullable=False)
    destino_lat = Column(DECIMAL(10, 6), nullable=False)
    destino_lng = Column(DECIMAL(10, 6), nullable=False)
    estado = Column(Enum(EstadoViajeEnum), default=EstadoViajeEnum.pendiente)
    metodo_pago = Column(Enum(MetodoPagoEnum), default=MetodoPagoEnum.efectivo)
    costo = Column(DECIMAL(10, 2))
    fecha_solicitud = Column(DateTime, default=datetime.utcnow)
    fecha_finalizacion = Column(DateTime)
    costo = Column(DECIMAL(10, 2))
    comision = Column(DECIMAL(10, 2), default=0.00)

    # Relaciones
    usuario = relationship("Usuario", back_populates="viajes")
    conductor = relationship("Conductor", back_populates="viajes")
    pago = relationship("HistorialPago", back_populates="viaje", uselist=False)

# Tabla historial_pagos
class HistorialPago(Base):
    __tablename__ = "historial_pagos"

    id = Column(Integer, primary_key=True, index=True)
    viaje_id = Column(Integer, ForeignKey("viajes.id"), nullable=False)
    monto = Column(DECIMAL(10, 2), nullable=False)
    metodo = Column(Enum(MetodoPagoEnum), nullable=False)
    fecha_pago = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    viaje = relationship("Viaje", back_populates="pago")

    # Tabla de ingresos de MotoYa por viaje
class IngresoMotoYa(Base):
    __tablename__ = "ingresos_motoya"

    id = Column(Integer, primary_key=True, index=True)
    viaje_id = Column(Integer, ForeignKey("viajes.id"), nullable=False)
    monto_comision = Column(DECIMAL(10, 2), nullable=False)
    metodo_pago = Column(Enum(MetodoPagoEnum), nullable=False)
    fecha_ingreso = Column(DateTime, default=datetime.utcnow)

    # Relación con viaje
    viaje = relationship("Viaje", backref="ingreso_motoya")
