import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    database='UN_Mapa'
);

if connection.is_connected():
    print("Conexión exitosa a la base de datos.")
    
connection.close()