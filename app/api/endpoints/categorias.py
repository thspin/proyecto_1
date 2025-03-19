from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.models import Categoria, Usuario
from app.schemas.schemas import CategoriaCreate, Categoria as CategoriaSchema, CategoriaUpdate

router = APIRouter()

@router.post("/", response_model=CategoriaSchema)
async def create_categoria(
    categoria_in: CategoriaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    # Create new category
    db_categoria = Categoria(
        nombre=categoria_in.nombre,
        tipo=categoria_in.tipo
    )
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@router.get("/", response_model=List[CategoriaSchema])
async def read_categorias(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    categorias = db.query(Categoria).offset(skip).limit(limit).all()
    return categorias

@router.get("/{categoria_id}", response_model=CategoriaSchema)
async def read_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    return categoria

@router.put("/{categoria_id}", response_model=CategoriaSchema)
async def update_categoria(
    categoria_id: int,
    categoria_in: CategoriaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    # Update category data
    categoria_data = categoria_in.dict(exclude_unset=True)
    for key, value in categoria_data.items():
        setattr(categoria, key, value)
    
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

@router.delete("/{categoria_id}", response_model=CategoriaSchema)
async def delete_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    # Check if there are transactions using this category
    if categoria.transacciones:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar la categoría porque tiene transacciones asociadas"
        )
    
    db.delete(categoria)
    db.commit()
    return categoria 