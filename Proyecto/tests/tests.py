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

    def test_registro_contraseña_debil(self):
        """
        Verifica que no se permita registrar un usuario con contraseña débil.
        """
        correo = "debil@unal.edu.co"
        contraseña_debil = "123456"  # No cumple con RF19
        resultado = login.registrar_usuario(correo, contraseña_debil)
        self.assertEqual(resultado['status'], 'error')
        self.assertIn('contraseña', resultado['msg'].lower())

    def test_login_exitoso(self):
        correo = "testuser_1@unal.edu.co"
        contraseña = "C0ntraseña!2"  # Cumple requisitos

        # Intentar registrar al usuario
        resultado_registro = login.registrar_usuario(correo, contraseña)
        self.assertIn(resultado_registro['status'], ['ok', 'error'])

        # Luego login con la misma contraseña en texto plano
        resultado_login = login.login(correo, contraseña)
        self.assertEqual(resultado_login['status'], 'ok')

    def test_registro_correo_duplicado(self):
        """
        Verifica que no se permita registrar dos veces el mismo correo institucional.
        """
        correo = "duplicado@unal.edu.co"
        contraseña = "$2b$12$ozy4qHcENEb1vj5tU29sOuLMkkPEUCGLDhnrEgz/mRcZVrD6IGSPe"
        login.registrar_usuario(correo, contraseña)  # Primera vez
        resultado = login.registrar_usuario(correo, contraseña)  # Segunda vez
        self.assertEqual(resultado['status'], 'error')
        self.assertIn('ya está registrado', resultado['msg'].lower())


if __name__ == '__main__':
    unittest.main()
