from fastapi import HTTPException

from app.models.usuario_externo import (
    UsuarioExterno
)

from app.repositories.usuario_externo_repository import (
    UsuarioExternoRepository
)


class UsuarioExternoService:

    @staticmethod
    def crear(
        db,
        data
    ):

        empresa_val = data.empresa.strip() if data.empresa else "Particular"
        if not empresa_val:
            empresa_val = "Particular"

        usuario = UsuarioExterno(
            documento=data.documento,
            nombre=data.nombre,
            empresa=empresa_val
        )

        return UsuarioExternoRepository.crear(
            db,
            usuario
        )

    @staticmethod
    def listar(db):
        return UsuarioExternoRepository.listar(db)

    @staticmethod
    def actualizar(
        db,
        usuario_id,
        data
    ):

        usuario = (
            UsuarioExternoRepository.obtener_por_id(
                db,
                usuario_id
            )
        )

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        empresa_val = data.empresa.strip() if data.empresa else "Particular"
        if not empresa_val:
            empresa_val = "Particular"

        usuario.documento = data.documento
        usuario.nombre = data.nombre
        usuario.empresa = empresa_val
        usuario.estado = data.estado

        return UsuarioExternoRepository.actualizar(
            db,
            usuario
        )