from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.services.movimiento_service import (
    MovimientoService
)

router = APIRouter(
    prefix="/movimientos",
    tags=["Movimientos"]
)


@router.get("/historial")
def historial(
    db: Session = Depends(get_db)
):
    return MovimientoService.historial(
        db
    )
    
@router.get("/persona/{persona_id}")
def historial_persona(
    persona_id: str,
    db: Session = Depends(get_db)
):
    return MovimientoService.historial_persona(
        db,
        persona_id
    )