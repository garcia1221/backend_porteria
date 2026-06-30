# 🛡️ Backend - Control de Equipos SENA

Este es el servidor central (Backend) del sistema de control de ingresos y salidas de equipos del SENA. Está construido con **Python** y **FastAPI**, y se encarga de manejar toda la lógica de negocio, la conexión con la base de datos y proveer las APIs para la aplicación móvil y la plataforma web.

## 🚀 Tecnologías Principales

- **[FastAPI](https://fastapi.tiangolo.com/):** Framework web moderno y rápido para construir APIs con Python 3.
- **[SQLAlchemy](https://www.sqlalchemy.org/):** ORM (Object Relational Mapper) para la manipulación y gestión de la base de datos.
- **[SQLite](https://www.sqlite.org/):** Base de datos ligera e integrada por defecto (escalable a PostgreSQL o MySQL si se requiere).
- **[Uvicorn](https://www.uvicorn.org/):** Servidor ASGI ultrarrápido para ejecutar la aplicación.

## 📁 Estructura del Proyecto

El proyecto sigue una arquitectura por capas para mantener el código limpio y escalable:

```text
backend/
├── app/
│   ├── database/       # Configuración y conexión a la base de datos (database.py)
│   ├── models/         # Modelos de SQLAlchemy (Tablas de la BD)
│   ├── repositories/   # Lógica de acceso a datos (Consultas a la BD)
│   ├── routes/         # Endpoints de la API (Controladores)
│   ├── services/       # Lógica de negocio (Reglas de la aplicación)
│   └── main.py         # Punto de entrada de la aplicación FastAPI
├── venv/               # Entorno virtual de Python
├── .env                # Variables de entorno (Credenciales, claves, etc.)
└── README.md           # Este archivo
```

## ⚙️ Configuración e Instalación

Sigue estos pasos para correr el proyecto de manera local en tu máquina:

### 1. Requisitos Previos
- Python 3.10 o superior instalado.
- Git (Opcional, para clonar el repositorio).

### 2. Crear y Activar el Entorno Virtual
Abre una terminal en la carpeta `backend` y ejecuta:

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
Una vez activado el entorno virtual (`(venv)` debe aparecer en tu terminal), instala las librerías necesarias:
```bash
pip install fastapi uvicorn sqlalchemy
```

### 4. Ejecutar el Servidor
Para encender el servidor en modo desarrollo (se reiniciará automáticamente si haces cambios en el código):

```bash
uvicorn app.main:app --reload --port 8000
```

> **Nota:** El servidor estará corriendo en `http://127.0.0.1:8000` o `http://localhost:8000`.

## 📚 Documentación Interactiva de la API

Una de las grandes ventajas de FastAPI es que genera documentación automática. Una vez que el servidor esté corriendo, puedes visitar cualquiera de los siguientes enlaces en tu navegador para probar y explorar los endpoints:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🛠️ Comandos Útiles para el Desarrollo

- **Desactivar el entorno virtual:**
  ```bash
  deactivate
  ```
- **Conocer tu IP Local (Windows)** *(Útil si estás conectando la App Móvil)*:
  ```bash
  ipconfig
  ```
  *Busca la línea que dice `Dirección IPv4` y úsala en tu frontend.*
