# API REST con FastAPI y PostgreSQL

Este proyecto es una API REST construida con FASTAPI que se conecta a una base de datos PostgreSQL.

## Estructura del proyecto

app/
├── api/ # Endpoints y rutas de la API
├── models/ # Modelos de la base de datos
├── schemas/ # Esquemas Pydantic para validación de datos
└── database/ # Configuración de la base de datos

## Requisitos

- Python 3.8+
- PostgreSQL
- Dependencias listadas en `requirements.txt`

## Instalación

1. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
- Copiar `.env.example` a `.env`
- Actualizar las credenciales de la base de datos en `.env`

4. Ejecutar la aplicación:
```bash
uvicorn app.main:app --reload
```

## Documentación de la API

Una vez que la aplicación esté corriendo, puedes acceder a:
- Documentación Swagger UI: http://localhost:8000/docs
- Documentación ReDoc: http://localhost:8000/redoc