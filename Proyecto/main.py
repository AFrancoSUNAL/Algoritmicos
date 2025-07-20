from pathlib import Path
import webview
from services.api import API
import services.renderer as renderer
from controllers.ubicacion import get_todas_ubicaciones

BASE_DIR = Path(__file__).resolve().parent
ubicaciones = get_todas_ubicaciones()

# Compilar la plantilla home con las ubicaciones y recursos comunes
renderer.compilar('home', {
    'ubicaciones': ubicaciones,
    **renderer.recursos_comun,
    **renderer.info_usuario
})

window = webview.create_window('UN-Mapa', (BASE_DIR / "web/_compilado.html").as_uri(), js_api=API())
renderer.window = window  
webview.start()