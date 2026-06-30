from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.movimiento import MovimientoCreate
from app.services.movimiento_service import MovimientoService

router = APIRouter(
    prefix="/movimientos",
    tags=["Movimientos"]
)


@router.post("/")
def crear_movimiento(
    data: MovimientoCreate,
    db: Session = Depends(get_db)
):
    return MovimientoService.crear_movimiento(db, data)


@router.get("/")
def listar_movimientos(
    db: Session = Depends(get_db)
):
    return MovimientoService.listar_movimientos(db)


@router.get("/historial")
def historial_completo(
    db: Session = Depends(get_db)
):
    return MovimientoService.historial(db)


@router.get("/persona/{persona_id}")
def historial_persona(
    persona_id: str,
    db: Session = Depends(get_db)
):
    return MovimientoService.historial_persona(db, persona_id)