import webview
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from controllers.ubicacion import get_todas_ubicaciones
from services.map_service import generar_mapa
import time

BASE_DIR = Path(__file__).resolve().parent
ubicaciones = get_todas_ubicaciones()

def esperar_archivo_ruta(ruta, max_segundos=5):
    """Espera hasta que el archivo exista y tenga contenido (>0 bytes)."""
    inicio = time.time()
    while time.time() - inicio < max_segundos:
        if ruta.exists() and ruta.stat().st_size > 50:  # tamaño mínimo arbitrario
            return True
        time.sleep(0.05)  # espera 50 ms antes de volver a intentar
    return False

def compilar(nombre_plantilla, context={}):
    env = Environment(loader=FileSystemLoader(BASE_DIR / 'web/templates'))
    plantilla = env.get_template(nombre_plantilla + '.html')
    html = plantilla.render(context)

    compilado_path = BASE_DIR / 'web' / '_compilado.html'
    with open(compilado_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    if not esperar_archivo_ruta(compilado_path):
        print("Error: El archivo compilado no se generó correctamente o está vacío.")

    if 'window' in globals():
        window.load_url(compilado_path.as_uri())
        
def cargar_recursos(tipo, nombre):
    recursos_dir = BASE_DIR / 'web' / 'static' / tipo
    recurso_path = recursos_dir / nombre

    if recurso_path.exists():
        return recurso_path.as_uri()
    else:
        raise FileNotFoundError(f"Recurso {nombre} no encontrado en {recursos_dir}")

class API:
    def cargar_home(self):
        compilar('home', {'nombre': 'Andres', 'ubicaciones': ubicaciones, **recursos_comun, **info_usuario})

    def cargar_login(self):
        compilar('login', {**recursos_comun, **info_usuario})
    
    def cargar_ubicacion(self, id_ubicacion):
        from controllers.ubicacion import get_ubicacion
        ubicacion = get_ubicacion(id_ubicacion)
        compilar('ubicacion', {'ubicacion': ubicacion, **recursos_comun, **info_usuario})
    
    def cargar_seleccion_ruta(self):
        from controllers.ubicacion import get_todas_ubicaciones
        ubicaciones = get_todas_ubicaciones()
        compilar('seleccion_ruta', {'ubicaciones': ubicaciones, **recursos_comun, **info_usuario})
        
    def crear_solicitud(self, titulo, descripcion, facultad, inicio, fin, id_ubicacion, id_usuario):
        from config.conexion import get_connection
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO Solicitud (titulo, descripcion, facultad, inicio, fin, fk_ubicacion, creado_por)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (titulo, descripcion, facultad, inicio, fin, id_ubicacion, id_usuario))

        connection.commit()
        cursor.close()
        connection.close()
        return {'status': 'ok'}

    def cargar_solicitudes(self):
        from controllers.solicitud import get_solicitudes_pendientes
        from controllers.ubicacion import get_todas_ubicaciones
        solicitudes = get_solicitudes_pendientes()
        ubicaciones = get_todas_ubicaciones()
        compilar('solicitudes', {'solicitudes': solicitudes, 'ubicaciones': ubicaciones, **recursos_comun, **info_usuario})
    
    def responder_solicitud(self, id_solicitud, aceptada, respuesta, id_admin):
        from config.conexion import get_connection
        connection = get_connection()
        cursor = connection.cursor()

        estado = 2 if aceptada else 3  # 2: aceptada, 3: rechazada
        
        cursor.execute("""
            SELECT fk_estado FROM solicitud WHERE id_solicitud = %s               
        """, (id_solicitud,))
        s = cursor.fetchone()
        
        if s[0] == 1:
            cursor.execute("""
                UPDATE Solicitud
                SET fk_estado = %s, respuesta = %s, gestionado_por = %s
                WHERE id_solicitud = %s
            """, (estado, respuesta, id_admin, id_solicitud))

            if aceptada:
                cursor.execute("""
                    SELECT titulo, descripcion, inicio, fin, fk_ubicacion FROM Solicitud WHERE id_solicitud = %s
                """, (id_solicitud,))
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
        from controllers.evento import get_eventos
        from controllers.ubicacion import get_todas_ubicaciones
        eventos = get_eventos()
        ubicaciones = get_todas_ubicaciones()
        compilar('eventos', {'eventos': eventos, 'ubicaciones': ubicaciones, **recursos_comun, **info_usuario})
    
    def crear_evento(self, titulo, descripcion, inicio, fin, id_ubicacion):
        from config.conexion import get_connection
        connection = get_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO Evento (titulo, descripcion, inicio, fin, fk_ubicacion)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (titulo, descripcion, inicio, fin, id_ubicacion))
        connection.commit()
        cursor.close()
        connection.close()
        return {'status': 'ok'}

    def abrir_ruta(self, id_origen, id_destino):
        from controllers.ubicacion import get_ubicacion
        import webbrowser

        origen = get_ubicacion(id_origen)
        destino = get_ubicacion(id_destino)

        if origen and destino:
            coord_origen = origen[4]
            coord_destino = destino[4]
            url = f"https://www.google.com/maps/dir/?api=1&origin={coord_origen}&destination={coord_destino}&travelmode=walking"
            webbrowser.open(url)
            return {'status': 'ok'}
        else:
            return {'status': 'error', 'msg': 'Ubicación no encontrada'}

    def cargar_mapa(self):
        from services.map_service import generar_mapa
        ruta_html = generar_mapa()
        with open(ruta_html, encoding='utf-8') as f:
            html_map = f.read()
        compilar('mapa', {'mapa_html': html_map, **recursos_comun, **info_usuario})
        
# Forma temporal de cargar la información del usuario
info_usuario = {
    'nombre': 'Usuario 1',
    'email': 'usuario1@unal.edu.co',
    'rol': 'admin',  # puede ser 'usuario', 'admin' o 'invitado'
}

recursos_comun = {
    'logo': cargar_recursos('img', 'escudoUnal.svg'),
    'logo_background': cargar_recursos('img', 'sealBck.png'),
    'logo_buho': cargar_recursos('img', 'logo_buho.svg')
}

compilar('home', {'ubicaciones': ubicaciones, **recursos_comun, **info_usuario})

window = webview.create_window('UN-Mapa', (BASE_DIR / "web/_compilado.html").as_uri(), js_api=API())
webview.start()