from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional
from app.database.session import get_db
from app.repositories.movimiento_repository import MovimientoRepository
from app.repositories.equipo_repository import EquipoRepository
from app.services.sena_service import SenaService

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)


@router.get("/movimientos")
def reportes_movimientos(
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    tipo_movimiento: Optional[str] = Query(None),
    persona: Optional[str] = Query(None),
    fk_persona: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    import traceback
    import sys
    try:
        dt_inicio = None
        if fecha_inicio:
            dt_inicio = datetime.combine(fecha_inicio, datetime.min.time())

        dt_fin = None
        if fecha_fin:
            dt_fin = datetime.combine(fecha_fin, datetime.max.time())

        persona_id = fk_persona or persona
        matching_ids = None

        if persona_id:
            import re
            is_uuid = bool(re.match(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", persona_id))
            
            if is_uuid:
                # Match exacto de UUID (para la app móvil)
                matching_ids = [persona_id]
            else:
                # Búsqueda general por nombre o documento/cédula (para la web)
                from app.database.sena_db import buscar_personas_por_filtro
                personas_sena = buscar_personas_por_filtro(persona_id)
                sena_ids = [p["fk_persona"] for p in personas_sena]
                
                from app.models.usuario_externo import UsuarioExterno
                externos = db.query(UsuarioExterno).filter(
                    (UsuarioExterno.documento.ilike(f"%{persona_id}%")) |
                    (UsuarioExterno.nombre.ilike(f"%{persona_id}%"))
                ).all()
                externo_ids = [str(ext.id) for ext in externos]
                
                matching_ids = sena_ids + externo_ids
                # También añadir el término original en caso de que sea un ID directo
                matching_ids.append(persona_id)

        movimientos = MovimientoRepository.filtrar_movimientos(
            db,
            fecha_inicio=dt_inicio,
            fecha_fin=dt_fin,
            tipo_movimiento=tipo_movimiento,
            fk_persona=matching_ids if matching_ids is not None else None
        )

        resultado = []
        for mov in movimientos:
            detalles = SenaService.obtener_persona_local_o_sena(db, mov.fk_persona)
            equipos = EquipoRepository.obtener_por_persona(db, mov.fk_persona)
            
            # Calcular el estado actual de la persona basado en su último movimiento global
            ultimo_mov = MovimientoRepository.obtener_ultimo_movimiento(db, mov.fk_persona)
            estado_actual = "Fuera"
            if ultimo_mov and ultimo_mov.tipo_movimiento == "entrada":
                estado_actual = "Dentro"

            resultado.append({
                "id": mov.id,
                "fk_persona": mov.fk_persona,
                "nombre": detalles["nombre"],
                "documento": detalles["documento"],
                "rol": detalles["rol"],
                "programa": detalles["programa"],
                "tipo_movimiento": mov.tipo_movimiento,
                "observacion": mov.observacion,
                "fecha_hora": mov.fecha_hora,
                "estado_actual": estado_actual,
                "equipos": [{"marca": eq.marca, "modelo": eq.modelo, "tipo_equipo": eq.tipo_equipo} for eq in equipos]
            })
        return resultado
    except Exception as e:
        with open("error_trace.txt", "w") as f:
            traceback.print_exc(file=f)
        raise e
