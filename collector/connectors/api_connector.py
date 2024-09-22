import requests

class APIConnector:
    """
    Handles connections to API data sources and fetches data.
    
    :param config: Configuration details for connecting to the API.
    :type config: dict
    """

    def __init__(self, config):
        """
        Initializes the APIConnector with API configuration.

        :param config: A dictionary containing connection details such as endpoint, method, headers, and query params.
        :type config: dict
        """
        self.config = config
        self.endpoint = config['endpoint']
        self.method = config['method']
        self.headers = config.get('headers', {})
        self.query_params = config.get('query_params', {})

    def fetch_data(self):
        """
        Executes an API request and fetches data.

        :return: The response data from the API.
        :rtype: dict
        :raises requests.exceptions.RequestException: If the API request fails.
        """
        try:
            if self.method.upper() == 'GET':
                response = requests.get(self.endpoint, headers=self.headers, params=self.query_params)
            elif self.method.upper() == 'POST':
                response = requests.post(self.endpoint, headers=self.headers, json=self.query_params)
            else:
                raise ValueError(f"Unsupported HTTP method: {self.method}")

            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()  # Return the JSON response
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")
