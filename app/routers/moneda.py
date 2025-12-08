from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.moneda import Moneda, MonedaCrear, MonedaActualizar
from app.crud.moneda import crear_moneda, listar_monedas, obtener_moneda, actualizar_moneda

router = APIRouter(prefix="/monedas", tags=["Monedas"])


@router.post("/", response_model=Moneda)
def crear(
    datos: MonedaCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_moneda(db, datos)


@router.get("/", response_model=list[Moneda])
def listar(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_monedas(db)


@router.get("/{moneda_id}", response_model=Moneda)
def obtener(
    moneda_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    moneda = obtener_moneda(db, moneda_id)
    if not moneda:
        raise HTTPException(404, "Moneda no encontrada")
    return moneda


@router.put("/{moneda_id}", response_model=Moneda)
def actualizar(
    moneda_id: int,
    datos: MonedaActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    moneda = actualizar_moneda(db, moneda_id, datos)
    if not moneda:
        raise HTTPException(404, "Moneda no encontrada")
    return moneda
