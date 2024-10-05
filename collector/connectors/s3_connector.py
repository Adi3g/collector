import pandas as pd
import json
import csv
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
        Fetches data from an S3 bucket, supports CSV, JSON, and Parquet formats.

        :return: Parsed data from S3, depending on file format.
        :rtype: list of dict for CSV/JSON, pandas.DataFrame for Parquet.
        """
        try:
            self.logger.info(f"Fetching data from S3 bucket: {
                             self.config['bucket']}, key: {self.config['key']}")
            response = self.s3.get_object(
                Bucket=self.config['bucket'], Key=self.config['key'])
            file_data = response['Body'].read().decode('utf-8')

            # Handle different file formats
            if self.config['key'].endswith('.csv'):
                return self._parse_csv(file_data)
            elif self.config['key'].endswith('.json'):
                return self._parse_json(file_data)
            elif self.config['key'].endswith('.parquet'):
                return self._parse_parquet(file_data)
            else:
                raise ValueError("Unsupported file format")

        except Exception as e:
            self.logger.error(f"Error fetching data from S3: {e}")
            raise

    def _parse_csv(self, file_data):
        """Parses CSV file content."""
        reader = csv.DictReader(file_data.splitlines())
        return [row for row in reader]

    def _parse_json(self, file_data):
        """Parses JSON file content."""
        return json.loads(file_data)

    def _parse_parquet(self, file_data):
        """Parses Parquet file content using pandas."""
        return pd.read_parquet(file_data)
