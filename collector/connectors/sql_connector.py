
# collector/connectors/sql_connector.py

import sqlalchemy
from sqlalchemy import create_engine

class SQLConnector:
    def __init__(self, config):
        self.config = config
        self.engine = None

    def connect(self):
        connection_string = f"postgresql://{self.config['username']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['database']}"
        self.engine = create_engine(connection_string)
        print(f"Connected to SQL database: {self.config['database']}")

    def fetch_data(self, query):
        if not self.engine:
            self.connect()
        with self.engine.connect() as connection:
            result = connection.execute(query)
            data = [dict(row) for row in result]
        return data
