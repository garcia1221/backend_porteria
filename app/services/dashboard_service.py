from app.repositories.dashboard_repository import (
    DashboardRepository
)


class DashboardService:

    @staticmethod
    def resumen(db):
        entradas = DashboardRepository.total_entradas_hoy(db)
        salidas = DashboardRepository.total_salidas_hoy(db)
        personas_dentro = entradas - salidas
        
        # Calcular visitantes externos
        personas_actuales = DashboardService.personas_dentro(db)
        externos = sum(1 for p in personas_actuales if p.get("rol", "").lower() == "externo")

        return {
            "personas_dentro": personas_dentro,
            "entradas_hoy": entradas,
            "salidas_hoy": salidas,
            "visitantes_externos": externos
        }
        
    @staticmethod
    def personas_dentro(db):
        movimientos = DashboardRepository.obtener_movimientos(db)
        personas = {}
    
        for movimiento in movimientos:
            if movimiento.fk_persona not in personas:
                personas[movimiento.fk_persona] = movimiento
    
        resultado = []
        from app.services.sena_service import SenaService
        from app.repositories.equipo_repository import EquipoRepository
    
        for persona_id, movimiento in personas.items():
            if movimiento.tipo_movimiento == "entrada":
                detalles = SenaService.obtener_persona_local_o_sena(db, persona_id)
                equipos = EquipoRepository.obtener_por_persona(db, persona_id)
                equipo_principal = "Ninguno"
                equipos_data = []
                if equipos:
                    equipo_principal = f"{equipos[0].marca} {equipos[0].modelo}"
                    for eq in equipos:
                        equipos_data.append({
                            "id": eq.id,
                            "marca": eq.marca,
                            "modelo": eq.modelo,
                            "serial": eq.serial,
                            "tipo_equipo": eq.tipo_equipo,
                            "estado": eq.estado
                        })
                    
                resultado.append(
                    {
                        "fk_persona": persona_id,
                        "nombre": detalles["nombre"],
                        "documento": detalles.get("documento", ""),
                        "rol": detalles["rol"],
                        "ultimo_movimiento": movimiento.tipo_movimiento,
                        "fecha_hora": movimiento.fecha_hora,
                        "equipo_principal": equipo_principal,
                        "equipos": equipos_data
                    }
                )
    
        return resultado