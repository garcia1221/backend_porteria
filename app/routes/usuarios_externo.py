from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.usuario_externo import (
    UsuarioExternoCreate,
    UsuarioExternoUpdate
)

from app.services.usuario_externo_service import (
    UsuarioExternoService
)

router = APIRouter(
    prefix="/externos",
    tags=["Usuarios Externos"]
)


@router.post("/")
def crear(
    data: UsuarioExternoCreate,
    db: Session = Depends(get_db)
):
    return UsuarioExternoService.crear(
        db,
        data
    )


@router.get("/")
def listar(
    db: Session = Depends(get_db)
):
    return UsuarioExternoService.listar(
        db
    )


@router.put("/{usuario_id}")
def actualizar(
    usuario_id: int,
    data: UsuarioExternoUpdate,
    db: Session = Depends(get_db)
):
    return UsuarioExternoService.actualizar(
        db,
        usuario_id,
        data
    )