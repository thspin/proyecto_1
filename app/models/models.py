from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean, DateTime, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.database.database import Base

class TipoCategoria(str, enum.Enum):
    INGRESO = "ingreso"
    EGRESO = "egreso"

class TipoTransaccion(str, enum.Enum):
    INGRESO = "ingreso"
    EGRESO = "egreso"

class RolUsuario(str, enum.Enum):
    ADMIN = "admin"
    USUARIO = "usuario"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    contrasena = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False, default=RolUsuario.USUARIO)
    
    # Relaciones
    transacciones = relationship("Transaccion", back_populates="usuario")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(20), nullable=False)
    
    # Relaciones
    transacciones = relationship("Transaccion", back_populates="categoria")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Transaccion(Base):
    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False, default=func.current_date())
    tipo = Column(String(20), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    detalle = Column(Text)
    monto = Column(Float, nullable=False)
    medio_de_pago = Column(String(100))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Relaciones
    categoria = relationship("Categoria", back_populates="transacciones")
    usuario = relationship("Usuario", back_populates="transacciones")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class TarjetaCredito(Base):
    __tablename__ = "tarjetas_credito"

    id = Column(Integer, primary_key=True, index=True)
    cuotas = Column(Integer, nullable=False)
    vencimiento = Column(Date, nullable=False)
    detalle = Column(Text)
    deuda = Column(Float, nullable=False)
    pago = Column(Float, nullable=False)
    medio_de_pago = Column(String(100))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Relaciones
    usuario = relationship("Usuario")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class OtroCredito(Base):
    __tablename__ = "otros_creditos"

    id = Column(Integer, primary_key=True, index=True)
    cuotas = Column(Integer, nullable=False)
    vencimiento = Column(Date, nullable=False)
    detalle = Column(Text)
    deuda = Column(Float, nullable=False)
    pago = Column(Float, nullable=False)
    medio_de_pago = Column(String(100))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Relaciones
    usuario = relationship("Usuario")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Alquiler(Base):
    __tablename__ = "alquileres"

    id = Column(Integer, primary_key=True, index=True)
    cuota = Column(Integer, nullable=False)
    vencimiento = Column(Date, nullable=False)
    inquilino = Column(String(255), nullable=False)
    deuda = Column(Float, nullable=False)
    pagado = Column(Float, nullable=False)
    propiedad = Column(Text)
    recibo = Column(String(100))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Relaciones
    usuario = relationship("Usuario")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Servicio(Base):
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True)
    vencimiento = Column(Date, nullable=False)
    servicio = Column(String(100), nullable=False)
    detalle = Column(Text)
    cuenta = Column(String(100))
    monto_ars = Column(Float, default=0)
    monto_usd = Column(Float, default=0)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Relaciones
    usuario = relationship("Usuario")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
