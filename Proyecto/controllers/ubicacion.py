from config.conexion import get_connection

def get_ubicacion(id_ubicacion):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ubicacion WHERE id_ubicacion = %s", (id_ubicacion,))
    ubicacion = cursor.fetchone()
    cursor.close()
    connection.close()
    return ubicacion

def get_todas_ubicaciones():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id_ubicacion, nombre FROM ubicacion ORDER BY nombre")
    ubicaciones = cursor.fetchall()
    cursor.close()
    connection.close()
    return ubicaciones
