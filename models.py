# Importar las librerías necesarias de SQLAlchemy y Pydantic
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

# URL de conexión a la base de datos PostgreSQL
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/inventario"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crear una clase de sesión local para manejar las transacciones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarar la clase base para los modelos de SQLAlchemy
Base = declarative_base()

# Definición del modelo de datos 'Pelicula'
class Inventario(Base):
    __tablename__ = "equipo"  # Nombre de la tabla en la base de datos

    id_equ = Column(Integer, primary_key=True, index=True)  # ID de la película (clave primaria)
    des_equ = Column(String, index=True)  # Título de la película
    mar_equ = Column(String)  # Director de la película
    pre_equ = Column(DECIMAL)  
    can_equ = Column(Integer)

# Modelo Pydantic para la creación de una nueva película
class InventarioCreate(BaseModel):
    des_equ: str  # Título de la película
    mar_equ: str  # Director de la película
    pre_equ: DECIMAL
    can_equ: int

# Modelo Pydantic para la respuesta al cliente, incluye el ID
class InventarioResponse(InventarioCreate):
    id: int  # ID de la película (será generado por la base de datos)

    class Config:
        orm_mode = True  # Permite que Pydantic trabaje con modelos de SQLAlchemy
