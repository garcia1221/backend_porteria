import uuid

from app.models.qr_usuario import QRUsuario

from app.repositories.qr_repository import (
    QRRepository
)


class QRService:

    @staticmethod
    def generar_qr(
        db,
        persona_id
    ):

        existente = QRRepository.obtener_por_persona(
            db,
            persona_id
        )

        if existente:
            return existente

        codigo = str(uuid.uuid4())

        qr = QRUsuario(
            fk_persona=persona_id,
            codigo_qr=codigo
        )

        return QRRepository.crear(
            db,
            qr
        )