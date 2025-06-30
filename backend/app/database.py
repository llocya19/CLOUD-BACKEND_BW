# backend/app/database.py

import mysql.connector
from app.config import Config  # Importar la clase Config

def get_db():
    """Establece y devuelve una conexión a la base de datos."""
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=int(Config.DB_PORT),  # convertir a int por seguridad
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        print("Conexión exitosa a la base de datos")
        return connection
    except mysql.connector.Error as err:
        print(f"Error al conectar con la base de datos: {err}")
        return None

def close_connection(connection):
    if connection:
        connection.close()
        print("Conexión cerrada")
