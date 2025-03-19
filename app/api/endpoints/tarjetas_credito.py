from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.models import TarjetaCredito, Usuario
from app.schemas.schemas import TarjetaCreditoCreate, TarjetaCredito as TarjetaCreditoSchema, TarjetaCreditoUpdate

router = APIRouter()

@router.post("/", response_model=TarjetaCreditoSchema)
async def create_tarjeta_credito(
    tarjeta_in: TarjetaCreditoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    # Validate that the user is creating a credit card for themselves
    if tarjeta_in.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para crear tarjetas de crédito para otros usuarios"
        )
    
    # Create new credit card
    db_tarjeta = TarjetaCredito(
        cuotas=tarjeta_in.cuotas,
        vencimiento=tarjeta_in.vencimiento,
        detalle=tarjeta_in.detalle,
        deuda=tarjeta_in.deuda,
        pago=tarjeta_in.pago,
        medio_de_pago=tarjeta_in.medio_de_pago,
        usuario_id=tarjeta_in.usuario_id
    )
    db.add(db_tarjeta)
    db.commit()
    db.refresh(db_tarjeta)
    return db_tarjeta

@router.get("/", response_model=List[TarjetaCreditoSchema])
async def read_tarjetas_credito(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    # Only return credit cards for the current user
    tarjetas = db.query(TarjetaCredito).filter(
        TarjetaCredito.usuario_id == current_user.id
    ).order_by(TarjetaCredito.vencimiento).offset(skip).limit(limit).all()
    return tarjetas

@router.get("/{tarjeta_id}", response_model=TarjetaCreditoSchema)
async def read_tarjeta_credito(
    tarjeta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    tarjeta = db.query(TarjetaCredito).filter(TarjetaCredito.id == tarjeta_id).first()
    if not tarjeta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarjeta de crédito no encontrada"
        )
    
    # Validate that the user is accessing their own credit card
    if tarjeta.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para acceder a esta tarjeta de crédito"
        )
    
    return tarjeta

@router.put("/{tarjeta_id}", response_model=TarjetaCreditoSchema)
async def update_tarjeta_credito(
    tarjeta_id: int,
    tarjeta_in: TarjetaCreditoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    tarjeta = db.query(TarjetaCredito).filter(TarjetaCredito.id == tarjeta_id).first()
    if not tarjeta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarjeta de crédito no encontrada"
        )
    
    # Validate that the user is updating their own credit card
    if tarjeta.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para modificar esta tarjeta de crédito"
        )
    
    # Update credit card data
    tarjeta_data = tarjeta_in.dict(exclude_unset=True)
    for key, value in tarjeta_data.items():
        setattr(tarjeta, key, value)
    
    db.add(tarjeta)
    db.commit()
    db.refresh(tarjeta)
    return tarjeta

@router.delete("/{tarjeta_id}", response_model=TarjetaCreditoSchema)
async def delete_tarjeta_credito(
    tarjeta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    tarjeta = db.query(TarjetaCredito).filter(TarjetaCredito.id == tarjeta_id).first()
    if not tarjeta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarjeta de crédito no encontrada"
        )
    
    # Validate that the user is deleting their own credit card
    if tarjeta.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para eliminar esta tarjeta de crédito"
        )
    
    db.delete(tarjeta)
    db.commit()
    return tarjeta 