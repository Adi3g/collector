import boto3
from collector.utils.logger import get_logger

class S3Connector:
    """
    S3Connector handles fetching files from AWS S3.

    :param config: Configuration details for connecting to the S3 bucket.
    :type config: dict
    """

    def __init__(self, config):
        """
        Initializes the S3Connector with AWS credentials and bucket details.

        :param config: A dictionary containing connection details like bucket name, key, and credentials.
        :type config: dict
        """
        self.config = config
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=config['aws_access_key'],
            aws_secret_access_key=config['aws_secret_key']
        )
        self.logger = get_logger("S3Connector")

    def fetch_data(self):
        """
        Fetches data from an S3 bucket.

        :return: The content of the file from S3.
        :rtype: str
        """
        try:
            self.logger.info(f"Fetching data from S3 bucket: {self.config['bucket']}, key: {self.config['key']}")
            response = self.s3.get_object(Bucket=self.config['bucket'], Key=self.config['key'])
            data = response['Body'].read().decode('utf-8')
            return data
        except Exception as e:
            self.logger.error(f"Error fetching data from S3: {e}")
            raise
