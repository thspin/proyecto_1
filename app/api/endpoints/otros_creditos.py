from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.models import OtroCredito, Usuario
from app.schemas.schemas import OtroCreditoCreate, OtroCredito as OtroCreditoSchema, OtroCreditoUpdate

router = APIRouter()

@router.post("/", response_model=OtroCreditoSchema)
async def create_otro_credito(
    credito_in: OtroCreditoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    # Validate that the user is creating a credit for themselves
    if credito_in.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para crear créditos para otros usuarios"
        )
    
    # Create new credit
    db_credito = OtroCredito(
        cuotas=credito_in.cuotas,
        vencimiento=credito_in.vencimiento,
        detalle=credito_in.detalle,
        deuda=credito_in.deuda,
        pago=credito_in.pago,
        medio_de_pago=credito_in.medio_de_pago,
        usuario_id=credito_in.usuario_id
    )
    db.add(db_credito)
    db.commit()
    db.refresh(db_credito)
    return db_credito

@router.get("/", response_model=List[OtroCreditoSchema])
async def read_otros_creditos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    # Only return credits for the current user
    creditos = db.query(OtroCredito).filter(
        OtroCredito.usuario_id == current_user.id
    ).order_by(OtroCredito.vencimiento).offset(skip).limit(limit).all()
    return creditos

@router.get("/{credito_id}", response_model=OtroCreditoSchema)
async def read_otro_credito(
    credito_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    credito = db.query(OtroCredito).filter(OtroCredito.id == credito_id).first()
    if not credito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crédito no encontrado"
        )
    
    # Validate that the user is accessing their own credit
    if credito.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para acceder a este crédito"
        )
    
    return credito

@router.put("/{credito_id}", response_model=OtroCreditoSchema)
async def update_otro_credito(
    credito_id: int,
    credito_in: OtroCreditoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    credito = db.query(OtroCredito).filter(OtroCredito.id == credito_id).first()
    if not credito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crédito no encontrado"
        )
    
    # Validate that the user is updating their own credit
    if credito.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para modificar este crédito"
        )
    
    # Update credit data
    credito_data = credito_in.dict(exclude_unset=True)
    for key, value in credito_data.items():
        setattr(credito, key, value)
    
    db.add(credito)
    db.commit()
    db.refresh(credito)
    return credito

@router.delete("/{credito_id}", response_model=OtroCreditoSchema)
async def delete_otro_credito(
    credito_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    credito = db.query(OtroCredito).filter(OtroCredito.id == credito_id).first()
    if not credito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crédito no encontrado"
        )
    
    # Validate that the user is deleting their own credit
    if credito.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para eliminar este crédito"
        )
    
    db.delete(credito)
    db.commit()
    return credito 