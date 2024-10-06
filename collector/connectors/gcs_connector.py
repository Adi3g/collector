from google.cloud import storage
from collector.utils.logger import get_logger

class GCSConnector:
    """
    GCSConnector handles fetching files from Google Cloud Storage.

    :param config: Configuration details for connecting to the GCS bucket.
    :type config: dict
    """

    def __init__(self, config):
        """
        Initializes the GCSConnector with GCP credentials and bucket details.

        :param config: A dictionary containing connection details like bucket name, object name, and credentials.
        :type config: dict
        """
        self.config = config
        self.client = storage.Client.from_service_account_json(config['google_cloud_key_file'])
        self.bucket = self.client.bucket(config['bucket'])
        self.logger = get_logger("GCSConnector")

    def fetch_data(self):
        """
        Fetches data from a GCS bucket.

        :return: The content of the file from GCS.
        :rtype: str
        """
        try:
            self.logger.info(f"Fetching data from GCS bucket: {self.config['bucket']}, object: {self.config['object']}")
            blob = self.bucket.blob(self.config['object'])
            data = blob.download_as_text()
            return data
        except Exception as e:
            self.logger.error(f"Error fetching data from GCS: {e}")
            raise
