import webview
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from controllers.ubicacion import get_todas_ubicaciones
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
        recursos = {
            'logo': cargar_recursos('img', 'escudoUnal.svg'),
            'logo_background': cargar_recursos('img', 'sealBck.png'),
            'logo_buho': cargar_recursos('img', 'logo_buho.svg')
        }
        compilar('home', {'nombre': 'Andres', 'ubicaciones': ubicaciones, **recursos, **info_usuario})

    def cargar_login(self):
        recursos = {
            'logo': cargar_recursos('img', 'escudoUnal.svg'),
            'logo_background': cargar_recursos('img', 'sealBck.png'),
            'logo_buho': cargar_recursos('img', 'logo_buho.svg')
        }
        compilar('login', {**recursos, **info_usuario})
    
    def cargar_ubicacion(self, id_ubicacion):
        from controllers.ubicacion import get_ubicacion
        ubicacion = get_ubicacion(id_ubicacion)
        print(ubicacion)
        recursos = {
            'logo': cargar_recursos('img', 'escudoUnal.svg'),
            'logo_background': cargar_recursos('img', 'sealBck.png'),
            'logo_buho': cargar_recursos('img', 'logo_buho.svg')
        }
        compilar('ubicacion', {'ubicacion': ubicacion, **recursos, **info_usuario})
    
    def cargar_seleccion_ruta(self):
        from controllers.ubicacion import get_todas_ubicaciones
        ubicaciones = get_todas_ubicaciones()
        recursos = {
            'logo': cargar_recursos('img', 'escudoUnal.svg'),
            'logo_background': cargar_recursos('img', 'sealBck.png'),
            'logo_buho': cargar_recursos('img', 'logo_buho.svg')
        }
        compilar('seleccion_ruta', {'ubicaciones': ubicaciones, **recursos, **info_usuario})
        
    def cargar_solicitudes(self):
        recursos = {
            'logo': cargar_recursos('img', 'escudoUnal.svg'),
            'logo_background': cargar_recursos('img', 'sealBck.png'),
            'logo_buho': cargar_recursos('img', 'logo_buho.svg')
        }
        compilar('solicitudes', {**recursos, **info_usuario})
    
    def cargar_eventos(self):
        recursos = {
            'logo': cargar_recursos('img', 'escudoUnal.svg'),
            'logo_background': cargar_recursos('img', 'sealBck.png'),
            'logo_buho': cargar_recursos('img', 'logo_buho.svg')
        }
        compilar('eventos', {**recursos, **info_usuario})
    
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

# Forma temporal de cargar la información del usuario
info_usuario = {
    'nombre': 'Usuario 1',
    'email': 'usuario1@unal.edu.co',
    'rol': 'usuario'
}

recursos = {
    'logo': cargar_recursos('img', 'escudoUnal.svg'),
    'logo_background': cargar_recursos('img', 'sealBck.png'),
    'logo_buho': cargar_recursos('img', 'logo_buho.svg')
}
compilar('home', {'ubicaciones': ubicaciones, **recursos, **info_usuario})

window = webview.create_window('UN-Mapa', (BASE_DIR / "web/_compilado.html").as_uri(), js_api=API())
webview.start()