from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.database.database import Base


class QRUsuario(Base):
    __tablename__ = "qr_usuario"

    id = Column(Integer, primary_key=True)

    fk_persona = Column(String(100), nullable=False)

    codigo_qr = Column(String(255), unique=True)

    activo = Column(Boolean, default=True)

    fecha_generacion = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )