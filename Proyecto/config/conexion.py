import mysql.connector
import json

def get_connection():
    with open('Proyecto/config/db_info.json', 'r') as db_info_file:
        db_info = json.load(db_info_file)

    connection = mysql.connector.connect(
        host=db_info["host"],
        user=db_info["user"],
        password=db_info["password"],
        database=db_info["database"],
        port=db_info["port"]
    );

    return connection