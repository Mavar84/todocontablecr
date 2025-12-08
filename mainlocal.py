import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from sqlalchemy import text
from database import engine, SessionLocal  # Importar la conexión a la BD
from app.routers import auth, empresa, catalogo_cuenta,comprobante,cliente
from app.routers import  proveedor, cuenta_cobrar, cuenta_pagar,factura_venta
from app.routers import  orden_compra, factura_compra,bodega, producto, inventario 
from app.routers import  tipo_activo, activo_fijo,cuenta_bancaria, movimiento_bancario 
from app.routers import  conciliacion_bancaria, reportes_contables,moneda, tipo_cambio 
from app.routers import  revaluacion_cambiaria
from app.routers import  configuracion_fe,certificado_firma,factura_electronica
from app.routers import recepcion_electronica ,cabys_codigo
from app.routers import impuesto
from app.routers import producto_impuesto
from app.routers import retencion_config
from app.routers import retencion_aplicada

from app.routers import (
    presupuestos,
    presupuesto_lineas,
    presupuesto_reporte,
    extractos_bancarios,
    extracto_movimientos,
    caja_chica,
    caja_chica_gastos,
    caja_chica_rendiciones,
     
    ordenes_trabajo,
    ordenes_trabajo_material_plan,
    ordenes_trabajo_consumos,
    ordenes_trabajo_actividades,empleados, planilla_eventos, planilla, planilla_contabilizacion
)
# ===============================
# Carga del archivo .env
# ===============================

load_dotenv()

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", 8000))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# ===============================
# Crear aplicación FastAPI
# ===============================

app = FastAPI(
    title="Sistema Contable SaaS – Backend",
    version="1.0.0"
)

# ===============================
# Middlewares (CORS)
# ===============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# Verificar conexión a la BD
# ===============================

def verificar_conexion():
    """
    Verifica que la base de datos PostgreSQL esté accesible.
    Se ejecuta una consulta simple SELECT 1.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print("❌ Error conectando a la base de datos:", e)
        return False

# Ejecutar prueba al iniciar el servidor
if not verificar_conexion():
    print("⚠️ Advertencia: No se pudo establecer conexión inicial con la base de datos.")
else:
    print("✅ Conexión inicial a la base de datos establecida correctamente.")


# ===============================
# ENDPOINTS
# ===============================

@app.get("/")
async def root():
    return {"mensaje": "Servidor FastAPI funcionando correctamente."}

@app.get("/health/db")
async def health_db():
    """
    Endpoint para verificar si la base de datos responde correctamente.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}

app.include_router(auth.router)
app.include_router(empresa.router)
app.include_router(catalogo_cuenta.router)
app.include_router(comprobante.router)
app.include_router(cliente.router)
app.include_router(proveedor.router)
app.include_router(cuenta_cobrar.router)    
app.include_router(cuenta_pagar.router)
app.include_router(factura_venta.router)
app.include_router(orden_compra.router)
app.include_router(factura_compra.router)
app.include_router(bodega.router)
app.include_router(producto.router)
app.include_router(inventario.router)
app.include_router(tipo_activo.router)
app.include_router(activo_fijo.router)

app.include_router(cuenta_bancaria.router)
app.include_router(movimiento_bancario.router)
app.include_router(conciliacion_bancaria.router)
app.include_router(reportes_contables.router)
app.include_router(moneda.router)
app.include_router(tipo_cambio.router)
app.include_router(revaluacion_cambiaria.router)
app.include_router(configuracion_fe.router)
app.include_router(certificado_firma.router)
app.include_router(factura_electronica.router)
app.include_router(recepcion_electronica.router)
app.include_router(cabys_codigo.router)
app.include_router(impuesto.router)
app.include_router(producto_impuesto.router)
app.include_router(retencion_config.router)
app.include_router(retencion_aplicada.router)
app.include_router(presupuestos.router)
app.include_router(presupuesto_lineas.router)
app.include_router(presupuesto_reporte.router)
app.include_router(extractos_bancarios.router)
app.include_router(extracto_movimientos.router)
app.include_router(caja_chica.router)
app.include_router(caja_chica_gastos.router)
app.include_router(caja_chica_rendiciones.router)
app.include_router(ordenes_trabajo.router)
app.include_router(ordenes_trabajo_material_plan.router)
app.include_router(ordenes_trabajo_consumos.router)
app.include_router(ordenes_trabajo_actividades.router)
app.include_router(empleados.router)
app.include_router(planilla_eventos.router)
app.include_router(planilla.router)
app.include_router(planilla_contabilizacion.router)
# ===============================
# Ejecutar servidor con Uvicorn
# ===============================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=APP_HOST,
        port=APP_PORT,
        reload=True  # recarga automática en desarrollo
    )
