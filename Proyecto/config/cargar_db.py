import mysql.connector
import sys
import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def create_database():
    try:
        user = sys.argv[1] if len(sys.argv) > 1 else None
        password = sys.argv[2] if len(sys.argv) > 2 else None
        port = sys.argv[3] if len(sys.argv) > 3 else None

        if not user or not password or not port:
            print("Por favor, proporciona el usuario, la contraseña y el puerto de la base de datos.")
            return

        conexion = mysql.connector.connect(
            host='localhost',
            port=port,
            user=user,
            password=password,
        )

        cursor = conexion.cursor()
        cursor.execute("CREATE DATABASE un_mapa_db")
        cursor.execute("USE un_mapa_db")

        # Ejecutar esquema.sql
        ruta_esquema = os.path.join(os.path.dirname(__file__), 'esquema.sql')
        with open(ruta_esquema, 'r', encoding='utf-8') as archivo:
            sql_script = archivo.read()

        for instruccion in sql_script.split(';'):
            instruccion = instruccion.strip()
            if instruccion:
                cursor.execute(instruccion)

        # Ejecutar datos.sql
        ruta_datos = os.path.join(os.path.dirname(__file__), 'datos.sql')
        with open(ruta_datos, 'r', encoding='utf-8') as archivo:
            datos_script = archivo.read()

        for instruccion in datos_script.split(';'):
            instruccion = instruccion.strip()
            if instruccion and not instruccion.upper().startswith("USE"):
                cursor.execute(instruccion)

        conexion.commit()
        print("Base de datos un_mapa_db creada y poblada exitosamente.")
        cursor.close()
        conexion.close()

        with open(BASE_DIR / 'config/db_info.json', 'w') as db_info_file:
            db_info = {
                "host": "localhost",
                "user": user,
                "port": port,
                "password": password,
                "database": "un_mapa_db"
            }
            db_info_file.write(json.dumps(db_info, indent=4))

    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_DB_CREATE_EXISTS:
            print("La base de datos un_mapa_db ya existe.")
        else:
            print(f"Error al crear o poblar la base de datos: {err}")

create_database()
