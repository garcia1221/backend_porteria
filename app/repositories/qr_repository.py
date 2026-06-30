from sqlalchemy.orm import Session
from app.models.qr_usuario import QRUsuario


class QRRepository:

    @staticmethod
    def obtener_por_persona(
        db: Session,
        persona_id: str
    ):
        return db.query(QRUsuario).filter(
            QRUsuario.fk_persona == persona_id
        ).first()

    @staticmethod
    def crear(
        db: Session,
        qr: QRUsuario
    ):
        db.add(qr)
        db.commit()
        db.refresh(qr)
        return qr
    
    @staticmethod
    def obtener_por_codigo(
        db: Session,
        codigo: str
    ):
        return (
            db.query(QRUsuario)
            .filter(
                QRUsuario.codigo_qr == codigo
            )
            .first()
        )