from pydantic import BaseModel


class ScanQRRequest(BaseModel):
    codigo_qr: str


class ConfirmarMovimientoRequest(BaseModel):
    fk_persona: str
    tipo_movimiento: str
    
