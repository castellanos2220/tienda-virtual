import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Servicio de Pedidos")

URL_PRODUCTOS = "http://localhost:8001"
URL_CLIENTES = "http://localhost:8002"

pedidos = []

class PedidoIn(BaseModel):
    cliente_id: int
    producto_id: int
    cantidad: int

def consultar(url: str, nombre: str):
    try:
        r = requests.get(url, timeout=3)
    except requests.RequestException:
        raise HTTPException(503, f"Servicio de {nombre} no disponible")
    if r.status_code == 404:
        raise HTTPException(404, f"{nombre} no encontrado")
    return r.json()

@app.post("/pedidos", status_code=201)
def registrar(datos: PedidoIn):
    cliente = consultar(f"{URL_CLIENTES}/clientes/{datos.cliente_id}", "cliente")
    producto = consultar(f"{URL_PRODUCTOS}/productos/{datos.producto_id}", "producto")
    nuevo = {
        "id": len(pedidos) + 1,
        "cliente_id": cliente["id"],
        "producto_id": producto["id"],
        "cantidad": datos.cantidad,
        "total": producto["precio"] * datos.cantidad,
        "estado": "REGISTRADO",
    }
    pedidos.append(nuevo)
    return nuevo

@app.get("/pedidos")
def listar():
    return pedidos

@app.get("/pedidos/{pedido_id}")
def estado(pedido_id: int):
    for p in pedidos:
        if p["id"] == pedido_id:
            return p
    raise HTTPException(404, "Pedido no encontrado")