import requests

class APIConnector:
    """
    APIConnector fetches data from an API and returns it as a list of dictionaries.
    
    :param config: Configuration for the API (endpoint, method, headers, etc.).
    :type config: dict
    """

    def __init__(self, config):
        """
        Initializes the APIConnector with the specified configuration.
        
        :param config: A dictionary containing configuration details such as endpoint, method, headers, and body.
        :type config: dict
        """
        self.endpoint = config['endpoint']
        self.method = config.get('method', 'GET')
        self.headers = config.get('headers', {})
        self.body = config.get('body', None)

    def fetch_data(self):
        """
        Sends an API request and returns the response data as a list of dictionaries (assuming the API returns JSON).
        
        :return: A list of rows from the API response.
        :rtype: list of dict
        """
        try:
            if self.method.upper() == 'GET':
                response = requests.get(self.endpoint, headers=self.headers)
            elif self.method.upper() == 'POST':
                response = requests.post(self.endpoint, headers=self.headers, json=self.body)
            else:
                raise ValueError(f"Unsupported method: {self.method}")
            
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()  # Assume the response is JSON

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            raise
