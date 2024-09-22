from sqlalchemy import create_engine, text

from collector.utils.logger import get_logger

class SQLConnector:
    """
    SQLConnector handles connections to SQL databases and fetches data.
    
    :param config: Configuration details for connecting to the SQL database.
    :type config: dict
    """

    def __init__(self, config):
        """
        Initializes the SQLConnector with database configuration.
        
        :param config: A dictionary containing connection details such as db_type, host, port, username, password, and database name.
        :type config: dict
        """
        self.config = config
        self.engine = None
        self.logger = get_logger()

    def connect(self):
        """
        Establishes a connection to the SQL database using SQLAlchemy.

        :raises sqlalchemy.exc.SQLAlchemyError: If a connection cannot be established.
        """
        db_type = self.config.get('db_type', 'postgresql')  # Default to PostgreSQL if not specified
        connection_string = self._generate_connection_string(db_type)
        self.engine = create_engine(connection_string)
        self.logger.info(f"Connected to SQL database: {self.config.get('database')}")

    def _generate_connection_string(self, db_type):
        """
        Generates a database connection string based on the db_type and configuration.

        :param db_type: The type of database (e.g., 'postgresql', 'mysql', 'sqlite').
        :type db_type: str
        :return: A connection string.
        :rtype: str
        """
        if db_type == 'sqlite':
            # SQLite doesn't need host, port, username, or password, only a file path
            db_path = self.config.get('database', ':memory:')  # Use in-memory database if not specified
            return f'sqlite:///{db_path}'
        else:
            # Default to other SQL databases (PostgreSQL, MySQL, etc.)
            username = self.config.get('username')
            password = self.config.get('password')
            host = self.config.get('host', 'localhost')
            port = self.config.get('port', 5432)  # Default to port 5432 for PostgreSQL-like databases
            database = self.config.get('database')
            return f"{db_type}://{username}:{password}@{host}:{port}/{database}"

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

        try:
            # Wrap the query in `text()` to ensure it's treated as an SQLAlchemy-compatible object
            with self.engine.connect() as connection:
                result = connection.execute(text(query))

                # Use the `mappings()` method to convert rows to dictionaries
                data = [dict(row) for row in result.mappings()]
                self.logger.info(f"Fetched {len(data)} rows")
            return data
        except Exception as e:
            self.logger.error(f"Query failed: {e}")
            raise
