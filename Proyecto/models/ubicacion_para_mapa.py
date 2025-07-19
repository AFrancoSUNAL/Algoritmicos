from config.conexion import get_connection

def obtener_ubicaciones():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.id_ubicacion, u.nombre, u.coordenadas
        FROM Ubicacion u
    """)
    ubicaciones = cursor.fetchall()
    cursor.close()
    connection.close()
    return ubicaciones

def obtener_eventos_activos(id_ubicacion):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_evento, titulo, descripcion, inicio, fin
        FROM Evento
        WHERE fk_ubicacion = %s
          AND NOW() BETWEEN inicio AND fin
    """, (id_ubicacion,))

    eventos = cursor.fetchall()
    cursor.close()
    connection.close()
    return eventos
