from unittest import mock
from collector.connectors.sql_connector import SQLConnector

@mock.patch('collector.connectors.sql_connector.create_engine')
def test_sql_connector(mock_create_engine):
    # Mock configuration for SQLConnector
    config = {
        'host': 'localhost',
        'port': 5432,
        'username': 'user',
        'password': 'pass',
        'database': 'test_db'
    }

    # Mock the database engine and connection
    mock_engine = mock_create_engine.return_value
    mock_connection = mock_engine.connect.return_value.__enter__.return_value

    # Mock the result of the query execution
    mock_result = [{'id': 1, 'name': 'Test'}, {'id': 2, 'name': 'Example'}]
    mock_connection.execute.return_value = iter(mock_result)  # Return an iterable object
    
    # Initialize the connector and run the query
    connector = SQLConnector(config)
    connector.connect()
    data = connector.fetch_data("SELECT * FROM test_table")

    # Assertions
    mock_create_engine.assert_called_once_with(
        "postgresql://user:pass@localhost:5432/test_db"
    )
    mock_connection.execute.assert_called_once_with("SELECT * FROM test_table")
    assert data == [{'id': 1, 'name': 'Test'}, {'id': 2, 'name': 'Example'}]  # Assert the data matches the mock result
