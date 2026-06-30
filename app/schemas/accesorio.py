from pydantic import BaseModel


class AccesorioCreate(BaseModel):
    fk_equipo: int
    tipo: str
    descripcion: str


class AccesorioResponse(BaseModel):
    id: int
    fk_equipo: int
    tipo: str
    descripcion: str

    class Config:
        from_attributes = True