import datetime
from collector.connectors.api_connector import APIConnector
from collector.connectors.mongodb_connector import MongoDBConnector
from collector.core.config_parser import CollectorConfigParser
from collector.core.validator import ColValidator  # Import the validator
from collector.connectors.sql_connector import SQLConnector
from collector.output.output_handler import OutputHandler
from collector.utils.logger import get_logger

class Collector:
    """
    The Collector class is responsible for loading configuration, initializing connectors, 
    collecting data, transforming data, and handling output.
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

    def validate_config(self):
        """
        Validates the configuration file using ColValidator.
        """
        validator = ColValidator(self.config)
        if not validator.validate():
            self.logger.error("Configuration validation failed.")
            raise ValueError("Invalid .col configuration file.")
        self.logger.info("Configuration validated successfully.")

    def initialize_connectors(self):
        """
        Initializes data source connectors based on the configuration.
        """
        self.logger.info("Initializing connectors")

        for source in self.config['sources']:
            if source['type'] == 'sql':
                # Initialize the SQLConnector with source details
                connector = SQLConnector(source['details'])
                self.sources.append(connector)
                self.logger.info(f"Initialized SQL connector for database: {source['details'].get('database')}")
            elif source['type'] == 'api':
                # Initialize the APIConnector with source details
                connector = APIConnector(source['details'])
                self.sources.append(connector)
                self.logger.info(f"Initialized API connector for endpoint: {source['details'].get('endpoint')}")
            elif source['type'] == 'mongodb':
                # MongoDBConnector initialization
                connector = MongoDBConnector(source['details'])
                self.sources.append(connector)
                self.logger.info(f"Initialized MongoDB connector for collection: {source['details'].get('collection')}")
            else:
                self.logger.error(f"Unsupported source type: {source['type']}")
                raise ValueError(f"Unsupported source type: {source['type']}")

        if not self.sources:
            self.logger.error("No valid data sources found.")
            raise ValueError("No valid data sources found.")

    def collect_data(self):
        """
        Collects data from all initialized connectors (SQL, API, etc.).
        
        :return: A list containing the data collected from each source.
        :rtype: list
        """
        self.logger.info("Collecting data from sources")
        
        all_data = []

        for connector in self.sources:
            if isinstance(connector, SQLConnector):
                # SQL connectors fetch data using SQL queries
                data = connector.fetch_data(connector.config['query'])
                self.logger.info(f"Collected {len(data)} rows from SQL source: {connector.config.get('database')}")
            elif isinstance(connector, APIConnector):
                # API connectors fetch data without a query
                data = connector.fetch_data()  # No query required for API
                self.logger.info(f"Collected data from API source: {connector.config.get('endpoint')}")
            else:
                self.logger.error(f"Unsupported connector type: {type(connector).__name__}")
                raise ValueError(f"Unsupported connector type: {type(connector).__name__}")
            
            if isinstance(data, list):
                all_data.extend(data)
            else:
                all_data.append(data)

        if not all_data:
            self.logger.error("No data collected from any source.")
            raise ValueError("No data collected from any source.")

        return all_data


    def _apply_date_format(self, date_str, date_format):
        """
        Converts a date string to the specified format.
        """
        try:
            formatted_date = datetime.strptime(date_str, date_format).strftime(date_format)
            return formatted_date
        except ValueError as e:
            self.logger.error(f"Date format error: {e}")
            return date_str

    def transform_data(self, raw_data):
        """
        Transforms the raw data based on the transformation rules specified in the configuration.
        
        :param raw_data: The raw data collected from the sources.
        :type raw_data: list of dict
        :return: Transformed data.
        :rtype: list of dict
        """
        self.logger.info("Transforming data")
        
        transformed_data = []
        
        for row in raw_data:
            transformed_row = row.copy()
            
            for transform in self.config['transformations']:
                # Get the source field that needs to be transformed
                source_field = transform['source']
                target_field = transform['target']
                rules = transform['rules']
                
                # Apply transformation rules to the row
                if source_field in transformed_row:
                    for rule in rules:
                        if rule['type'] == 'date':
                            # Convert to a date format if the type is specified as date
                            transformed_row[target_field] = self._apply_date_format(transformed_row[source_field], rule['format'])
                        elif rule['type'] == 'float':
                            # Convert the value to a float
                            transformed_row[target_field] = float(transformed_row[source_field])
                        elif 'default' in rule:
                            # Apply default value if specified
                            transformed_row[target_field] = transformed_row.get(source_field, rule['default'])
            
            transformed_data.append(transformed_row)
        
        self.logger.info(f"Transformed {len(transformed_data)} rows")
        return transformed_data

    def output_data(self, transformed_data):
        """
        Outputs the transformed data using the OutputHandler based on the configuration.

        :param transformed_data: The transformed data to output.
        :type transformed_data: list of dict
        """
        output_config = self.config['output']
        output_handler = OutputHandler(output_config)  # Initialize OutputHandler with the configuration
        try:
            self.logger.info(f"Outputting data using OutputHandler as {output_config['type']}")
            output_handler.write_output(transformed_data)  # Delegate output to OutputHandler
            self.logger.info(f"Data successfully written to {output_config['details']['path']}")
        except Exception as e:
            self.logger.error(f"Failed to output data: {e}")
            raise


    def run(self):
        """
        Executes the full data collection, transformation, and output process.
        """
        self.logger.info("Starting collector")
        self.load_config()

        # Validate the configuration before proceeding
        self.validate_config()

        self.initialize_connectors()
        raw_data = self.collect_data()
        transformed_data = self.transform_data(raw_data)
        self.output_data(transformed_data)
        self.logger.info("Collector run complete")
