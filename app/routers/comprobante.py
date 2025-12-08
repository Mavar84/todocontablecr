from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.comprobante import ComprobanteCreate, Comprobante
from app.crud.comprobante import crear_comprobante, listar_comprobantes, obtener_comprobante

router = APIRouter(
    prefix="/comprobantes",
    tags=["Comprobantes contables"],
)


@router.post("/", response_model=Comprobante)
def crear(
    data: ComprobanteCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    try:
        return crear_comprobante(
            db=db,
            data=data,
            empresa_id=usuario.empresa_id,
            usuario_id=usuario.usuario_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[Comprobante])
def listar(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return listar_comprobantes(db, usuario.empresa_id)


@router.get("/{comprobante_id}", response_model=Comprobante)
def obtener(
    comprobante_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    comprobante = obtener_comprobante(db, usuario.empresa_id, comprobante_id)
    if not comprobante:
        raise HTTPException(status_code=404, detail="Comprobante no encontrado")
    return comprobante
