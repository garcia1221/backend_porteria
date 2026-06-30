from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.services.qr_service import QRService

router = APIRouter(
    prefix="/qr",
    tags=["QR"]
)


@router.post("/{persona_id}")
def generar_qr(
    persona_id: str,
    db: Session = Depends(get_db)
):
    return QRService.generar_qr(
        db,
        persona_id
    )