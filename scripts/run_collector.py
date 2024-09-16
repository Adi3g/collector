
from collector.core.collector import Collector

def main():
    config_path = 'path/to/config.col'  # Update with an actual path to your .col file
    collector = Collector(config_path)
    collector.run()

if __name__ == "__main__":
    main()
