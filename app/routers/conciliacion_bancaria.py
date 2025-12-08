from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.conciliacion_bancaria import (
    ConciliacionCrear,
    Conciliacion,
)
from app.crud.conciliacion_bancaria import (
    crear_conciliacion,
    listar_conciliaciones,
    obtener_conciliacion,
)

router = APIRouter(prefix="/conciliaciones-bancarias", tags=["Conciliaciones bancarias"])


@router.post("/", response_model=Conciliacion)
def crear(
    datos: ConciliacionCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        return crear_conciliacion(db, datos, usuario.empresa_id, usuario.usuario_id)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/", response_model=list[Conciliacion])
def listar(
    cuenta_bancaria_id: int | None = None,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_conciliaciones(db, usuario.empresa_id, cuenta_bancaria_id)


@router.get("/{conciliacion_id}", response_model=Conciliacion)
def obtener(
    conciliacion_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    conc = obtener_conciliacion(db, usuario.empresa_id, conciliacion_id)
    if not conc:
        raise HTTPException(404, "Conciliación no encontrada")
    return conc
