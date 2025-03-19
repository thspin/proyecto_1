from fastapi import APIRouter
from app.api.endpoints import usuarios, categorias, transacciones, tarjetas_credito, otros_creditos, alquileres, servicios

api_router = APIRouter()

# Incluir todos los routers de endpoints
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
api_router.include_router(categorias.router, prefix="/categorias", tags=["categorias"])
api_router.include_router(transacciones.router, prefix="/transacciones", tags=["transacciones"])
api_router.include_router(tarjetas_credito.router, prefix="/tarjetas-credito", tags=["tarjetas-credito"])
api_router.include_router(otros_creditos.router, prefix="/otros-creditos", tags=["otros-creditos"])
api_router.include_router(alquileres.router, prefix="/alquileres", tags=["alquileres"])
api_router.include_router(servicios.router, prefix="/servicios", tags=["servicios"]) 