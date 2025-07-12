import mysql.connector
import sys


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
        sql_script = open('db/esquema.sql', 'r').read()
        for instruccion in sql_script.split(';'):
            instruccion = instruccion.strip()
            if instruccion:
                cursor.execute(instruccion)
        conexion.commit()
        print("Base de datos un_mapa_db creada exitosamente.")
        cursor.close()
        conexion.close()
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_DB_CREATE_EXISTS:
            print("La base de datos un_mapa_db ya existe.")
        else:
            print(f"Error al crear la base de datos: {err}")
            
    
create_database()