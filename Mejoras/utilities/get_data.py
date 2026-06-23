# Importar la clase MySQLConnection desde el módulo mysql_connection para establecer la conexión a la base de datos MySQL
# y obtener el engine.
import mysql_connection
import pandas as pd
from datetime import datetime
from pathlib import Path
from pathlib import Path # agregado x Tsuna -- para craer lacarpeta si es que no existe 

class GetData:
    def __init__(self, connection_json_path):
        self.connection_json_path = connection_json_path
        # Asumo que mysql_connection es tu módulo personalizado
        self.mysql_connection = mysql_connection.MySQLConnection(connection_json_path).connect_to_mysql()

    def _read_file(self, file_path):
        """Lee el contenido de un archivo SQL."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            raise Exception(f"Error: No se encontró el archivo en {file_path}")

    def run_sql(self, query):
        """Extrae la consulta del archivo y la ejecuta en la BD."""
        # Ejecutar con pandas
        try:
           
            data = pd.read_sql(query, self.mysql_connection)
            #print(f"Carga finalizada. Registros obtenidos: {len(data):,}")
            
            return data
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
