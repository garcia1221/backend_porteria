from sqlalchemy.orm import Session
from app.models.accesorio import Accesorio


class AccesorioRepository:

    @staticmethod
    def crear(db: Session, accesorio: Accesorio):
        db.add(accesorio)
        db.commit()
        db.refresh(accesorio)
        return accesorio

    @staticmethod
    def listar_por_equipo(
        db: Session,
        equipo_id: int
    ):
        return db.query(Accesorio).filter(
            Accesorio.fk_equipo == equipo_id
        ).all()
        
        
        
    @staticmethod
    def obtener_por_equipo(
        db: Session,
        equipo_id: int
    ):
        return db.query(
            Accesorio
        ).filter(
            Accesorio.fk_equipo == equipo_id
        ).all()
        
        
    @staticmethod
    def obtener_por_equipo(
        db: Session,
        equipo_id: int
    ):
        return (
            db.query(Accesorio)
            .filter(
                Accesorio.fk_equipo == equipo_id
            )
            .all()
        )