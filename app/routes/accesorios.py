from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.accesorio import (
    AccesorioCreate
)

from app.services.accesorio_service import (
    AccesorioService
)

router = APIRouter(
    prefix="/accesorios",
    tags=["Accesorios"]
)


@router.post("/")
def crear_accesorio(
    data: AccesorioCreate,
    db: Session = Depends(get_db)
):
    return AccesorioService.crear_accesorio(
        db,
        data
    )


@router.get("/equipo/{equipo_id}")
def listar_accesorios(
    equipo_id: int,
    db: Session = Depends(get_db)
):
    return AccesorioService.listar_por_equipo(
        db,
        equipo_id
    )