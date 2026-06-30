from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.database import Base


class UsuarioExterno(Base):
    __tablename__ = "usuarios_externos"

    id = Column(Integer, primary_key=True)

    documento = Column(String(50), unique=True)

    nombre = Column(String(200))

    empresa = Column(String(200))

    estado = Column(String(20), default="activo")