from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime, date
from typing import Optional, List
from enum import Enum

# Enums
class TipoCategoria(str, Enum):
    INGRESO = "ingreso"
    EGRESO = "egreso"

class TipoTransaccion(str, Enum):
    INGRESO = "ingreso"
    EGRESO = "egreso"

class RolUsuario(str, Enum):
    ADMIN = "admin"
    USUARIO = "usuario"

# Usuario schemas
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    rol: Optional[RolUsuario] = RolUsuario.USUARIO

class UsuarioCreate(UsuarioBase):
    contrasena: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    rol: Optional[RolUsuario] = None

class Usuario(UsuarioBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Categoría schemas
class CategoriaBase(BaseModel):
    nombre: str
    tipo: TipoCategoria

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[TipoCategoria] = None

class Categoria(CategoriaBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Transacción schemas
class TransaccionBase(BaseModel):
    fecha: date
    tipo: TipoTransaccion
    categoria_id: int
    detalle: Optional[str] = None
    monto: float
    medio_de_pago: Optional[str] = None
    usuario_id: int

class TransaccionCreate(TransaccionBase):
    pass

class TransaccionUpdate(BaseModel):
    fecha: Optional[date] = None
    tipo: Optional[TipoTransaccion] = None
    categoria_id: Optional[int] = None
    detalle: Optional[str] = None
    monto: Optional[float] = None
    medio_de_pago: Optional[str] = None

class Transaccion(TransaccionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# TarjetaCredito schemas
class TarjetaCreditoBase(BaseModel):
    cuotas: int
    vencimiento: date
    detalle: Optional[str] = None
    deuda: float
    pago: float
    medio_de_pago: Optional[str] = None
    usuario_id: int

class TarjetaCreditoCreate(TarjetaCreditoBase):
    pass

class TarjetaCreditoUpdate(BaseModel):
    cuotas: Optional[int] = None
    vencimiento: Optional[date] = None
    detalle: Optional[str] = None
    deuda: Optional[float] = None
    pago: Optional[float] = None
    medio_de_pago: Optional[str] = None

class TarjetaCredito(TarjetaCreditoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# OtroCredito schemas
class OtroCreditoBase(BaseModel):
    cuotas: int
    vencimiento: date
    detalle: Optional[str] = None
    deuda: float
    pago: float
    medio_de_pago: Optional[str] = None
    usuario_id: int

class OtroCreditoCreate(OtroCreditoBase):
    pass

class OtroCreditoUpdate(BaseModel):
    cuotas: Optional[int] = None
    vencimiento: Optional[date] = None
    detalle: Optional[str] = None
    deuda: Optional[float] = None
    pago: Optional[float] = None
    medio_de_pago: Optional[str] = None

class OtroCredito(OtroCreditoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Alquiler schemas
class AlquilerBase(BaseModel):
    cuota: int
    vencimiento: date
    inquilino: str
    deuda: float
    pagado: float
    propiedad: Optional[str] = None
    recibo: Optional[str] = None
    usuario_id: int

class AlquilerCreate(AlquilerBase):
    pass

class AlquilerUpdate(BaseModel):
    cuota: Optional[int] = None
    vencimiento: Optional[date] = None
    inquilino: Optional[str] = None
    deuda: Optional[float] = None
    pagado: Optional[float] = None
    propiedad: Optional[str] = None
    recibo: Optional[str] = None

class Alquiler(AlquilerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Servicio schemas
class ServicioBase(BaseModel):
    vencimiento: date
    servicio: str
    detalle: Optional[str] = None
    cuenta: Optional[str] = None
    monto_ars: float = 0
    monto_usd: float = 0
    usuario_id: int

class ServicioCreate(ServicioBase):
    pass

class ServicioUpdate(BaseModel):
    vencimiento: Optional[date] = None
    servicio: Optional[str] = None
    detalle: Optional[str] = None
    cuenta: Optional[str] = None
    monto_ars: Optional[float] = None
    monto_usd: Optional[float] = None

class Servicio(ServicioBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Token schemas para autenticación
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
