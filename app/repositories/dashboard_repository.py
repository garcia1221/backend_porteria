from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.movimiento import Movimiento


class DashboardRepository:

    @staticmethod
    def total_entradas_hoy(
        db: Session
    ):
        return (
            db.query(Movimiento)
            .filter(
                Movimiento.tipo_movimiento == "entrada"
            )
            .count()
        )

    @staticmethod
    def total_salidas_hoy(
        db: Session
    ):
        return (
            db.query(Movimiento)
            .filter(
                Movimiento.tipo_movimiento == "salida"
            )
            .count()
        )
        
    @staticmethod
    def obtener_movimientos(
        db: Session
    ):
        return (
            db.query(Movimiento)
            .order_by(
                Movimiento.fecha_hora.desc()
            )
            .all()
        )