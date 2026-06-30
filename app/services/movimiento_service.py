from app.models.movimiento import Movimiento
from fastapi import HTTPException
from app.repositories.movimiento_repository import MovimientoRepository
from app.database.sena_db import buscar_persona_por_uuid


class MovimientoService:

    @staticmethod
    def crear_movimiento(db, data):
        ultimo = MovimientoRepository.obtener_ultimo_movimiento(db, data.fk_persona)
    
        if ultimo:
            if ultimo.tipo_movimiento == "entrada" and data.tipo_movimiento == "entrada":
                raise HTTPException(
                    status_code=400,
                    detail="Debe registrar una salida antes de otra entrada"
                )
            if ultimo.tipo_movimiento == "salida" and data.tipo_movimiento == "salida":
                raise HTTPException(
                    status_code=400,
                    detail="Debe registrar una entrada antes de otra salida"
                )
    
        movimiento = Movimiento(
            fk_persona=data.fk_persona,
            tipo_movimiento=data.tipo_movimiento,
            observacion=data.observacion
        )
        return MovimientoRepository.crear(db, movimiento)


    @staticmethod
    def listar_movimientos(db):
        return MovimientoRepository.listar(db)


    @staticmethod
    def movimientos_persona(db, persona_id):
        return MovimientoRepository.obtener_por_persona(db, persona_id)
        
        
    @staticmethod
    def historial(db):
        movimientos = MovimientoRepository.obtener_todos(db)
        resultado = []

        for movimiento in movimientos:
            # Resolver nombre y cedula desde BD SENA
            persona_info = buscar_persona_por_uuid(str(movimiento.fk_persona))
            nombre = persona_info.get("nombre", "") if persona_info else ""
            cedula = persona_info.get("documento", "") if persona_info else ""
            
            resultado.append({
                "id": movimiento.id,
                "fk_persona": str(movimiento.fk_persona),
                "nombre": nombre,
                "cedula": cedula,
                "tipo_movimiento": movimiento.tipo_movimiento,
                "fecha_hora": movimiento.fecha_hora
            })

        return resultado
    
    @staticmethod
    def historial_persona(db, persona_id):
        movimientos = MovimientoRepository.obtener_por_persona(db, persona_id)
        resultado = []
    
        for movimiento in movimientos:
            resultado.append({
                "id": movimiento.id,
                "tipo_movimiento": movimiento.tipo_movimiento,
                "fecha_hora": movimiento.fecha_hora
            })
    
        return resultado