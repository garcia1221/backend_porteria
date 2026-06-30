from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.database.database import Base


class Movimiento(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True)

    fk_persona = Column(String(36), nullable=False)

    tipo_movimiento = Column(
        String(20),
        nullable=False
    )

    observacion = Column(
        String(255),
        nullable=True
    )

    fecha_hora = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )