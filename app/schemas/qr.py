from pydantic import BaseModel


class QRCreate(BaseModel):
    fk_persona: int