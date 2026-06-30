from pydantic import BaseModel
from typing import Optional


class MovimientoCreate(BaseModel):
    fk_persona: int
    tipo_movimiento: str
    observacion: Optional[str] = None