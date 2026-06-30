import os
from sqlalchemy.orm import Session
from sqlalchemy import text
import uuid
import random
from datetime import datetime, timedelta

from app.database.database import engine, Base, SessionLocal
from app.database.sena_db import sena_engine
from app.models.usuario_externo import UsuarioExterno
from app.models.equipo import Equipo
from app.models.movimiento import Movimiento
from app.models.detalle_movimiento import DetalleMovimiento

def reset_local_db():
    print("Recreando tablas locales (control_equipos)...")
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE;"))
        conn.execute(text("CREATE SCHEMA public;"))
    
    # We must also import all models so create_all creates them
    from app.models.accesorio import Accesorio
    from app.models.qr_usuario import QRUsuario
    
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # 1. Crear 10 Usuarios Externos
    print("Creando 10 Usuarios Externos...")
    externos = []
    for i in range(1, 11):
        ext = UsuarioExterno(
            documento=f"9000{i:04d}",
            nombre=f"Visitante Externo {i}",
            correo=f"visitante{i}@empresa.com",
            telefono=f"30012345{i:02d}"
        )
        db.add(ext)
        externos.append(ext)
    db.commit()

    # Necesitamos algunos IDs de personas del ERP SENA para equipos/movimientos
    # Buscamos 5 aprendices de la base de datos de SENA para usarlos
    with sena_engine.connect() as conn:
        result = conn.execute(text('SELECT "idPersona" FROM public.personas LIMIT 10'))
        sena_ids = [str(row[0]) for row in result.fetchall()]

    todas_personas = sena_ids + [str(e.id) for e in externos]
    
    if not todas_personas:
        print("ERROR: No hay personas en la BD SENA. Por favor corre reset_db.py de nuevo después de poblarla.")
        return

    # 2. Crear 10 Equipos
    print("Creando 10 Equipos...")
    equipos = []
    marcas = ["HP", "Dell", "Lenovo", "Asus", "Acer"]
    for i in range(1, 11):
        fk_persona = random.choice(todas_personas)
        eq = Equipo(
            fk_persona=fk_persona,
            tipo_equipo="Computador",
            marca=random.choice(marcas),
            modelo=f"Laptop Pro {i}",
            serial=f"SN-{uuid.uuid4().hex[:8].upper()}",
            estado="aprobado"
        )
        db.add(eq)
        equipos.append(eq)
        db.commit()
        db.refresh(eq)
        
        # Crear 1 o 2 accesorios para este equipo
        from app.models.accesorio import Accesorio
        for j in range(random.randint(1, 2)):
            tipos_acc = ["Cargador", "Mouse", "Maletín", "Base refrigerante"]
            acc = Accesorio(
                fk_equipo=eq.id,
                tipo=random.choice(tipos_acc),
                descripcion=f"Accesorio de prueba {j+1}"
            )
            db.add(acc)
    db.commit()

    # 3. Crear 10 Movimientos y sus Detalles
    print("Creando 10 Movimientos con sus detalles...")
    for i in range(1, 11):
        # Seleccionamos una persona al azar que tenga equipos
        eq_aleatorio = random.choice(equipos)
        fk_persona = eq_aleatorio.fk_persona
        
        # Determinar el rol
        rol = "externo" if fk_persona in [str(e.id) for e in externos] else "aprendiz"
        
        es_entrada = i % 2 == 0
        mov = Movimiento(
            fk_persona=fk_persona,
            tipo_movimiento="entrada" if es_entrada else "salida",
            observacion=f"Movimiento de prueba {i}",
            fecha_hora=datetime.now() - timedelta(hours=random.randint(1, 24))
        )
        db.add(mov)
        db.commit()
        db.refresh(mov)
        
        # Agregar el detalle de movimiento (qué equipo entró/salió)
        det = DetalleMovimiento(
            fk_movimiento=mov.id,
            fk_equipo=eq_aleatorio.id
        )
        db.add(det)
        db.commit()

    db.close()
    print("Base de datos local poblada correctamente.")

def reset_sena_db():
    print("Limpiando y poblando tabla personas en ERP SENA...")
    with sena_engine.begin() as conn:
        # Para evitar problemas con foreign keys o si la tabla no existe
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS public.personas (
                "idPersona" UUID PRIMARY KEY,
                nombre VARCHAR(100),
                cedula BIGINT UNIQUE,
                correo VARCHAR(100),
                telefono BIGINT,
                direccion VARCHAR(200),
                estado VARCHAR(20)
            )
        """))
        conn.execute(text('TRUNCATE TABLE public.personas CASCADE'))
        
        # Insertar 10 aprendices
        for i in range(1, 11):
            conn.execute(
                text("""
                    INSERT INTO public.personas ("idPersona", nombre, cedula, correo, telefono, estado)
                    VALUES (:id, :nombre, :cedula, :correo, :telefono, 'ACTIVO')
                """),
                {
                    "id": str(uuid.uuid4()),
                    "nombre": f"Aprendiz Prueba {i}",
                    "cedula": 1000000000 + i,
                    "correo": f"aprendiz{i}@sena.edu.co",
                    "telefono": 3000000000 + i
                }
            )
    print("Base de datos SENA poblada correctamente.")

if __name__ == "__main__":
    reset_sena_db()
    reset_local_db()
    print("¡TODO LISTO!")
