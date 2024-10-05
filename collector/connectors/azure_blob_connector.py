from azure.storage.blob import BlobServiceClient
from collector.utils.logger import get_logger

class AzureBlobConnector:
    """
    AzureBlobConnector handles fetching files from Azure Blob Storage.

    :param config: Configuration details for connecting to the Azure Blob Storage.
    :type config: dict
    """

    def __init__(self, config):
        """
        Initializes the AzureBlobConnector with Azure credentials and container details.

        :param config: A dictionary containing connection details like container name, blob name, and credentials.
        :type config: dict
        """
        self.config = config
        self.blob_service_client = BlobServiceClient(
            account_url=f"https://{config['azure_storage_account']}.blob.core.windows.net",
            credential=config['azure_storage_key']
        )
        self.logger = get_logger("AzureBlobConnector")

    def fetch_data(self):
        """
        Fetches data from an Azure Blob Storage container.

        :return: The content of the blob from Azure Blob Storage.
        :rtype: str
        """
        try:
            self.logger.info(f"Fetching data from Azure Blob container: {self.config['container']}, blob: {self.config['blob']}")
            blob_client = self.blob_service_client.get_blob_client(container=self.config['container'], blob=self.config['blob'])
            blob_data = blob_client.download_blob().readall().decode('utf-8')
            return blob_data
        except Exception as e:
            self.logger.error(f"Error fetching data from Azure Blob Storage: {e}")
            raise
