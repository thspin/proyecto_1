from sqlalchemy import create_engine, inspect
from app.database.database import Base, engine
from app.models.models import Usuario, Categoria, Transaccion, TarjetaCredito, OtroCredito, Alquiler, Servicio
from app.models.models import TipoCategoria, TipoTransaccion, RolUsuario
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """Inicializa la base de datos creando todas las tablas definidas en los modelos."""
    try:
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        logger.info("Se han creado todas las tablas en la base de datos.")
        
        # Verificar qué tablas se crearon
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Tablas creadas: {', '.join(tables)}")
        
        return True
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        return False

def crear_datos_iniciales(db):
    """Crea datos iniciales en la base de datos si no existen."""
    try:
        # Verificar si ya existen usuarios
        if db.query(Usuario).count() == 0:
            # Crear usuario administrador
            admin = Usuario(
                nombre="Administrador",
                email="admin@ejemplo.com",
                contrasena="admin123",  # En producción, esto debe estar hasheado
                rol=RolUsuario.ADMIN
            )
            db.add(admin)
            
            # Crear categorías de ejemplo
            categorias = [
                Categoria(nombre="Salario", tipo=TipoCategoria.INGRESO),
                Categoria(nombre="Freelance", tipo=TipoCategoria.INGRESO),
                Categoria(nombre="Alimentación", tipo=TipoCategoria.EGRESO),
                Categoria(nombre="Transporte", tipo=TipoCategoria.EGRESO),
                Categoria(nombre="Ocio", tipo=TipoCategoria.EGRESO),
                Categoria(nombre="Servicios", tipo=TipoCategoria.EGRESO),
            ]
            db.add_all(categorias)
            
            db.commit()
            logger.info("Datos iniciales creados exitosamente.")
        else:
            logger.info("Ya existen datos en la base de datos. No se crearon datos iniciales.")
            
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear datos iniciales: {e}")
        return False

if __name__ == "__main__":
    # Ejecutar inicialización de la base de datos
    if init_db():
        from app.database.database import SessionLocal
        db = SessionLocal()
        try:
            crear_datos_iniciales(db)
        finally:
            db.close()
