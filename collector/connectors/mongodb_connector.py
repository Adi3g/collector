from pymongo import MongoClient
from collector.utils.logger import get_logger

class MongoDBConnector:
    """
    MongoDBConnector handles connections to a MongoDB database and fetches data from collections.

    :param config: Configuration details for connecting to the MongoDB database.
    :type config: dict
    """

    def __init__(self, config):
        """
        Initializes the MongoDBConnector with database configuration.

        :param config: A dictionary containing connection details such as host, port, database, collection, and query.
        :type config: dict
        """
        self.config = config
        self.client = None
        self.database = None
        self.collection = None
        self.logger = get_logger("MongoDBConnector")

    def connect(self):
        """
        Establishes a connection to the MongoDB database.
        """
        try:
            connection_string = f"mongodb://{self.config['host']}:{self.config['port']}"
            self.client = MongoClient(connection_string)
            self.database = self.client[self.config['database']]
            self.collection = self.database[self.config['collection']]
            self.logger.info(f"Connected to MongoDB: {self.config['database']} -> {self.config['collection']}")
        except Exception as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def fetch_data(self):
        """
        Fetches data from the MongoDB collection based on the specified query.

        :return: A list of documents fetched from the MongoDB collection.
        :rtype: list of dict
        :raises pymongo.errors.PyMongoError: If there is an error executing the query.
        """
        try:
            if not self.client:
                self.connect()
            query = eval(self.config.get('query', '{}'))  # Ensure query is evaluated as a dictionary
            data = list(self.collection.find(query))
            self.logger.info(f"Fetched {len(data)} documents from MongoDB collection")
            return data
        except Exception as e:
            self.logger.error(f"Error fetching data from MongoDB: {e}")
            raise
