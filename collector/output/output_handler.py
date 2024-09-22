import pandas as pd
import json

class OutputHandler:
    """
    Handles outputting the transformed data to different formats (CSV, JSON, Parquet).
    """

    def __init__(self, output_config):
        """
        Initializes the OutputHandler with the output configuration.

        :param output_config: The configuration specifying output format and path.
        :type output_config: dict
        """
        self.output_type = output_config['type']
        details = output_config.get('details', {})
        self.output_path = details.get('path', None)
        self.options = details.get('options', {})

    def write_output(self, data):
        """
        Writes the data to the specified format (CSV, JSON, Parquet).
        
        :param data: The data to be written.
        :type data: list of dict
        """
        if self.output_type == 'csv':
            self._write_csv(data)
        elif self.output_type == 'json':
            self._write_json(data)
        elif self.output_type == 'parquet':
            self._write_parquet(data)
        else:
            raise ValueError(f"Unsupported output type: {self.output_type}")

    def _write_csv(self, data):
        """
        Outputs data to a CSV file.

        :param data: The data to output.
        :type data: list of dict
        """
        df = pd.DataFrame(data)  # Convert data to DataFrame
        df.to_csv(self.output_path, index=False)

    def _write_json(self, data):
        """
        Outputs data to a JSON file.

        :param data: The data to output.
        :type data: list of dict
        """
        with open(self.output_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def _write_parquet(self, data):
        """
        Outputs data to a Parquet file with optional compression.

        :param data: The data to output.
        :type data: list of dict
        """
        df = pd.DataFrame(data)  # Convert data to DataFrame
        compression = self.options.get('compression', None)  # Get compression option, if specified
        df.to_parquet(self.output_path, compression=compression)
