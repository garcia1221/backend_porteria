from sqlalchemy.orm import Session
from app.models.equipo import Equipo


class EquipoRepository:

    @staticmethod
    def crear(db: Session, equipo: Equipo):
        db.add(equipo)
        db.commit()
        db.refresh(equipo)
        return equipo

    @staticmethod
    def listar(db: Session):
        return db.query(Equipo).all()

    @staticmethod
    def obtener_por_id(db: Session, equipo_id: int):
        return db.query(Equipo).filter(
            Equipo.id == equipo_id
        ).first()
        
    @staticmethod
    def obtener_por_persona(
        db: Session,
        persona_id: str
    ):
        return (
            db.query(Equipo)
            .filter(
                Equipo.fk_persona == persona_id
            )
            .all()
        )