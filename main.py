from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Importar CORSMiddleware para manejar CORS
from sqlalchemy.orm import Session
from typing import List
from models import Inventario, InventarioCreate, InventarioResponse, SessionLocal, Base, engine

# Crear todas las tablas en la base de datos usando los modelos definidos
Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI
app = FastAPI()

# Configuración del middleware de CORS para permitir solicitudes desde diferentes orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()  # Crear una nueva sesión de base de datos
    try:
        yield db  # Devolver la sesión al consumidor
    finally:
        db.close()  # Cerrar la sesión al final

# Endpoint para crear una nueva película
@app.post("/inventario/", response_model=InventarioResponse)
def crear_inventario(inventario: InventarioCreate, db: Session = Depends(get_db)):
    db_inventario = Inventario(**inventario.dict())  # Crear un nuevo objeto Pelicula
    db.add(db_inventario)  # Agregar la película a la sesión
    db.commit()  # Confirmar los cambios en la base de datos
    db.refresh(db_inventario)  # Obtener la película recién creada
    return db_inventario  # Devolver la película creada

# Endpoint para leer todas las inventario, ordenadas por ID
@app.get("/inventario/", response_model=List[InventarioResponse])
def leer_inventario(db: Session = Depends(get_db)):
    inventario = db.query(Inventario).order_by(inventario.id).all()  # Consultar todas las películas y ordenarlas por ID
    return inventario  # Devolver la lista de películas

# Endpoint para leer una película específica por ID
@app.get("/inventario/{inventario_id}", response_model=InventarioResponse)
def leer_inventario(inventario_id: int, db: Session = Depends(get_db)):
    inventario = db.query(Inventario).filter(Inventario.id == inventario_id).first()  # Buscar la película por ID
    if inventario is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrada")  # Manejar el caso donde no se encuentra la película
    return inventario  # Devolver la película encontrada

# Endpoint para actualizar una película existente
@app.put("/inventario/{inventario_id}", response_model=InventarioResponse)
def actualizar_inventario(inventario_id: int, inventario: InventarioCreate, db: Session = Depends(get_db)):
    db_inventario = db.query(Inventario).filter(Inventario.id == inventario_id).first() 
    
    if db_inventario is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrada")  # Manejar el caso donde no se encuentra la película
    db_inventario.des_equ = inventario.des_equ  # Actualizar el título
    db_inventario.mar_equ = inventario.mar_equ  # Actualizar el director
    db_inventario.pre_equ = inventario.pre_equ
    db_inventario.can_equ = inventario.can_equ
    # Actualizar el año
    db.commit()  # Confirmar los cambios
    return db_inventario  # Devolver la película actualizada

# Endpoint para eliminar una película por ID
@app.delete("/inventario/{inventario_id}", response_model=dict)
def eliminar_inventario(inventario_id: int, db: Session = Depends(get_db)):
    db_inventario = db.query(Inventario).filter(Inventario.id == inventario_id).first()  # Buscar la película por ID
    if db_inventario is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrada")  # Manejar el caso donde no se encuentra la película
    db.delete(db_inventario)  # Eliminar la película de la base de datos
    db.commit()  # Confirmar los cambios
    return {"detail": "Inventario eliminada"}  # Devolver un mensaje de éxito
