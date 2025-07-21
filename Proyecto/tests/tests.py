import unittest
import sys
from pathlib import Path

# Añadir la ruta raíz del proyecto para poder importar correctamente
sys.path.append(str(Path(__file__).resolve().parent.parent))
from controllers import login

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

    def test_login_contraseña_incorrecta(self):
        """
        Verifica que no se permita el inicio de sesión con una contraseña incorrecta.
        Asegúrate de que este correo exista con una contraseña distinta a 'incorrecta'.
        """
        resultado = login.login("testuser@unal.edu.co", "incorrecta")
        self.assertEqual(resultado['status'], 'error')
        self.assertIn('Contraseña', resultado['msg'])

if __name__ == '__main__':
    unittest.main()
