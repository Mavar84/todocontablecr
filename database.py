import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cargar variables del .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# ===============================================
# CONFIGURACIÓN DEL MOTOR SQLALCHEMY
# ===============================================

# Se permite hasta 20 conexiones simultáneas
engine = create_engine(
    DATABASE_URL,
    pool_size=20,            # número máximo de conexiones en el pool
    max_overflow=0,          # no crear conexiones adicionales fuera del pool
    pool_pre_ping=True,      # valida que la conexión esté viva
    pool_timeout=30,         # segundos máximos para esperar conexión libre
    echo=False               # cambiar a True para ver los SQL en consola
)

# ===============================================
# SESIONES PARA FASTAPI
# ===============================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False    # mejora estabilidad en servicios concurrentes
)

# Base para los modelos ORM
Base = declarative_base()

# ===============================================
# DEPENDENCIA PARA FASTAPI
# ===============================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
