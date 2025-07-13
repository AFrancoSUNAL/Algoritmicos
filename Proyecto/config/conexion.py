import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    database='un_mapa_db'
);

if connection.is_connected():
    print("Conexión exitosa a la base de datos.")
    
connection.close()