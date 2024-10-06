# Collector

Collector is a Python library designed to collect data from various sources such as databases, big data files, cloud storage, APIs, and more, and transform the data into a unified output structure. This flexible and extensible tool allows you to define data collection and transformation rules using a custom configuration file format (`.col`), making data integration tasks streamlined and maintainable.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Configuration File (.col)](#configuration-file-col)
- [Connectors](#connectors)
- [Transformations](#transformations)
- [Output Formats](#output-formats)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Multiple Data Sources**: Supports SQL databases, cloud storage (AWS S3, Google Cloud Storage, Azure Blob), CSV files, APIs, JSON, Parquet, and more.
- **Flexible Transformation Rules**: Apply type conversions, renaming, formatting, and custom transformations.
- **Unified Output**: Output data in various formats such as CSV, JSON, and Parquet with custom options.
- **Modular Configuration**: Use `.col` files to define data sources, transformations, and outputs, with support for imports to reuse configurations.
- **Data Collection Modes**: Choose between **parallel** and **sequential** data collection modes for improved performance.
- **Extensible Architecture**: Easily add new connectors and transformations to expand functionality.

## Getting Started

Follow these steps to get started with Collector:

1. **Install Dependencies**: Install required dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

2. **Define a Configuration File (.col)**: Create a `.col` file that specifies your data sources, transformation rules, and output configuration.

3. **Run the Collector**: Use the provided script to run the collector with your configuration file:
   ```bash
   python scripts/run_collector.py <your_col_file.col>
   ```

## Configuration File (.col)

The `.col` file is the heart of Collector, allowing you to define how data should be collected, transformed, and output. Below is a basic example of a `.col` file:

```plaintext
VERSION 1.0

# Optional: Set Collection Mode (default is 'sequence')
COLLECT_MODE parallel  # Can be 'parallel' or 'sequence'

# Define Data Sources
SOURCE sales_db TYPE sql {
    HOST "localhost"
    PORT 5432
    USERNAME "user"
    PASSWORD "pass"
    DATABASE "sales"
    QUERY "SELECT * FROM sales_data"
}

# Define Transformations
TRANSFORM unified_sales FROM sales_db {
    FIELD sale_date TYPE date FORMAT "%Y-%m-%d"
    FIELD amount TYPE float DEFAULT 0.0
}

# Define Output
OUTPUT unified_data TYPE parquet {
    PATH "/output/unified_sales.parquet"
    OPTIONS {
        COMPRESSION "gzip"
    }
}

```

### Collect Mode

- **`parallel`**: Data from all sources is collected concurrently, speeding up the process for large datasets or slower APIs.
- **`sequence`** (default): Data is collected sequentially, one source at a time.

## Connectors

Collector includes connectors for various data sources:

- **SQL Connector**: Connect to SQL databases like MySQL, PostgreSQL, etc.
- **CSV Connector**: Read data from CSV files with customizable options.
- **API Connector**: Fetch data from RESTful APIs using GET, POST, and other methods.
- **Parquet Connector**: Read data from Parquet files with compression options.
- **MongoDB Connector**: Fetch data from MongoDB collections.
- **Cloud Storage Connectors**:
  - **AWS S3**: Fetch data from Amazon S3 buckets.
  - **Google Cloud Storage**: Fetch data from Google Cloud Storage buckets.
  - **Azure Blob Storage**: Fetch data from Azure Blob containers.

## Transformations

Define transformation rules in your `.col` file to:

- Convert data types (e.g., string to date, int to float).
- Rename fields.
- Apply conditional transformations.
- Set default values.

### Example Transformation

```plaintext
TRANSFORM unified_sales FROM sales_db {
    FIELD sale_date TYPE date FORMAT "%Y-%m-%d"
    FIELD amount TYPE float DEFAULT 0.0
}
```

## Output Formats

Collector supports various output formats:

- **CSV**: Output data to CSV files with customizable delimiters and headers.
- **JSON**: Save data as JSON with options for pretty printing.
- **Parquet**: Export data to Parquet files with optional compression.

## Examples

Check out the `examples/` directory for sample `.col` files demonstrating different configurations:

- `basic_example.col`: A simple example using SQL and CSV sources.
- `advanced_example.col`: An advanced configuration with multiple data sources and transformations.
- `parallel_example.col`: Demonstrates parallel data collection from multiple sources.
- `shared_sources.col`: Demonstrates importing shared data sources across configurations.

## Contributing

We welcome contributions to improve Collector! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push to your fork.
4. Open a pull request with a detailed description of your changes.

Please ensure that your code follows the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
