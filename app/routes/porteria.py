from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.services.porteria_service import (
    PorteriaService
)

from app.schemas.porteria import (
    ConfirmarMovimientoRequest
)

router = APIRouter(
    prefix="/porteria",
    tags=["Porteria"]
)


@router.get("/scan/{codigo_qr}")
def scan_qr(
    codigo_qr: str,
    db: Session = Depends(get_db)
):
    return PorteriaService.scan(
        db,
        codigo_qr
    )
    
@router.post("/confirmar")
def confirmar_movimiento(
    data: ConfirmarMovimientoRequest,
    db: Session = Depends(get_db)
):
    return PorteriaService.confirmar(
        db,
        data.fk_persona,
        data.tipo_movimiento
    ) 
    
    