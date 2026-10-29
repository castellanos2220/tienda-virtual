from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Servicio de Clientes")

clientes = [
    {"id": 1, "nombre": "Laura Gómez", "correo": "laura@correo.com"},
]

class ClienteIn(BaseModel):
    nombre: str
    correo: str

@app.get("/clientes")
def listar():
    return clientes

@app.get("/clientes/{cliente_id}")
def obtener(cliente_id: int):
    for c in clientes:
        if c["id"] == cliente_id:
            return c
    raise HTTPException(404, "Cliente no encontrado")

@app.post("/clientes", status_code=201)
def registrar(datos: ClienteIn):
    nuevo = {"id": len(clientes) + 1, **datos.model_dump()}
    clientes.append(nuevo)
    return nuevo