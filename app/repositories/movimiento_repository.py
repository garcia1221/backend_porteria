from sqlalchemy.orm import Session

from app.models.movimiento import Movimiento


class MovimientoRepository:

    @staticmethod
    def crear(
        db: Session,
        movimiento: Movimiento
    ):
        db.add(movimiento)
        db.commit()
        db.refresh(movimiento)

        return movimiento

    @staticmethod
    def listar(
        db: Session
    ):
        return db.query(
            Movimiento
        ).order_by(
            Movimiento.id.desc()
        ).all()

    @staticmethod
    def obtener_por_persona(
        db: Session,
        persona_id: int
    ):
        return db.query(
            Movimiento
        ).filter(
            Movimiento.fk_persona == persona_id
        ).all()
        
    
    @staticmethod
    def obtener_ultimo_movimiento(
        db: Session,
        persona_id: str
    ):
        return (
            db.query(Movimiento)
        .filter(
            Movimiento.fk_persona == persona_id
        )
        .order_by(
            Movimiento.fecha_hora.desc()
        )
        .first()
    )
        
        
    @staticmethod
    def obtener_todos(
        db: Session
    ):
        return (
            db.query(Movimiento)
            .order_by(
                Movimiento.fecha_hora.desc()
            )
            .all()
        )
        
        
    @staticmethod
    def obtener_por_persona(
        db: Session,
        persona_id: str
    ):
        return (
            db.query(Movimiento)
            .filter(
                Movimiento.fk_persona == persona_id
            )
            .order_by(
                Movimiento.fecha_hora.desc()
            )
            .all()
        )
        
    @staticmethod
    def filtrar_movimientos(
        db: Session,
        fecha_inicio=None,
        fecha_fin=None,
        tipo_movimiento=None,
        fk_persona=None
    ):
        query = db.query(Movimiento)
        if fecha_inicio:
            query = query.filter(Movimiento.fecha_hora >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Movimiento.fecha_hora <= fecha_fin)
        if tipo_movimiento:
            query = query.filter(Movimiento.tipo_movimiento == tipo_movimiento)
        if fk_persona:
            if isinstance(fk_persona, list):
                query = query.filter(Movimiento.fk_persona.in_(fk_persona))
            else:
                query = query.filter(Movimiento.fk_persona == fk_persona)
        return query.order_by(Movimiento.fecha_hora.desc()).all()
        
 