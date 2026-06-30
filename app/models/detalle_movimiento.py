from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from app.database.database import Base


class DetalleMovimiento(Base):
    __tablename__ = "detalle_movimiento"

    id = Column(Integer, primary_key=True)

    fk_movimiento = Column(
        Integer,
        ForeignKey("movimientos.id")
    )

    fk_equipo = Column(
        Integer,
        ForeignKey("equipos.id")
    )