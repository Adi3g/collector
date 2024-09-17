
from collector.connectors.sql_connector import SQLConnector

def test_sql_connector():
    config = {
        'host': 'localhost',
        'port': 5432,
        'username': 'user',
        'password': 'pass',
        'database': 'test_db'
    }
    connector = SQLConnector(config)
    connector.connect()
    data = connector.fetch_data("SELECT * FROM test_table")  # Update query as per your test DB
    assert data is not None
