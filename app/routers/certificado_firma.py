from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.certificado_firma import (
    CertificadoFirma,
    CertificadoFirmaCrear,
    CertificadoFirmaActualizar,
)
from app.crud.certificado_firma import (
    crear_certificado,
    listar_certificados,
    obtener_certificado,
    actualizar_certificado,
)

router = APIRouter(prefix="/certificados-firma", tags=["Factura electrónica - certificados"])


@router.post("/", response_model=CertificadoFirma)
def crear(
    datos: CertificadoFirmaCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_certificado(db, usuario.empresa_id, usuario.usuario_id, datos)


@router.get("/", response_model=list[CertificadoFirma])
def listar(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_certificados(db, usuario.empresa_id)


@router.get("/{certificado_id}", response_model=CertificadoFirma)
def obtener(
    certificado_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    cert = obtener_certificado(db, usuario.empresa_id, certificado_id)
    if not cert:
        raise HTTPException(404, "Certificado no encontrado")
    return cert


@router.put("/{certificado_id}", response_model=CertificadoFirma)
def actualizar(
    certificado_id: int,
    datos: CertificadoFirmaActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    cert = actualizar_certificado(db, usuario.empresa_id, certificado_id, usuario.usuario_id, datos)
    if not cert:
        raise HTTPException(404, "Certificado no encontrado")
    return cert
