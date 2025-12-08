from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.extracto_bancario import (
    ExtractoBancario,
    ExtractoBancarioCrear,
    ExtractoBancarioActualizar,
)
from app.crud.extracto_bancario import (
    crear_extracto,
    listar_extractos,
    obtener_extracto,
    actualizar_extracto,
)

router = APIRouter(prefix="/extractos-bancarios", tags=["Bancos - extractos"])


@router.post("/", response_model=ExtractoBancario)
def crear(
    datos: ExtractoBancarioCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_extracto(db, usuario.empresa_id, usuario.usuario_id, datos)


@router.get("/", response_model=list[ExtractoBancario])
def listar(
    cuenta_bancaria_id: int | None = None,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_extractos(db, usuario.empresa_id, cuenta_bancaria_id)


@router.get("/{extracto_id}", response_model=ExtractoBancario)
def obtener(
    extracto_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    ext = obtener_extracto(db, usuario.empresa_id, extracto_id)
    if not ext:
        raise HTTPException(404, "Extracto bancario no encontrado")
    return ext


@router.put("/{extracto_id}", response_model=ExtractoBancario)
def actualizar(
    extracto_id: int,
    datos: ExtractoBancarioActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    ext = actualizar_extracto(db, usuario.empresa_id, extracto_id, usuario.usuario_id, datos)
    if not ext:
        raise HTTPException(404, "Extracto bancario no encontrado")
    return ext
