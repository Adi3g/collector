import argparse
from collector.core.collector import Collector  # Assuming Collector is correctly implemented

def main():
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Run the Collector with a specified .col configuration file")
    
    # Add the argument for the path to the .col file
    parser.add_argument("config_path", help="Path to the .col configuration file")
    
    # Parse the command-line arguments
    args = parser.parse_args()

    # Initialize and run the collector with the provided config path
    collector = Collector(args.config_path)
    collector.run()

if __name__ == "__main__":
    main()
