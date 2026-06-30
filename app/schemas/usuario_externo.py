from pydantic import BaseModel
from typing import Optional

class UsuarioExternoCreate(BaseModel):
    documento: str
    nombre: str
    empresa: Optional[str] = ""

class UsuarioExternoUpdate(BaseModel):
    documento: str
    nombre: str
    empresa: Optional[str] = ""
    estado: str

class UsuarioExternoResponse(BaseModel):
    id: int
    documento: str
    nombre: str
    empresa: Optional[str] = ""
    estado: str

    class Config:
        from_attributes = True