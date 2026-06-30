from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.equipo import Equipo
from app.schemas.equipo import EquipoCreate
from app.database.session import get_db

router = APIRouter(
    prefix="/equipos",
    tags=["Equipos"]
)

@router.post("/")
def crear_equipo(
    data: EquipoCreate,
    db: Session = Depends(get_db)
):
    # Intentar resolver la cédula al UUID de la persona
    fk_persona = data.fk_persona
    from app.database.sena_db import buscar_persona_por_cedula
    persona = buscar_persona_por_cedula(fk_persona)
    if persona:
        fk_persona = persona["fk_persona"]
    else:
        # Intentar buscar en externos locales por cédula/documento
        from app.models.usuario_externo import UsuarioExterno
        externo = db.query(UsuarioExterno).filter(UsuarioExterno.documento == fk_persona).first()
        if externo:
            fk_persona = str(externo.id)

    equipo = Equipo(
        fk_persona=fk_persona,
        tipo_equipo=data.tipo_equipo,
        marca=data.marca,
        modelo=data.modelo,
        serial=data.serial
    )
    db.add(equipo)
    db.commit()
    db.refresh(equipo)
    return equipo

@router.get("/")
def listar_equipos(
    db: Session = Depends(get_db),
    tipo_equipo: str = None,
    fk_persona: str = None,
    estado: str = None
):
    query = db.query(Equipo)
    if tipo_equipo:
        query = query.filter(Equipo.tipo_equipo == tipo_equipo)
    
    if fk_persona:
        import re
        is_uuid = bool(re.match(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", fk_persona))
        
        if is_uuid:
            query = query.filter(Equipo.fk_persona == fk_persona)
        else:
            # Buscar en erp_sena por nombre o cédula
            from app.database.sena_db import buscar_personas_por_filtro
            personas_sena = buscar_personas_por_filtro(fk_persona)
            sena_ids = [p["fk_persona"] for p in personas_sena]
            
            # Buscar en externos locales por nombre o cédula
            from app.models.usuario_externo import UsuarioExterno
            externos = db.query(UsuarioExterno).filter(
                (UsuarioExterno.documento.ilike(f"%{fk_persona}%")) |
                (UsuarioExterno.nombre.ilike(f"%{fk_persona}%"))
            ).all()
            externo_ids = [str(ext.id) for ext in externos]
            
            matching_ids = sena_ids + externo_ids
            matching_ids.append(fk_persona)
            
            query = query.filter(Equipo.fk_persona.in_(matching_ids))

    if estado:
        query = query.filter(Equipo.estado == estado)
        
    equipos = query.all()
    
    # Enriquecer los equipos con nombre y cédula del propietario
    from app.database.sena_db import buscar_persona_por_uuid
    from app.repositories.usuario_externo_repository import UsuarioExternoRepository
    
    resultado = []
    for eq in equipos:
        nombre = ""
        cedula = ""
        
        # Intentar en erp_sena
        persona_info = buscar_persona_por_uuid(eq.fk_persona)
        if persona_info:
            nombre = persona_info["nombre"]
            cedula = persona_info["documento"]
        else:
            # Intentar en externos locales
            if eq.fk_persona.isdigit():
                ext = UsuarioExternoRepository.obtener_por_id(db, int(eq.fk_persona))
                if ext:
                    nombre = ext.nombre
                    cedula = ext.documento
        
        resultado.append({
            "id": eq.id,
            "fk_persona": eq.fk_persona,
            "nombre_propietario": nombre,
            "cedula_propietario": cedula,
            "tipo_equipo": eq.tipo_equipo,
            "marca": eq.marca,
            "modelo": eq.modelo,
            "serial": eq.serial,
            "estado": eq.estado,
            "fecha_registro": eq.fecha_registro
        })
        
    return resultado


@router.get("/persona/{persona_id}")
def equipos_persona(
    persona_id: str,
    db: Session = Depends(get_db)
):
    return db.query(Equipo).filter(Equipo.fk_persona == persona_id).all()

@router.get("/{equipo_id}")
def obtener_equipo(
    equipo_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Equipo).filter(Equipo.id == equipo_id).first()

@router.put("/{equipo_id}")
def editar_equipo(
    equipo_id: int,
    data: dict,
    db: Session = Depends(get_db)
):
    equipo = db.query(Equipo).filter(Equipo.id == equipo_id).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
        
    if "marca" in data:
        equipo.marca = data["marca"]
    if "modelo" in data:
        equipo.modelo = data["modelo"]
    if "serial" in data:
        equipo.serial = data["serial"]
    if "estado" in data:
        equipo.estado = data["estado"]
        
    db.commit()
    db.refresh(equipo)
    return equipo

@router.delete("/{equipo_id}")
def eliminar_equipo(
    equipo_id: int,
    db: Session = Depends(get_db)
):
    equipo = db.query(Equipo).filter(Equipo.id == equipo_id).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
        
    db.delete(equipo)
    db.commit()
    return {"success": True, "message": "Equipo eliminado"}