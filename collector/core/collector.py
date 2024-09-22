from collector.core.config_parser import CollectorConfigParser
from collector.connectors.sql_connector import SQLConnector
from collector.output.output_handler import OutputHandler
from collector.utils.logger import get_logger

class Collector:
    """
    The Collector class is responsible for loading configuration, initializing connectors, 
    collecting data, transforming data, and handling output.

    :param config_path: Path to the configuration (.col) file.
    :type config_path: str
    """

    def __init__(self, config_path):
        """
        Initializes the Collector with the specified configuration path.

        :param config_path: The path to the .col configuration file.
        :type config_path: str
        """
        self.config_path = config_path
        self.config = None
        self.sources = []
        self.transformer = None
        self.output = None
        self.logger = get_logger()  # Initialize logger

    def load_config(self):
        """
        Loads the configuration from the .col file using the CollectorConfigParser.
        """
        try:
            self.logger.info(f"Loading configuration from {self.config_path}")
            parser = CollectorConfigParser(self.config_path)
            self.config = parser.parse()
            self.logger.info("Configuration loaded successfully")
        except FileNotFoundError as e:
            self.logger.error(f"Configuration file not found: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            raise

    def initialize_connectors(self):
        """
        Initializes data source connectors based on the configuration.
        Currently supports SQL connectors.
        """
        self.logger.info("Initializing connectors")
        for source in self.config['sources']:
            if source['type'] == 'sql':
                connector = SQLConnector(source['details'])
                self.sources.append(connector)
                self.logger.debug(f"Initialized SQL connector for {source['details']['database']}")
        self.logger.info(f"Initialized {len(self.sources)} connectors")

    def collect_data(self):
        """
        Collects data from all initialized connectors.
        """
        all_data = []
        self.logger.info("Collecting data from sources")
        for connector in self.sources:
            data = connector.fetch_data(connector.config['query'])
            all_data.extend(data)
            self.logger.debug(f"Collected {len(data)} rows from source")
        return all_data

    def transform_data(self, data):
        """
        Transforms the collected data according to the transformation rules defined in the configuration.
        """
        self.logger.info("Transforming data")
        # Placeholder for transformation logic
        transformed_data = data  # Add actual transformation logic here
        self.logger.debug(f"Transformed data: {transformed_data}")
        return transformed_data

    def output_data(self, transformed_data):
        """
        Handles the output of transformed data as specified in the configuration.
        """
        self.logger.info(f"Outputting data")
        self.output = OutputHandler(self.config['output'])
        self.output.save(transformed_data)
        self.logger.info("Data output complete")

    def run(self):
        """
        Executes the full data collection, transformation, and output process.
        """
        self.logger.info("Starting collector")
        self.load_config()
        self.initialize_connectors()
        raw_data = self.collect_data()
        transformed_data = self.transform_data(raw_data)
        self.output_data(transformed_data)
        self.logger.info("Collector run complete")
