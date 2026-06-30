from app.models.equipo import Equipo
from app.repositories.equipo_repository import EquipoRepository


class EquipoService:

    @staticmethod
    def crear_equipo(db, data):

        equipo = Equipo(
            fk_persona=data.fk_persona,
            tipo_equipo=data.tipo_equipo,
            marca=data.marca,
            modelo=data.modelo,
            serial=data.serial
        )

        return EquipoRepository.crear(
            db,
            equipo
        )

    @staticmethod
    def listar_equipos(db):
        return EquipoRepository.listar(db)

    @staticmethod
    def obtener_equipo(db, equipo_id):
        return EquipoRepository.obtener_por_id(
            db,
            equipo_id
        )