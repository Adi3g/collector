from sqlalchemy import create_engine

class SQLConnector:
    """
    SQLConnector handles connections to SQL databases and fetches data.

    :param config: Configuration details for connecting to the SQL database.
    :type config: dict
    """

    def __init__(self, config):
        """
        Initializes the SQLConnector with database configuration.

        :param config: A dictionary containing connection details such as host, port, username, password, and database name.
        :type config: dict
        """
        self.config = config
        self.engine = None

    def connect(self):
        """
        Establishes a connection to the SQL database using SQLAlchemy.

        :raises sqlalchemy.exc.SQLAlchemyError: If a connection cannot be established.
        """
        connection_string = f"postgresql://{self.config['username']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['database']}"
        self.engine = create_engine(connection_string)
        print(f"Connected to SQL database: {self.config['database']}")

    def fetch_data(self, query):
        """
        Executes a SQL query and fetches data from the database.

        :param query: SQL query string to execute.
        :type query: str
        :return: A list of rows fetched from the database, where each row is a dictionary.
        :rtype: list of dict
        :raises sqlalchemy.exc.SQLAlchemyError: If the query fails to execute.
        """
        if not self.engine:
            self.connect()
        with self.engine.connect() as connection:
            result = connection.execute(query)
            data = [dict(row) for row in result]
        return data
