from collector.core.config_parser import CollectorConfigParser
from collector.connectors.sql_connector import SQLConnector

class Collector:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = None
        self.sources = []
        self.transformer = None
        self.output = None

    def load_config(self):
        parser = CollectorConfigParser(self.config_path)
        self.config = parser.parse()
        print("Configuration loaded successfully")

    def initialize_connectors(self):
        for source in self.config['sources']:
            if source['type'] == 'sql':
                connector = SQLConnector(source['details'])
                self.sources.append(connector)
        print(f"Initialized {len(self.sources)} connectors")

    def collect_data(self):
        all_data = []
        for connector in self.sources:
            data = connector.fetch_data(connector.config['query'])
            all_data.extend(data)
        return all_data

    def transform_data(self, data):
        # Placeholder for transformation logic
        return data

    def output_data(self, transformed_data):
        # Placeholder for output logic
        print("Outputting data:", transformed_data)

    def run(self):
        self.load_config()
        self.initialize_connectors()
        raw_data = self.collect_data()
        transformed_data = self.transform_data(raw_data)
        self.output_data(transformed_data)
