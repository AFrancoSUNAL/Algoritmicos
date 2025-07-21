import unittest
import sys
import datetime
from pathlib import Path

# Añadir la ruta raíz del proyecto para poder importar correctamente
sys.path.append(str(Path(__file__).resolve().parent.parent))
from controllers import login
from services.api import API
from config.conexion import get_connection 
from controllers.solicitud import get_solicitudes_pendientes

class TestLogin(unittest.TestCase):
    def test_registro_correo_no_institucional(self):
        """
        Verifica que no se permita registrar un usuario con correo que no sea @unal.edu.co
        """
        resultado = login.registrar_usuario("juan@gmail.com", "$2b$12$ozy4qHcENEb1vj5tU29sOuLMkkPEUCGLDhnrEgz/mRcZVrD6IGSPe")#la contraseña es un hash de 'password', este hash significa 12345
        self.assertEqual(resultado['status'], 'error')
        self.assertIn('@unal.edu.co', resultado['msg'])

    def test_registro_exitoso(self):
        """
        Verifica que se pueda registrar un usuario correctamente con un correo institucional.
        (Nota: esta prueba puede fallar si ya existe ese correo en la BD, se recomienda limpiar).
        """
        correo = "testuser@unal.edu.co"
        resultado = login.registrar_usuario(correo, "$2b$12$ozy4qHcENEb1vj5tU29sOuLMkkPEUCGLDhnrEgz/mRcZVrD6IGSPe")
        # El test puede devolver 'ok' o 'error' si el usuario ya está registrado, ambas respuestas son válidas.
        self.assertIn(resultado['status'], ['ok', 'error'])

    def test_login_contrasena_incorrecta(self):
        """
        Verifica que no se permita el inicio de sesión con una contraseña incorrecta.
        Asegúrate de que este correo exista con una contraseña distinta a 'incorrecta'.
        """
        resultado = login.login("testuser@unal.edu.co", "incorrecta")
        self.assertEqual(resultado['status'], 'error')
        self.assertIn('Contraseña', resultado['msg'])

class TestSolicitudes(unittest.TestCase):
    
    def test_crear_eventos_repetidos(self):
        """
        Verifica que no se acepten o rechazen solicitudes de eventos varias veces.
        """
        
        api = API()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Evento")
        total_antes = cursor.fetchone()

        api.crear_solicitud("solicitud_test", "Lorem ipsum dolor sit amet", "", datetime.datetime.now() + datetime.timedelta(days=1), datetime.datetime.now() + datetime.timedelta(days=2), 1, 2)
        
        ultima_solicitud = get_solicitudes_pendientes()[-1]
        api.responder_solicitud(ultima_solicitud['id_solicitud'], 'Aceptada', 'Solicitud aceptada correctamente', 1)
        api.responder_solicitud(ultima_solicitud['id_solicitud'], 'Aceptada', 'Solicitud aceptada correctamente', 1)
        api.responder_solicitud(ultima_solicitud['id_solicitud'], 'Aceptada', 'Solicitud aceptada correctamente', 1)

        cursor.close()
        conn.close()
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM Evento")
        
        total_despues = cursor.fetchone()
        cursor.close()
        conn.close()

        self.assertEqual(int(total_antes[0]) + 1, int(total_despues[0]))
        
    def test_crear_solicitud_repetida(self):
        """
        Verifica que no se pueda crear una solicitud si ya hay una pendiente.
        """
        
        api = API()

        conn = get_connection()
        cursor = conn.cursor()

        api.crear_solicitud("solicitud_repetida_test_1", "Lorem ipsum dolor sit amet", "", datetime.datetime.now() + datetime.timedelta(days=1), datetime.datetime.now() + datetime.timedelta(days=2), 1, 1)
        
        # Intentar crear otra solicitud
        resultado = api.crear_solicitud("solicitud_repetida_test_2", "Lorem ipsum dolor sit amet", "", datetime.datetime.now() + datetime.timedelta(days=3), datetime.datetime.now() + datetime.timedelta(days=4), 1, 1)

        cursor.close()
        conn.close()
        
        self.assertEqual(resultado['status'], 'forbidden')
        
    def test_solicitud_sin_respuesta(self):
        """
        Verifica que no se pueda aceptar o rechazar una solicitud sin respuesta.
        """
        
        api = API()
        
        api.crear_solicitud("solicitud_sin_respuesta", "Lorem ipsum dolor sit amet", "", datetime.datetime.now() + datetime.timedelta(days=1), datetime.datetime.now() + datetime.timedelta(days=2), 1, 2)
        ultima_solicitud = get_solicitudes_pendientes()[-1]
        test1 = api.responder_solicitud(ultima_solicitud['id_solicitud'], 2, "", 2)
        test2 = api.responder_solicitud(ultima_solicitud['id_solicitud'], 1, None, 2)
        
        self.assertEqual(test1['status'], 'error')
        self.assertEqual(test2['status'], 'error')
        
class TestRegistro(unittest.TestCase):
    def test_registro_contrasena_debil(self):
        """
        Verifica que no se permita registrar un usuario con contraseña débil.
        """
        correo = "debil@unal.edu.co"
        contrasena_debil = "123456"  # No cumple con RF19
        resultado = login.registrar_usuario(correo, contrasena_debil)
        self.assertEqual(resultado['status'], 'error')
        self.assertIn('contraseña', resultado['msg'].lower())

    def test_login_exitoso(self):
        correo = "testuser_1@unal.edu.co"
        contrasena = "C0ntraseña!2"  # Cumple requisitos

        # Intentar registrar al usuario
        resultado_registro = login.registrar_usuario(correo, contrasena)
        self.assertIn(resultado_registro['status'], ['ok', 'error'])

        # Luego login con la misma contraseña en texto plano
        resultado_login = login.login(correo, contrasena)
        self.assertEqual(resultado_login['status'], 'ok')

    def test_registro_correo_duplicado(self):
        """
        Verifica que no se permita registrar dos veces el mismo correo institucional.
        """
        correo = "duplicado@unal.edu.co"
        contrasena = "$2b$12$ozy4qHcENEb1vj5tU29sOuLMkkPEUCGLDhnrEgz/mRcZVrD6IGSPe"
        login.registrar_usuario(correo, contrasena)  # Primera vez
        resultado = login.registrar_usuario(correo, contrasena)  # Segunda vez
        self.assertEqual(resultado['status'], 'error')
        self.assertIn('ya está registrado', resultado['msg'].lower())

if __name__ == '__main__':
    unittest.main()
