import webview
from jinja2 import Environment, FileSystemLoader

class API:
    def cargar_home(self):
        from controllers.ubicacion import get_todas_ubicaciones
        ubicaciones = get_todas_ubicaciones()
        compilar('home', {'nombre': 'Andres', 'ubicaciones': ubicaciones})
        window.load_url('web/_compilado.html')
    def cargar_login(self):
        compilar('login', {})
        window.load_url('web/_compilado.html')
    def cargar_ubicacion(self, id_ubicacion):
        from controllers.ubicacion import get_ubicacion
        ubicacion = get_ubicacion(id_ubicacion)
        compilar('ubicacion', {'ubicacion': ubicacion})
        window.load_url('web/_compilado.html')
    def cargar_seleccion_ruta(self):
        from controllers.ubicacion import get_todas_ubicaciones
        ubicaciones = get_todas_ubicaciones()
        compilar('seleccion_ruta', {'ubicaciones': ubicaciones})
        window.load_url('web/_compilado.html')
    def abrir_ruta(self, id_origen, id_destino):
        from controllers.ubicacion import get_ubicacion
        import webbrowser

        origen = get_ubicacion(id_origen)
        destino = get_ubicacion(id_destino)

        if origen and destino:
            coord_origen = origen[3] 
            coord_destino = destino[3]

            url = f"https://www.google.com/maps/dir/?api=1&origin={coord_origen}&destination={coord_destino}&travelmode=walking"
            webbrowser.open(url)
            return {'status': 'ok'}
        else:
            return {'status': 'error', 'msg': 'Ubicación no encontrada'}

def compilar(plantilla, context={}):
    env = Environment(loader=FileSystemLoader('Proyecto/web/templates'))
    plantilla = env.get_template(plantilla + '.html')
    html = plantilla.render(context)

    with open('Proyecto/web/_compilado.html', 'w', encoding='utf-8') as f:
        f.write(html)
        

api = API()
window = webview.create_window('UN-Mapa', "web/_compilado.html", js_api=api)
webview.start()