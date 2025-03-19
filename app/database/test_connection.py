from sqlalchemy import create_engine, text

def test_connection():
    try:
        # Crear la URL de conexión manualmente
        DATABASE_URL = "postgresql://postgres:1234@localhost:5432/proyecto_1"
        
        # Crear el engine con parámetros específicos
        engine = create_engine(
            DATABASE_URL,
            connect_args={
                "client_encoding": "utf8"
            }
        )
        
        # Probar la conexión
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.scalar()
            print("¡Conexión exitosa a la base de datos!")
            print(f"Versión de PostgreSQL: {version}")
            
        return True
    except Exception as e:
        print(f"Error al conectar a la base de datos: {str(e)}")
        print(f"Tipo de error: {type(e)}")
        return False

if __name__ == "__main__":
    test_connection() 