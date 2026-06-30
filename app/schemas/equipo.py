from pydantic import BaseModel


class EquipoCreate(BaseModel):
    fk_persona: str
    tipo_equipo: str
    marca: str
    modelo: str
    serial: str


class EquipoResponse(BaseModel):
    id: int
    fk_persona: str
    tipo_equipo: str
    marca: str
    modelo: str
    serial: str
    estado: str

    class Config:
        from_attributes = True