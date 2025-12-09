"""
Configuración de la base de datos SQLAlchemy con SQLite
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
import os

# Obtener la ruta de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./quiz_api.db")

# Crear el engine de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db() -> Generator:
    """
    Función para obtener la sesión de base de datos.
    Se usa como dependencia en FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa la base de datos creando todas las tablas.
    """
    Base.metadata.create_all(bind=engine)
