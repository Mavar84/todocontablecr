from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.cliente import Cliente, ClienteCrear, ClienteActualizar
from app.crud.cliente import (
    crear_cliente,
    listar_clientes,
    obtener_cliente,
    actualizar_cliente,
)

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=Cliente)
def crear(
    datos: ClienteCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_cliente(db, usuario.empresa_id, usuario.usuario_id, datos)


@router.get("/", response_model=list[Cliente])
def listar(
    solo_activos: bool = True,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_clientes(db, usuario.empresa_id, solo_activos)


@router.get("/{cliente_id}", response_model=Cliente)
def obtener(
    cliente_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    cli = obtener_cliente(db, usuario.empresa_id, cliente_id)
    if not cli:
        raise HTTPException(404, "Cliente no encontrado")
    return cli


@router.put("/{cliente_id}", response_model=Cliente)
def actualizar(
    cliente_id: int,
    datos: ClienteActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    cli = actualizar_cliente(db, usuario.empresa_id, cliente_id, usuario.usuario_id, datos)
    if not cli:
        raise HTTPException(404, "Cliente no encontrado")
    return cli
