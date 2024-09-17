# tests/test_config_parser.py

from collector.core.config_parser import CollectorConfigParser

def test_config_parser():
    parser = CollectorConfigParser('examples/basic_example.col')
    config = parser.parse()
    assert config['version'] == '1.0'
    assert len(config['sources']) > 0
    assert config['output'] is not None
