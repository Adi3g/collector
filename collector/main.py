from collector.core.collector import Collector

def main():
    config_path = 'examples/basic_example.col'  # Path to the sample .col file
    collector = Collector(config_path)
    collector.run()

if __name__ == "__main__":
    main()
