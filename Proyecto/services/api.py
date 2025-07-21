import webbrowser
from controllers.ubicacion import get_ubicacion, get_todas_ubicaciones
from controllers.evento import get_eventos
from controllers.solicitud import get_solicitudes_pendientes
from controllers.login import login, registrar_usuario
from services.map_service import generar_mapa
from config.conexion import get_connection
from services.renderer import compilar, recursos_comun, info_usuario

class API:
    def cargar_home(self):
        compilar('home', {'nombre': 'Andres', 'ubicaciones': get_todas_ubicaciones(), **recursos_comun, **info_usuario})

    def cargar_login(self):
        compilar('login', {**recursos_comun, **info_usuario})

    def cargar_ubicacion(self, id_ubicacion):
        ubicacion = get_ubicacion(id_ubicacion)
        compilar('ubicacion', {'ubicacion': ubicacion, **recursos_comun, **info_usuario})

    def cargar_seleccion_ruta(self):
        ubicaciones = get_todas_ubicaciones()
        compilar('seleccion_ruta', {'ubicaciones': ubicaciones, **recursos_comun, **info_usuario})

    def crear_solicitud(self, titulo, descripcion, facultad, inicio, fin, id_ubicacion, id_usuario):
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM solicitud WHERE fk_estado=1 AND creado_por = %s", (id_usuario,))
        if cursor.fetchone()[0] > 0:
            cursor.close()
            connection.close()
            return {'status': 'forbidden', 'msg': 'Ya tienes una solicitud pendiente.'}
        
        cursor.execute("""
            INSERT INTO Solicitud (titulo, descripcion, facultad, inicio, fin, fk_ubicacion, creado_por)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (titulo, descripcion, facultad, inicio, fin, id_ubicacion, id_usuario))
        connection.commit()
        cursor.close()
        connection.close()
        return {'status': 'ok'}

    def cargar_solicitudes(self):
        solicitudes = get_solicitudes_pendientes()
        ubicaciones = get_todas_ubicaciones()
        compilar('solicitudes', {'solicitudes': solicitudes, 'ubicaciones': ubicaciones, **recursos_comun, **info_usuario})

    def responder_solicitud(self, id_solicitud, aceptada, respuesta, id_admin):
        if respuesta is None or respuesta.strip() == "":
            return {'status': 'error', 'msg': 'La respuesta no puede estar vacía.'}
        
        connection = get_connection()
        cursor = connection.cursor()
        estado = 2 if aceptada else 3

        cursor.execute("SELECT fk_estado FROM solicitud WHERE id_solicitud = %s", (id_solicitud,))
        s = cursor.fetchone()

        if s and s[0] == 1:
            cursor.execute("""
                UPDATE Solicitud
                SET fk_estado = %s, respuesta = %s, gestionado_por = %s
                WHERE id_solicitud = %s
            """, (estado, respuesta, id_admin, id_solicitud))

            if aceptada:
                cursor.execute("SELECT titulo, descripcion, inicio, fin, fk_ubicacion FROM Solicitud WHERE id_solicitud = %s", (id_solicitud,))
                s = cursor.fetchone()
                cursor.execute("""
                    INSERT INTO Evento (titulo, descripcion, inicio, fin, fk_ubicacion, fk_solicitud_asociada)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (s[0], s[1], s[2], s[3], s[4], id_solicitud))

            connection.commit()
        cursor.close()
        connection.close()
        return {'status': 'ok'}

    def cargar_eventos(self):
        eventos = get_eventos()
        ubicaciones = get_todas_ubicaciones()
        compilar('eventos', {'eventos': eventos, 'ubicaciones': ubicaciones, **recursos_comun, **info_usuario})

    def crear_evento(self, titulo, descripcion, inicio, fin, id_ubicacion):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Evento (titulo, descripcion, inicio, fin, fk_ubicacion)
            VALUES (%s, %s, %s, %s, %s)
        """, (titulo, descripcion, inicio, fin, id_ubicacion))
        connection.commit()
        cursor.close()
        connection.close()
        return {'status': 'ok'}

    def cargar_registro(self):
        compilar('registro', {**recursos_comun, **info_usuario})

    def abrir_ruta(self, id_origen, id_destino):
        origen = get_ubicacion(id_origen)
        destino = get_ubicacion(id_destino)
        if origen and destino:
            url = f"https://www.google.com/maps/dir/?api=1&origin={origen[4]}&destination={destino[4]}&travelmode=walking"
            webbrowser.open(url)
            return {'status': 'ok'}
        return {'status': 'error', 'msg': 'Ubicación no encontrada'}

    def cargar_mapa(self):
        ruta_mapa = generar_mapa()
        compilar('mapa', {'ruta_mapa': ruta_mapa, **recursos_comun, **info_usuario})

    def login_usuario(self, correo, password):
        resultado = login(correo, password)
        if resultado['status'] == 'ok':
            info_usuario.update(resultado['usuario'])
        return resultado

    def registrar_usuario(self, correo, password):
        return registrar_usuario(correo, password)

    def cerrar_sesion(self):
        info_usuario.update({'id': '', 'nombre': '', 'email': '', 'rol': 'invitado'})
        self.cargar_home()
