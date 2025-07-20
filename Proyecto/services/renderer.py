from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parents[1]
window = None  # Será asignado por main.py

def esperar_archivo_ruta(ruta, max_segundos=5):
    inicio = time.time()
    while time.time() - inicio < max_segundos:
        if ruta.exists() and ruta.stat().st_size > 50:
            return True
        time.sleep(0.05)
    return False

def compilar(nombre_plantilla, context={}):
    env = Environment(loader=FileSystemLoader(BASE_DIR / 'web/templates'))
    plantilla = env.get_template(nombre_plantilla + '.html')
    html = plantilla.render(context)

    compilado_path = BASE_DIR / 'web' / '_compilado.html'
    with open(compilado_path, 'w', encoding='utf-8') as f:
        f.write(html)

    esperar_archivo_ruta(compilado_path)

    # Solo recargar si ya se asignó window
    if window is not None:
        window.load_url(compilado_path.as_uri())

def cargar_recurso(tipo, nombre):
    recurso_path = BASE_DIR / 'web' / 'static' / tipo / nombre
    if recurso_path.exists():
        return recurso_path.as_uri()
    else:
        raise FileNotFoundError(f"No se encontró el recurso {nombre} en {tipo}")

recursos_comun = {
    'logo': cargar_recurso('img', 'escudoUnal.svg'),
    'logo_background': cargar_recurso('img', 'sealBck.png'),
    'logo_buho': cargar_recurso('img', 'logo_buho.svg')
}

info_usuario = {
    'id': '',
    'nombre': '',
    'email': '',
    'rol': 'admin'  # puede ser 'usuario', 'admin' o 'invitado'
}
