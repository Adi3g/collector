import pytest
from unittest import mock
from pymongo.errors import PyMongoError
from collector.connectors.mongodb_connector import MongoDBConnector

# Mocked MongoDB configuration
config = {
    'host': 'localhost',
    'port': 27017,
    'database': 'users',
    'collection': 'profiles',
    'query': "{'age': {'$gt': 25}}"
}

@pytest.fixture
def mongodb_connector():
    """Fixture for initializing MongoDBConnector."""
    return MongoDBConnector(config)

@mock.patch('collector.connectors.mongodb_connector.MongoClient')
def test_mongodb_connector_fetch_data(mock_mongo_client, mongodb_connector):
    """
    Test the MongoDBConnector fetch_data method by mocking the MongoDB client and collection.
    """
    # Mock database and collection
    mock_db = mock_mongo_client.return_value[config['database']]
    mock_collection = mock_db[config['collection']]
    
    # Simulate MongoDB find() results
    mock_collection.find.return_value = [
        {'name': 'John Doe', 'age': 30},
        {'name': 'Jane Doe', 'age': 35}
    ]
    
    # Fetch data using MongoDBConnector
    data = mongodb_connector.fetch_data()

    # Assertions
    assert len(data) == 2
    assert data[0]['name'] == 'John Doe'
    assert data[1]['age'] == 35
    mock_collection.find.assert_called_once_with({'age': {'$gt': 25}})

@mock.patch('collector.connectors.mongodb_connector.MongoClient')
def test_mongodb_connector_connection_failure(mock_mongo_client, mongodb_connector):
    """
    Test the MongoDBConnector handling of a connection failure.
    """
    # Simulate connection failure
    mock_mongo_client.side_effect = PyMongoError("Connection failed")
    
    # Expect an exception to be raised
    with pytest.raises(PyMongoError):
        mongodb_connector.connect()

@mock.patch('collector.connectors.mongodb_connector.MongoClient')
def test_mongodb_connector_fetch_data_failure(mock_mongo_client, mongodb_connector):
    """
    Test the MongoDBConnector fetch_data method handling a query failure.
    """
    # Mock database and collection
    mock_db = mock_mongo_client.return_value[config['database']]
    mock_collection = mock_db[config['collection']]
    
    # Simulate MongoDB find() raising an error
    mock_collection.find.side_effect = PyMongoError("Query failed")
    
    # Expect an exception to be raised
    with pytest.raises(PyMongoError):
        mongodb_connector.fetch_data()
