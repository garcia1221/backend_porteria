import os
from sqlalchemy import text
from app.database.database import engine

with engine.connect() as con:
    con.execute(text('ALTER TABLE usuarios_externos DROP COLUMN IF EXISTS correo;'))
    con.execute(text('ALTER TABLE usuarios_externos DROP COLUMN IF EXISTS telefono;'))
    con.execute(text("UPDATE usuarios_externos SET empresa='Particular' WHERE empresa IS NULL OR empresa='' OR empresa='<null>';"))
    con.commit()

print('Database updated!')
