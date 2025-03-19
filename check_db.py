import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Parámetros de conexión
params = {
    'dbname': 'proyecto_1',
    'user': 'admin',
    'password': 'admin123',
    'host': 'localhost'
}

try:
    # Conexión simple para verificar tablas
    conn = psycopg2.connect(**params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    # Obtener tablas
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    
    tables = cur.fetchall()
    
    if tables:
        print("Tablas en la base de datos:")
        for table in tables:
            print(f"  - {table[0]}")
    else:
        print("No hay tablas en la base de datos.")
    
    # Cerrar todo
    cur.close()
    conn.close()

except Exception as e:
    print(f"Error al conectar o consultar: {e}")
    print(f"Tipo de error: {type(e)}") 