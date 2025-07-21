import bcrypt
import re

def registrar_usuario(correo, password):
    if not re.match(r'^[\w\.-]+@unal\.edu\.co$', correo):
        return {'status': 'error', 'msg': 'El correo debe ser institucional (@unal.edu.co)'}
    
    if not es_contraseña_segura(password):
        return {"status": "error", "msg": "La contraseña no cumple con los requisitos de seguridad"}

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    from config.conexion import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verificar si ya existe    
    cursor.execute("SELECT * FROM Usuario WHERE correo = %s", (correo,))
    if cursor.fetchone():
        return {'status': 'error', 'msg': 'El usuario ya está registrado'}

    cursor.execute("""
        INSERT INTO Usuario (nombre, correo, contrasena, rol)
        VALUES (%s, %s, %s, %s)
    """, (correo.split("@")[0], correo, hashed, "usuario"))

    conn.commit()
    cursor.close()
    conn.close()

    return {'status': 'ok', 'msg': 'Usuario registrado correctamente'} 

def login(correo, password):
    from config.conexion import get_connection
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id_usuario, nombre, correo, contrasena, rol FROM Usuario WHERE correo = %s", (correo,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        return {'status': 'error', 'msg': 'Usuario no encontrado'}

    if bcrypt.checkpw(password.encode(), user[3].encode()):
        return {
            'status': 'ok',
            'usuario': {
                'id': user[0],
                'nombre': user[1],
                'email': user[2],
                'rol': user[4]
            }
        }
    else:
        return {'status': 'error', 'msg': 'Contraseña incorrecta'}
    
def es_contraseña_segura(contraseña):
    return (
        len(contraseña) >= 8 and
        re.search(r"[A-Z]", contraseña) and
        re.search(r"[a-z]", contraseña) and
        re.search(r"\d", contraseña) and
        re.search(r"[^A-Za-z0-9]", contraseña)
    )
