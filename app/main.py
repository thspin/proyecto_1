from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FastAPI app",
    description="API REST con FastAPI y PostgreSQL",
    version="1.0.0"
)

# Configuracion de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #En produccion especificar los origenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API"}