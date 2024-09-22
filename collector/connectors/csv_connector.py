import pandas as pd

class CSVConnector:
    """
    CSVConnector reads data from a CSV file and returns it as a list of dictionaries.
    
    :param config: Configuration for the CSV file (file path, delimiter, etc.).
    :type config: dict
    """

    def __init__(self, config):
        """
        Initializes the CSVConnector with the specified configuration.
        
        :param config: A dictionary containing configuration details such as file_path and delimiter.
        :type config: dict
        """
        self.file_path = config['file_path']
        self.delimiter = config.get('delimiter', ',')
    
    def fetch_data(self):
        """
        Reads the CSV file and returns the data as a list of dictionaries.
        
        :return: A list of rows from the CSV file, where each row is a dictionary.
        :rtype: list of dict
        """
        try:
            df = pd.read_csv(self.file_path, delimiter=self.delimiter)
            return df.to_dict(orient='records')
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            raise
