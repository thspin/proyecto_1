from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.models import Transaccion, Usuario, Categoria
from app.schemas.schemas import TransaccionCreate, Transaccion as TransaccionSchema, TransaccionUpdate

router = APIRouter()

@router.post("/", response_model=TransaccionSchema)
async def create_transaccion(
    transaccion_in: TransaccionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    # Check if the category exists
    categoria = db.query(Categoria).filter(Categoria.id == transaccion_in.categoria_id).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    # Validate that the user is creating a transaction for themselves
    if transaccion_in.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para crear transacciones para otros usuarios"
        )
    
    # Create new transaction
    db_transaccion = Transaccion(
        fecha=transaccion_in.fecha,
        tipo=transaccion_in.tipo,
        categoria_id=transaccion_in.categoria_id,
        detalle=transaccion_in.detalle,
        monto=transaccion_in.monto,
        medio_de_pago=transaccion_in.medio_de_pago,
        usuario_id=transaccion_in.usuario_id
    )
    db.add(db_transaccion)
    db.commit()
    db.refresh(db_transaccion)
    return db_transaccion

@router.get("/", response_model=List[TransaccionSchema])
async def read_transacciones(
    skip: int = 0,
    limit: int = 100,
    tipo: str = None,
    categoria_id: int = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    # Build query
    query = db.query(Transaccion).filter(Transaccion.usuario_id == current_user.id)
    
    # Apply filters if provided
    if tipo:
        query = query.filter(Transaccion.tipo == tipo)
    if categoria_id:
        query = query.filter(Transaccion.categoria_id == categoria_id)
    
    # Apply pagination
    transacciones = query.order_by(Transaccion.fecha.desc()).offset(skip).limit(limit).all()
    return transacciones

@router.get("/{transaccion_id}", response_model=TransaccionSchema)
async def read_transaccion(
    transaccion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    transaccion = db.query(Transaccion).filter(Transaccion.id == transaccion_id).first()
    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada"
        )
    
    # Validate that the user is accessing their own transaction
    if transaccion.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para acceder a esta transacción"
        )
    
    return transaccion

@router.put("/{transaccion_id}", response_model=TransaccionSchema)
async def update_transaccion(
    transaccion_id: int,
    transaccion_in: TransaccionUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    transaccion = db.query(Transaccion).filter(Transaccion.id == transaccion_id).first()
    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada"
        )
    
    # Validate that the user is updating their own transaction
    if transaccion.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para modificar esta transacción"
        )
    
    # Check if the category exists if it's being updated
    if transaccion_in.categoria_id is not None:
        categoria = db.query(Categoria).filter(Categoria.id == transaccion_in.categoria_id).first()
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )
    
    # Update transaction data
    transaccion_data = transaccion_in.dict(exclude_unset=True)
    for key, value in transaccion_data.items():
        setattr(transaccion, key, value)
    
    db.add(transaccion)
    db.commit()
    db.refresh(transaccion)
    return transaccion

@router.delete("/{transaccion_id}", response_model=TransaccionSchema)
async def delete_transaccion(
    transaccion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    transaccion = db.query(Transaccion).filter(Transaccion.id == transaccion_id).first()
    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada"
        )
    
    # Validate that the user is deleting their own transaction
    if transaccion.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para eliminar esta transacción"
        )
    
    db.delete(transaccion)
    db.commit()
    return transaccion 