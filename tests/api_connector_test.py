import requests
from unittest import mock
from collector.connectors.api_connector import APIConnector

@mock.patch('requests.get')
def test_api_connector_get(mock_get):
    config = {
        'endpoint': 'https://api.example.com/data',
        'method': 'GET',
        'headers': {'Authorization': 'Bearer token'}
    }

    # Mock the API response
    mock_response = mock.Mock()
    mock_response.json.return_value = [{'id': 1, 'name': 'Test'}, {'id': 2, 'name': 'Example'}]
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Initialize the connector and fetch data
    connector = APIConnector(config)
    data = connector.fetch_data()

    # Assert the data matches the mocked API response
    assert data == [{'id': 1, 'name': 'Test'}, {'id': 2, 'name': 'Example'}]
    mock_get.assert_called_once_with('https://api.example.com/data', headers={'Authorization': 'Bearer token'})

@mock.patch('requests.post')
def test_api_connector_post(mock_post):
    config = {
        'endpoint': 'https://api.example.com/data',
        'method': 'POST',
        'headers': {'Authorization': 'Bearer token'},
        'body': {'key': 'value'}
    }

    # Mock the API response
    mock_response = mock.Mock()
    mock_response.json.return_value = [{'id': 1, 'name': 'Test'}]
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    # Initialize the connector and fetch data
    connector = APIConnector(config)
    data = connector.fetch_data()

    # Assert the data matches the mocked API response
    assert data == [{'id': 1, 'name': 'Test'}]
    mock_post.assert_called_once_with('https://api.example.com/data', headers={'Authorization': 'Bearer token'}, json={'key': 'value'})
