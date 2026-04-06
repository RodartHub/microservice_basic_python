from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, OrdenProcesada
from prometheus_fastapi_instrumentator import Instrumentator
from typing import List

app = FastAPI(title="Mi Primer Microservicio de Consulta")

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de Órdenes. Ve a /ordenes para ver los datos."}

@app.get("/ordenes")
def listar_ordenes(db: Session = Depends(get_db)):
    # Consultamos todos los registros de la tabla
    ordenes = db.query(OrdenProcesada).all()
    return ordenes


Instrumentator().instrument(app).expose(app)