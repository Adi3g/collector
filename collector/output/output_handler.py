# collector/output/output_handler.py

import pandas as pd

class OutputHandler:
    """
    OutputHandler manages the output of transformed data into specified formats.

    :param output_config: Configuration details for output, including type and options.
    :type output_config: dict
    """

    def __init__(self, output_config):
        """
        Initializes the OutputHandler with output configuration.

        :param output_config: Output settings from the configuration file.
        :type output_config: dict
        """
        self.output_config = output_config

    def save(self, data):
        """
        Saves the transformed data to the specified format and path.

        :param data: The transformed data to be outputted.
        :type data: list of dict
        :raises ValueError: If an unsupported output type is specified.
        """
        output_type = self.output_config['type']
        if output_type == 'csv':
            self._save_csv(data)
        elif output_type == 'json':
            self._save_json(data)
        elif output_type == 'parquet':
            self._save_parquet(data)
        else:
            raise ValueError(f"Unsupported output type: {output_type}")

    def _save_csv(self, data):
        """
        Saves the data as a CSV file.

        :param data: The data to save as CSV.
        :type data: list of dict
        """
        df = pd.DataFrame(data)
        df.to_csv(self.output_config['details']['path'], index=False)
        print(f"Data saved as CSV at {self.output_config['details']['path']}")

    def _save_json(self, data):
        """
        Saves the data as a JSON file.

        :param data: The data to save as JSON.
        :type data: list of dict
        """
        df = pd.DataFrame(data)
        df.to_json(self.output_config['details']['path'], orient='records', indent=2)
        print(f"Data saved as JSON at {self.output_config['details']['path']}")

    def _save_parquet(self, data):
        """
        Saves the data as a Parquet file.

        :param data: The data to save as Parquet.
        :type data: list of dict
        """
        df = pd.DataFrame(data)
        df.to_parquet(self.output_config['details']['path'], compression=self.output_config['details'].get('compression', 'snappy'))
        print(f"Data saved as Parquet at {self.output_config['details']['path']}")
