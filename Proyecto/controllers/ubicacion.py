from config.conexion import get_connection

def get_ubicacion(id_ubicacion):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ubicacion WHERE id_ubicacion = %s", (id_ubicacion,))
    ubicacion = cursor.fetchone()
    cursor.close()
    connection.close()
    return ubicacion