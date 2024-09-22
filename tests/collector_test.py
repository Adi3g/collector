from collector.core.collector import Collector
from unittest import mock
import os


def test_collector_initialization():
    collector = Collector(config_path='path/to/config.col')
    assert collector.config_path == 'path/to/config.col'


@mock.patch('collector.connectors.sql_connector.SQLConnector.fetch_data')
@mock.patch('collector.output.output_handler.OutputHandler.save')
def test_collector_with_file(mock_output_save, mock_sql_fetch_data, tmpdir):
    # Mock the fetch_data method to return some test data
    mock_sql_fetch_data.return_value = [{'id': 1, 'name': 'Test Name'}]

    # Mock the output saving
    output_file = os.path.join(tmpdir, 'test_output.json')
    mock_output_save.return_value = None  # No need to simulate a real save

    # Create a test .col file path
    config_path = 'examples/test_config.col'

    # Initialize the collector with the test configuration
    collector = Collector(config_path)
    collector.run()

    # Assertions
    mock_sql_fetch_data.assert_called_once_with("SELECT * FROM test_table")
    mock_output_save.assert_called_once_with([{'id': 1, 'name': 'Test Name'}])

    # You can also verify that the output path was used, if applicable
    assert mock_output_save.call_count == 1
