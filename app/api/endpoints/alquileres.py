from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.models import Alquiler, Usuario
from app.schemas.schemas import AlquilerCreate, Alquiler as AlquilerSchema, AlquilerUpdate

router = APIRouter()

@router.post("/", response_model=AlquilerSchema)
async def create_alquiler(
    alquiler_in: AlquilerCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    # Validate that the user is creating a rental for themselves
    if alquiler_in.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para crear alquileres para otros usuarios"
        )
    
    # Create new rental
    db_alquiler = Alquiler(
        cuota=alquiler_in.cuota,
        vencimiento=alquiler_in.vencimiento,
        inquilino=alquiler_in.inquilino,
        deuda=alquiler_in.deuda,
        pagado=alquiler_in.pagado,
        propiedad=alquiler_in.propiedad,
        recibo=alquiler_in.recibo,
        usuario_id=alquiler_in.usuario_id
    )
    db.add(db_alquiler)
    db.commit()
    db.refresh(db_alquiler)
    return db_alquiler

@router.get("/", response_model=List[AlquilerSchema])
async def read_alquileres(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    # Only return rentals for the current user
    alquileres = db.query(Alquiler).filter(
        Alquiler.usuario_id == current_user.id
    ).order_by(Alquiler.vencimiento, Alquiler.inquilino).offset(skip).limit(limit).all()
    return alquileres

@router.get("/{alquiler_id}", response_model=AlquilerSchema)
async def read_alquiler(
    alquiler_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    alquiler = db.query(Alquiler).filter(Alquiler.id == alquiler_id).first()
    if not alquiler:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alquiler no encontrado"
        )
    
    # Validate that the user is accessing their own rental
    if alquiler.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para acceder a este alquiler"
        )
    
    return alquiler

@router.put("/{alquiler_id}", response_model=AlquilerSchema)
async def update_alquiler(
    alquiler_id: int,
    alquiler_in: AlquilerUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    alquiler = db.query(Alquiler).filter(Alquiler.id == alquiler_id).first()
    if not alquiler:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alquiler no encontrado"
        )
    
    # Validate that the user is updating their own rental
    if alquiler.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para modificar este alquiler"
        )
    
    # Update rental data
    alquiler_data = alquiler_in.dict(exclude_unset=True)
    for key, value in alquiler_data.items():
        setattr(alquiler, key, value)
    
    db.add(alquiler)
    db.commit()
    db.refresh(alquiler)
    return alquiler

@router.delete("/{alquiler_id}", response_model=AlquilerSchema)
async def delete_alquiler(
    alquiler_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    alquiler = db.query(Alquiler).filter(Alquiler.id == alquiler_id).first()
    if not alquiler:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alquiler no encontrado"
        )
    
    # Validate that the user is deleting their own rental
    if alquiler.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para eliminar este alquiler"
        )
    
    db.delete(alquiler)
    db.commit()
    return alquiler 