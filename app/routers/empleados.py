from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from app.core.auth import get_current_user
from app.models.empleado import Empleado
from app.schemas.empleado import (
    EmpleadoCrear,
    EmpleadoActualizar,
    EmpleadoOut,
)


router = APIRouter(prefix="/empleados", tags=["Planilla - Empleados"])


@router.post("/", response_model=EmpleadoOut)
def crear_empleado(
    datos: EmpleadoCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    emp = Empleado(
        empresa_id=usuario.empresa_id,
        cedula=datos.cedula,
        nombre=datos.nombre,
        apellido1=datos.apellido1,
        apellido2=datos.apellido2,
        fecha_ingreso=datos.fecha_ingreso,
        tipo_contrato=datos.tipo_contrato,
        puesto=datos.puesto,
        departamento=datos.departamento,
        salario_base=datos.salario_base,
        tipo_jornada=datos.tipo_jornada,
        centro_costo_id=datos.centro_costo_id,
        activo=True,
        creado_en=datetime.utcnow(),
    )
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp


@router.get("/", response_model=list[EmpleadoOut])
def listar_empleados(
    activos: bool | None = None,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    q = db.query(Empleado).filter(Empleado.empresa_id == usuario.empresa_id)
    if activos is not None:
        q = q.filter(Empleado.activo == activos)
    return q.order_by(Empleado.nombre).all()


@router.get("/{empleado_id}", response_model=EmpleadoOut)
def obtener_empleado(
    empleado_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    emp = db.query(Empleado).filter(
        Empleado.empresa_id == usuario.empresa_id,
        Empleado.empleado_id == empleado_id,
    ).first()

    if not emp:
        raise HTTPException(404, "Empleado no encontrado")
    return emp


@router.put("/{empleado_id}", response_model=EmpleadoOut)
def actualizar_empleado(
    empleado_id: int,
    datos: EmpleadoActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    emp = db.query(Empleado).filter(
        Empleado.empresa_id == usuario.empresa_id,
        Empleado.empleado_id == empleado_id,
    ).first()

    if not emp:
        raise HTTPException(404, "Empleado no encontrado")

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(emp, campo, valor)

    emp.actualizado_en = datetime.utcnow()

    db.commit()
    db.refresh(emp)
    return emp


@router.delete("/{empleado_id}")
def eliminar_empleado(
    empleado_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    emp = db.query(Empleado).filter(
        Empleado.empresa_id == usuario.empresa_id,
        Empleado.empleado_id == empleado_id,
    ).first()

    if not emp:
        raise HTTPException(404, "Empleado no encontrado")

    emp.activo = False
    emp.actualizado_en = datetime.utcnow()
    db.commit()

    return {"mensaje": "Empleado desactivado correctamente"}
