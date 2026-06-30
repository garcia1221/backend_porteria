from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Conexión a la BD SENA (ERP separado)
SENA_DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"erp_sena"
)

sena_engine = create_engine(SENA_DATABASE_URL)
SenaSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sena_engine)


def get_sena_db():
    db = SenaSessionLocal()
    try:
        yield db
    finally:
        db.close()


def buscar_persona_por_cedula(cedula: str):
    """
    Busca una persona directamente en la BD erp_sena por número de cédula.
    Retorna un dict con los datos o None si no la encuentra.
    """
    try:
        with sena_engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT "idPersona", nombre, cedula, correo, telefono, direccion
                    FROM public.personas
                    WHERE cedula = :cedula
                    LIMIT 1
                """),
                {"cedula": cedula}
            )
            row = result.fetchone()
            if row:
                return {
                    "fk_persona": str(row[0]),
                    "nombre": row[1],
                    "documento": str(row[2]),
                    "correo": row[3] or "",
                    "telefono": str(row[4] or ""),
                    "rol": "aprendiz",
                    "programa": "SENA"
                }
    except Exception as e:
        print(f"Error buscando en erp_sena: {e}")
    return None


def buscar_persona_por_uuid(uuid: str):
    """
    Busca una persona en erp_sena por su UUID (idPersona).
    Retorna dict con nombre, cedula, correo o None.
    """
    try:
        with sena_engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT "idPersona", nombre, cedula, correo, telefono
                    FROM public.personas
                    WHERE "idPersona"::text = :uuid
                    LIMIT 1
                """),
                {"uuid": uuid}
            )
            row = result.fetchone()
            if row:
                return {
                    "fk_persona": str(row[0]),
                    "nombre": row[1],
                    "documento": str(row[2]),
                    "correo": row[3] or "",
                    "telefono": str(row[4] or ""),
                    "rol": "aprendiz",
                }
    except Exception as e:
        print(f"Error buscando por UUID en erp_sena: {e}")
    return None


def buscar_personas_por_filtro(filtro: str):
    """
    Busca personas en erp_sena por cédula (exacta/parcial) o nombre (parcial).
    Retorna una lista de dicts con fk_persona, nombre, documento, etc.
    """
    try:
        with sena_engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT "idPersona", nombre, cedula, correo, telefono
                    FROM public.personas
                    WHERE cedula::text ILIKE :filtro
                       OR nombre ILIKE :filtro
                    LIMIT 50
                """),
                {"filtro": f"%{filtro}%"}
            )
            rows = result.fetchall()
            return [
                {
                    "fk_persona": str(row[0]),
                    "nombre": row[1],
                    "documento": str(row[2]),
                    "correo": row[3] or "",
                    "telefono": str(row[4] or ""),
                    "rol": "aprendiz"
                }
                for row in rows
            ]
    except Exception as e:
        print(f"Error filtrando personas en erp_sena: {e}")
    return []

def listar_aprendices():
    """
    Lista todos los aprendices (personas) de erp_sena.
    """
    try:
        with sena_engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT "idPersona", nombre, cedula, correo, telefono
                    FROM public.personas
                    ORDER BY nombre ASC
                    LIMIT 100
                """)
            )
            rows = result.fetchall()
            return [
                {
                    "fk_persona": str(row[0]),
                    "nombre": row[1],
                    "documento": str(row[2]),
                    "correo": row[3] or "",
                    "telefono": str(row[4] or ""),
                    "rol": "aprendiz"
                }
                for row in rows
            ]
    except Exception as e:
        print(f"Error listando aprendices en erp_sena: {e}")
    return []

def crear_aprendiz(nombre: str, cedula: str, correo: str, telefono: str):
    """
    Crea un nuevo aprendiz en erp_sena.
    Retorna el dict con los datos y fk_persona (UUID generado).
    """
    import uuid
    nuevo_uuid = str(uuid.uuid4())
    try:
        with sena_engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO public.personas ("idPersona", nombre, cedula, correo, telefono, estado)
                    VALUES (:id, :n, :c, :co, :t, 'ACTIVO')
                """),
                {
                    "id": nuevo_uuid,
                    "n": nombre,
                    "c": int(cedula),
                    "co": correo,
                    "t": int(telefono) if telefono else None
                }
            )
        return {
            "fk_persona": nuevo_uuid,
            "nombre": nombre,
            "documento": cedula,
            "correo": correo,
            "telefono": telefono,
            "rol": "aprendiz"
        }
    except Exception as e:
        print(f"Error creando aprendiz en erp_sena: {e}")
        return None
