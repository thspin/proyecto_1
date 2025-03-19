from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.models import Servicio, Usuario
from app.schemas.schemas import ServicioCreate, Servicio as ServicioSchema, ServicioUpdate

router = APIRouter()

@router.post("/", response_model=ServicioSchema)
async def create_servicio(
    servicio_in: ServicioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    # Validate that the user is creating a service for themselves
    if servicio_in.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para crear servicios para otros usuarios"
        )
    
    # Create new service
    db_servicio = Servicio(
        vencimiento=servicio_in.vencimiento,
        servicio=servicio_in.servicio,
        detalle=servicio_in.detalle,
        cuenta=servicio_in.cuenta,
        monto_ars=servicio_in.monto_ars,
        monto_usd=servicio_in.monto_usd,
        usuario_id=servicio_in.usuario_id
    )
    db.add(db_servicio)
    db.commit()
    db.refresh(db_servicio)
    return db_servicio

@router.get("/", response_model=List[ServicioSchema])
async def read_servicios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    # Only return services for the current user
    servicios = db.query(Servicio).filter(
        Servicio.usuario_id == current_user.id
    ).order_by(Servicio.vencimiento, Servicio.servicio).offset(skip).limit(limit).all()
    return servicios

@router.get("/{servicio_id}", response_model=ServicioSchema)
async def read_servicio(
    servicio_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    servicio = db.query(Servicio).filter(Servicio.id == servicio_id).first()
    if not servicio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Servicio no encontrado"
        )
    
    # Validate that the user is accessing their own service
    if servicio.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para acceder a este servicio"
        )
    
    return servicio

@router.put("/{servicio_id}", response_model=ServicioSchema)
async def update_servicio(
    servicio_id: int,
    servicio_in: ServicioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    servicio = db.query(Servicio).filter(Servicio.id == servicio_id).first()
    if not servicio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Servicio no encontrado"
        )
    
    # Validate that the user is updating their own service
    if servicio.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para modificar este servicio"
        )
    
    # Update service data
    servicio_data = servicio_in.dict(exclude_unset=True)
    for key, value in servicio_data.items():
        setattr(servicio, key, value)
    
    db.add(servicio)
    db.commit()
    db.refresh(servicio)
    return servicio

@router.delete("/{servicio_id}", response_model=ServicioSchema)
async def delete_servicio(
    servicio_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    servicio = db.query(Servicio).filter(Servicio.id == servicio_id).first()
    if not servicio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Servicio no encontrado"
        )
    
    # Validate that the user is deleting their own service
    if servicio.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para eliminar este servicio"
        )
    
    db.delete(servicio)
    db.commit()
    return servicio 