from app.repositories.qr_repository import QRRepository
from app.repositories.equipo_repository import EquipoRepository
from app.repositories.accesorio_repository import AccesorioRepository
from app.repositories.movimiento_repository import MovimientoRepository


class PorteriaService:

    @staticmethod
    def scan(
        db,
        codigo_qr
    ):

        fk_persona = None
        qr = QRRepository.obtener_por_codigo(
            db,
            codigo_qr
        )

        from app.services.sena_service import SenaService

        if qr:
            fk_persona = qr.fk_persona
        else:
            # Si no es un QR válido, intentar buscar si es un documento / cédula ingresado manualmente
            persona_detalles = SenaService.obtener_persona_local_o_sena(db, codigo_qr)
            if persona_detalles and "Desconocido" not in persona_detalles.get("nombre", ""):
                fk_persona = persona_detalles.get("id") or codigo_qr
            else:
                return {
                    "success": False,
                    "message": "QR o Documento no registrado en el sistema"
                }

        equipos = EquipoRepository.obtener_por_persona(
            db,
            fk_persona
        )

        resultado_equipos = []

        for equipo in equipos:

            accesorios = (
                AccesorioRepository.obtener_por_equipo(
                    db,
                    equipo.id
                )
            )

            resultado_equipos.append(
                {
                    "id": equipo.id,
                    "marca": equipo.marca,
                    "modelo": equipo.modelo,
                    "serial": equipo.serial,
                    "estado": equipo.estado,
                    "tipo_equipo": equipo.tipo_equipo,
                    "accesorios": accesorios
                }
            )

        ultimo = (
            MovimientoRepository.obtener_ultimo_movimiento(
                db,
                fk_persona
            )
        )

        movimiento = "entrada"

        if ultimo:
            if ultimo.tipo_movimiento == "entrada":
                movimiento = "salida"

        persona_detalles = SenaService.obtener_persona_local_o_sena(db, fk_persona)

        return {
            "success": True,
            "fk_persona": fk_persona,
            "nombre": persona_detalles["nombre"],
            "documento": persona_detalles["documento"],
            "rol": persona_detalles["rol"],
            "programa": persona_detalles["programa"],
            "movimiento_sugerido": movimiento,
            "equipos": resultado_equipos
        }
        
        
    @staticmethod
    def confirmar(
        db,
        fk_persona,
        tipo_movimiento
    ):
    
        from app.models.movimiento import Movimiento
    
        movimiento = Movimiento(
            fk_persona=fk_persona,
            tipo_movimiento=tipo_movimiento
        )
    
        db.add(movimiento)
        db.commit()
        db.refresh(movimiento)
    
        return {
            "success": True,
            "message": "Movimiento registrado",
            "id": movimiento.id
        }