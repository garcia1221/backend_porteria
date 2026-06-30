import requests
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.repositories.usuario_externo_repository import UsuarioExternoRepository

load_dotenv()


class SenaService:

    BASE_URL = os.getenv(
        "NEST_API_URL"
    )

    @staticmethod
    def obtener_persona_local_o_sena(db: Session, persona_id: str):
        # 1. Intentar buscar como Usuario Externo local (por documento o ID)
        from app.models.usuario_externo import UsuarioExterno
        if persona_id:
            query = db.query(UsuarioExterno).filter(UsuarioExterno.documento == str(persona_id))
            if isinstance(persona_id, int) or (isinstance(persona_id, str) and persona_id.isdigit()):
                query = db.query(UsuarioExterno).filter(
                    (UsuarioExterno.documento == str(persona_id)) | 
                    (UsuarioExterno.id == int(persona_id))
                )
            externo = query.first()
            if externo:
                return {
                    "id": str(externo.id),
                    "nombre": externo.nombre,
                    "documento": externo.documento,
                    "rol": "externo",
                    "programa": externo.empresa,
                    "tipo_propietario": "externo"
                }

        # 2. Intentar buscar en BD SENA (NestJS)
        if persona_id:
            try:
                # Si es numérico, buscar por cédula, de lo contrario buscar por ID (UUID)
                if str(persona_id).isdigit():
                    url = f"{SenaService.BASE_URL}/personas/cedula/{persona_id}"
                else:
                    url = f"{SenaService.BASE_URL}/personas/{persona_id}"
                    
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    programa = "Ninguno"
                    matriculas = data.get("matriculas", [])
                    if matriculas:
                        curso = matriculas[0].get("curso")
                        if curso:
                            prog = curso.get("programa")
                            if prog:
                                programa = prog.get("nombre", "Ninguno")
                    
                    return {
                        "id": data.get("idPersona"),
                        "nombre": data.get("nombre"),
                        "documento": str(data.get("cedula")),
                        "rol": data.get("cargo", "aprendiz"),
                        "programa": programa,
                        "tipo_propietario": data.get("cargo", "aprendiz"),
                        "correo": data.get("correo"),
                        "telefono": str(data.get("telefono") or "")
                    }
            except Exception as e:
                print(f"Error consultando BD SENA para {persona_id}: {e}")

        return {
            "id": persona_id,
            "nombre": f"Desconocido ({persona_id})",
            "documento": "",
            "rol": "desconocido",
            "programa": "Ninguno",
            "tipo_propietario": "desconocido"
        }