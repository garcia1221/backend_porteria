from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.equipos import router as equipos_router
from app.routes.accesorios import router as accesorios_router
from app.routes.qr import router as qr_router
from app.routes.movimientos import router as movimientos_router
from app.routes.porteria import router as porteria_router
from app.routes.usuarios_externo import router as usuarios_externo_router
from app.routes.dashboard import router as dashboard_router
from app.routes.reportes import router as reportes_router
from app.routes.personas import router as personas_router

app = FastAPI(
    title="Control Equipos SENA",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(equipos_router)
app.include_router(accesorios_router)
app.include_router(qr_router)
app.include_router(movimientos_router)
app.include_router(porteria_router)
app.include_router(usuarios_externo_router)
app.include_router(dashboard_router)
app.include_router(reportes_router)
app.include_router(personas_router)


@app.get("/")
def root():
    return {
        "mensaje": "API Control Equipos SENA"
    }
