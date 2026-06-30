from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database.session import get_db
from app.database.sena_db import buscar_persona_por_cedula
from app.repositories.usuario_externo_repository import UsuarioExternoRepository

router = APIRouter(
    prefix="/personas",
    tags=["Personas"]
)


@router.get("/identificacion/{cedula}")
def identificar_por_cedula(cedula: str, db: Session = Depends(get_db)):
    """
    Busca una persona por número de cédula/documento.
    Primero revisa la BD SENA (erp_sena), luego en usuarios externos.
    Usado principalmente por la app móvil para el login.
    """
    # 1. Buscar en BD SENA (erp_sena.personas)
    persona = buscar_persona_por_cedula(cedula)
    if persona:
        return persona

    # 2. Buscar en usuarios externos locales
    externos = db.execute(
        __import__("sqlalchemy").text(
            "SELECT id, nombre, documento, correo, telefono, empresa FROM usuarios_externos WHERE documento = :doc LIMIT 1"
        ),
        {"doc": cedula}
    ).fetchone()

    if externos:
        return {
            "fk_persona": str(externos[0]),
            "nombre": externos[1],
            "documento": str(externos[2]),
            "correo": externos[3] or "",
            "telefono": str(externos[4] or ""),
            "rol": "externo",
            "programa": externos[5] or "Externo"
        }

    raise HTTPException(status_code=404, detail="Usuario no encontrado")


from pydantic import BaseModel
from typing import Optional

class AprendizCreate(BaseModel):
    nombre: str
    cedula: str
    correo: str
    telefono: Optional[str] = None

@router.get("/buscar")
def buscar_personas(q: str, db: Session = Depends(get_db)):
    """
    Busca personas por nombre o documento para el autocompletado en el frontend.
    """
    if not q or len(q) < 2:
        return []
    
    resultados = []
    
    # 1. Buscar en BD SENA
    from app.database.sena_db import buscar_personas_por_filtro
    personas_sena = buscar_personas_por_filtro(q)
    for p in personas_sena:
        resultados.append({
            "id": p["fk_persona"],
            "nombre": p["nombre"],
            "documento": p["documento"],
            "rol": "aprendiz"
        })
        
    # 2. Buscar en BD local (Usuarios externos)
    from app.models.usuario_externo import UsuarioExterno
    externos = db.query(UsuarioExterno).filter(
        (UsuarioExterno.documento.ilike(f"%{q}%")) |
        (UsuarioExterno.nombre.ilike(f"%{q}%"))
    ).limit(15).all()
    
    for ext in externos:
        resultados.append({
            "id": str(ext.id),
            "nombre": ext.nombre,
            "documento": ext.documento,
            "rol": "externo"
        })
        
    # Eliminar duplicados basados en documento
    vistos = set()
    unicos = []
    for r in resultados:
        if r["documento"] not in vistos:
            vistos.add(r["documento"])
            unicos.append(r)
            
    return unicos[:15]

@router.get("/aprendices")
def get_aprendices():
    from app.database.sena_db import listar_aprendices
    return listar_aprendices()

@router.post("/aprendices")
def create_aprendiz(data: AprendizCreate):
    from app.database.sena_db import buscar_persona_por_cedula, crear_aprendiz
    existente = buscar_persona_por_cedula(data.cedula)
    if existente:
        raise HTTPException(status_code=400, detail="El aprendiz ya existe")
    
    nuevo = crear_aprendiz(data.nombre, data.cedula, data.correo, data.telefono)
    if not nuevo:
        raise HTTPException(status_code=500, detail="Error creando aprendiz")
    return nuevo
