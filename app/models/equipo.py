from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.database import Base


class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)

    fk_persona = Column(String(100), nullable=False)

    tipo_equipo = Column(String(50), nullable=False)

    marca = Column(String(100), nullable=False)

    modelo = Column(String(100), nullable=False)

    serial = Column(String(100), nullable=False)

    estado = Column(
        String(20),
        default="pendiente"
    )

    fecha_registro = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )