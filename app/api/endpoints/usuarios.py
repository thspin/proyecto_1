from datetime import timedelta
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.api.deps import get_db, get_current_user, get_current_admin_user
from app.models.models import Usuario, RolUsuario
from app.schemas.schemas import UsuarioCreate, Usuario as UsuarioSchema, UsuarioUpdate, Token

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configs
SECRET_KEY = "your-secret-key"  # Change in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if expires_delta:
        expire = expires_delta
    to_encode.update({"exp": timedelta(minutes=15) + expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, email: str, password: str) -> Usuario:
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user or not verify_password(password, user.contrasena):
        return None
    return user

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Any:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", response_model=UsuarioSchema)
async def create_user(
    user_in: UsuarioCreate, db: Session = Depends(get_db)
) -> Any:
    # Check if user with the email already exists
    db_user = db.query(Usuario).filter(Usuario.email == user_in.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create new user
    hashed_password = get_password_hash(user_in.contrasena)
    db_user = Usuario(
        email=user_in.email,
        nombre=user_in.nombre,
        contrasena=hashed_password,
        rol=user_in.rol
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[UsuarioSchema])
async def read_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin_user)
) -> Any:
    users = db.query(Usuario).offset(skip).limit(limit).all()
    return users

@router.get("/me", response_model=UsuarioSchema)
async def read_user_me(
    current_user: Usuario = Depends(get_current_user),
) -> Any:
    return current_user

@router.get("/{user_id}", response_model=UsuarioSchema)
async def read_user(
    user_id: int, db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    # Regular users can only access their own data
    if current_user.rol != RolUsuario.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/{user_id}", response_model=UsuarioSchema)
async def update_user(
    user_id: int, user_in: UsuarioUpdate, db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Any:
    # Regular users can only update their own data
    if current_user.rol != RolUsuario.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user data
    user_data = user_in.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", response_model=UsuarioSchema)
async def delete_user(
    user_id: int, db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin_user)
) -> Any:
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    return user 