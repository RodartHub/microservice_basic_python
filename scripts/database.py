from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Configuración de la conexión (usamos el puerto 5433 del Docker)
DATABASE_URL = "postgresql://admin:password123@localhost:5433/micro_service_db"

# El motor de la base de datos
engine = create_engine(DATABASE_URL)

# La fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# La clase base para nuestros modelos
Base = declarative_base()

# 2. Definición del Modelo
class OrdenProcesada(Base):
    __tablename__ = "ordenes_procesadas"
    id = Column(Integer, primary_key=True, index=True)
    contenido = Column(String)

# 3. Crear las tablas físicamente en Postgres
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("¡Tablas creadas exitosamente!")