from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.database.database import Base


class Accesorio(Base):
    __tablename__ = "accesorios"

    id = Column(Integer, primary_key=True)

    fk_equipo = Column(
        Integer,
        ForeignKey("equipos.id")
    )

    tipo = Column(String(50))

    descripcion = Column(String(255))