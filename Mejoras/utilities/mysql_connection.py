from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import json


class MySQLConnection:
    def __init__(self, connection_json_path):
        self.connection_json_path = connection_json_path

    def connect_to_mysql(self):
        # This function establishes a connection to a MySQL database using credentials stored in a JSON file.
        # It reads the JSON file to get the username, password, server, and database name, then creates an SQLAlchemy engine.
        # The engine is used to interact with the database.
        with open(self.connection_json_path, 'r') as file:
            credenciales_lyft = json.load(file)

        engine = create_engine(f"mysql+pymysql://{credenciales_lyft['USERNAME']}:{credenciales_lyft['PASSWORD']}@{credenciales_lyft['SERVER']}/{credenciales_lyft['DATABASE']}")
        print(f"Conexión a MySQL establecida exitosamente: {engine}")
        return engine