from sqlalchemy.orm import Session

from app.models.usuario_externo import (
    UsuarioExterno
)


class UsuarioExternoRepository:

    @staticmethod
    def crear(
        db: Session,
        usuario: UsuarioExterno
    ):
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        return usuario

    @staticmethod
    def listar(
        db: Session
    ):
        return db.query(
            UsuarioExterno
        ).all()

    @staticmethod
    def obtener_por_id(
        db: Session,
        usuario_id: int
    ):
        return db.query(
            UsuarioExterno
        ).filter(
            UsuarioExterno.id == usuario_id
        ).first()

    @staticmethod
    def actualizar(
        db: Session,
        usuario
    ):
        db.commit()
        db.refresh(usuario)

        return usuario