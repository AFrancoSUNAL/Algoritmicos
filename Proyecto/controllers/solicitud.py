from config.conexion import get_connection

def get_solicitudes_pendientes():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT s.id_solicitud, s.titulo, s.descripcion, s.facultad, s.inicio, s.fin, s.creado_en,
               u.nombre AS solicitante,
               ub.nombre AS ubicacion
        FROM Solicitud s
        JOIN Usuario u ON s.creado_por = u.id_usuario
        JOIN Ubicacion ub ON s.fk_ubicacion = ub.id_ubicacion
        WHERE s.fk_estado = 1
        ORDER BY s.creado_en ASC
    """
    cursor.execute(query)
    solicitudes = cursor.fetchall()
    cursor.close()
    connection.close()
    return solicitudes
