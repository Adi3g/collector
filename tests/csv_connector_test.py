from unittest import mock
from collector.connectors.csv_connector import CSVConnector

@mock.patch('builtins.open', new_callable=mock.mock_open, read_data="id,name\n1,Test\n2,Example")
def test_csv_connector(mock_open):
    config = {
        'file_path': 'test.csv',
        'delimiter': ','
    }
    connector = CSVConnector(config)
    data = connector.fetch_data()

    # Assert the data read from the file (with integers for 'id')
    assert data == [{'id': 1, 'name': 'Test'}, {'id': 2, 'name': 'Example'}]
