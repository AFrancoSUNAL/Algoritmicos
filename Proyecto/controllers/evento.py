from config.conexion import get_connection

def get_eventos():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT e.id_evento, e.titulo, e.descripcion, e.inicio, e.fin,
            u.nombre AS nombre_ubicacion
        FROM evento e 
        JOIN ubicacion u ON e.fk_ubicacion = u.id_ubicacion
        WHERE e.fin >= date(now())
        ORDER BY e.inicio DESC;
    """
    cursor.execute(query)
    eventos = cursor.fetchall()
    cursor.close()
    connection.close()
    return eventos
