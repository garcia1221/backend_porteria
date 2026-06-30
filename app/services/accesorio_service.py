from app.models.accesorio import Accesorio
from app.repositories.accesorio_repository import (
    AccesorioRepository
)


class AccesorioService:

    @staticmethod
    def crear_accesorio(
        db,
        data
    ):
        accesorio = Accesorio(
            fk_equipo=data.fk_equipo,
            tipo=data.tipo,
            descripcion=data.descripcion
        )

        return AccesorioRepository.crear(
            db,
            accesorio
        )

    @staticmethod
    def listar_por_equipo(
        db,
        equipo_id
    ):
        return AccesorioRepository.listar_por_equipo(
            db,
            equipo_id
        )