from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.services.dashboard_service import (
    DashboardService
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/resumen")
def resumen(
    db: Session = Depends(get_db)
):
    return DashboardService.resumen(
        db
    )
    
    
@router.get("/personas-dentro")
def personas_dentro(
    db: Session = Depends(get_db)
):
    return DashboardService.personas_dentro(
        db
    )