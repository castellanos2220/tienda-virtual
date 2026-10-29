from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Servicio de Productos")

productos = [
    {"id": 1, "nombre": "Portátil 14 pulgadas", "precio": 2500000},
    {"id": 2, "nombre": "Mouse inalámbrico", "precio": 60000},
]

class ProductoIn(BaseModel):
    nombre: str
    precio: float

@app.get("/productos")
def listar():
    return productos

@app.get("/productos/{producto_id}")
def obtener(producto_id: int):
    for p in productos:
        if p["id"] == producto_id:
            return p
    raise HTTPException(404, "Producto no encontrado")

@app.post("/productos", status_code=201)
def registrar(datos: ProductoIn):
    nuevo = {"id": len(productos) + 1, **datos.model_dump()}
    productos.append(nuevo)
    return nuevo