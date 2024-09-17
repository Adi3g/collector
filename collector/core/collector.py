from collector.core.config_parser import CollectorConfigParser
from collector.connectors.sql_connector import SQLConnector
from collector.core.transformer import DataTransformer
from collector.output.output_handler import OutputHandler


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

    def load_config(self):
        """
        Loads the configuration from the .col file using the CollectorConfigParser.

        :raises FileNotFoundError: If the configuration file cannot be found.
        :raises ValueError: If the configuration is invalid.
        """
        parser = CollectorConfigParser(self.config_path)
        self.config = parser.parse()
        print("Configuration loaded successfully")

    def initialize_connectors(self):
        """
        Initializes data source connectors based on the configuration.
        Currently supports SQL connectors.
        """
        for source in self.config['sources']:
            if source['type'] == 'sql':
                connector = SQLConnector(source['details'])
                self.sources.append(connector)
        print(f"Initialized {len(self.sources)} connectors")

    def collect_data(self):
        """
        Collects data from all initialized connectors.

        :return: A list of collected data from all sources.
        :rtype: list
        """
        all_data = []
        for connector in self.sources:
            data = connector.fetch_data(connector.config['query'])
            all_data.extend(data)
        return all_data

    def transform_data(self, data):
        """
        Transforms the collected data according to the transformation rules defined in the configuration.

        :param data: The raw data collected from sources.
        :type data: list
        :return: Transformed data.
        :rtype: list
        """
        # Placeholder for transformation logic
        return data

    def output_data(self, transformed_data):
        """
        Handles the output of transformed data as specified in the configuration.

        :param transformed_data: The data after applying transformations.
        :type transformed_data: list
        """
        # Placeholder for output logic
        print("Outputting data:", transformed_data)

    def run(self):
        """
        Executes the full data collection, transformation, and output process.
        """
        self.load_config()
        self.initialize_connectors()
        raw_data = self.collect_data()
        transformed_data = self.transform_data(raw_data)
        self.output_data(transformed_data)

    def initialize_transformer(self):
        """
        Initializes the data transformer with transformation rules from the configuration.
        """
        self.transformer = DataTransformer(self.config['transformations'])
        print("Data transformer initialized")

    def transform_data(self, data):
        """
        Transforms the collected data using the initialized data transformer.

        :param data: The raw data collected from sources.
        :type data: list
        :return: Transformed data.
        :rtype: list
        """
        return self.transformer.transform(data)


    def initialize_output_handler(self):
        """
        Initializes the output handler with the output settings from the configuration.
        """
        self.output = OutputHandler(self.config['output'])
        print("Output handler initialized")

    def output_data(self, transformed_data):
        """
        Outputs the transformed data using the initialized output handler.

        :param transformed_data: The data after applying transformations.
        :type transformed_data: list
        """
        self.output.save(transformed_data)

    def run(self):
        self.load_config()
        self.initialize_connectors()
        self.initialize_transformer()
        self.initialize_output_handler()
        raw_data = self.collect_data()
        transformed_data = self.transform_data(raw_data)
        self.output_data(transformed_data)

