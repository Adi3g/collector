# tests/test_collector.py


from collector.core.collector import Collector


def test_collector_initialization():
    collector = Collector(config_path='path/to/config.col')
    assert collector.config_path == 'path/to/config.col'
