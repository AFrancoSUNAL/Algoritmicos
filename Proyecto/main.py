import webview
from jinja2 import Environment, FileSystemLoader

class API:
    def cargar_login(self):
        compilar('login', {})
        window.load_url('web/_compilado.html')
    def cargar_home(self):
        compilar('home', {'nombre': 'Andres'})
        window.load_url('web/_compilado.html')

def compilar(plantilla, context={}):
    env = Environment(loader=FileSystemLoader('web/templates'))
    plantilla = env.get_template(plantilla + '.html')
    html = plantilla.render(context)

    with open('web/_compilado.html', 'w') as f:
        f.write(html)
        
compilar('home', {'nombre': 'Andres'})

api = API()
window = webview.create_window('UN-Mapa', "web/_compilado.html", js_api=api)
webview.start()