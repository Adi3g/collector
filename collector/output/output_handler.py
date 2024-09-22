from decimal import Decimal
from xml.dom import minidom
import pandas as pd
import json
from datetime import date
import xml.etree.ElementTree as ET

class OutputHandler:
    """
    Handles outputting the transformed data to different formats (CSV, JSON, Parquet).
    """

    def __init__(self, output_config):
        """
        Initializes the OutputHandler with the output configuration.

        :param output_config: The configuration specifying output format and path.
        :type output_config: dict
        """
        self.output_type = output_config['type']
        details = output_config.get('details', {})
        self.output_path = details.get('path', None)
        self.options = details.get('options', {})

    def write_output(self, data):
        """
        Writes the data to the specified format (CSV, JSON, Parquet).
        
        :param data: The data to be written.
        :type data: list of dict
        """
        if self.output_type == 'csv':
            self._write_csv(data)
        elif self.output_type == 'json':
            self._write_json(data)
        elif self.output_type == 'xml':
            self._write_xml(data)
        elif self.output_type == 'parquet':
            self._write_parquet(data)
        else:
            raise ValueError(f"Unsupported output type: {self.output_type}")

    def _write_csv(self, data):
        """
        Outputs data to a CSV file.

        :param data: The data to output.
        :type data: list of dict
        """
        df = pd.DataFrame(data)  # Convert data to DataFrame
        df.to_csv(self.output_path, index=False)

    def _write_xml(self, data):
        """
        Outputs data to an XML file with pretty printing.

        :param data: The data to output.
        :type data: list of dict
        """
        root = ET.Element("data")

        # Convert each dictionary entry into an XML element
        for row in data:
            item = ET.SubElement(root, "item")
            for key, value in row.items():
                child = ET.SubElement(item, key)
                child.text = str(value)  # Ensure everything is a string

        # Convert the ElementTree to a string and apply pretty printing
        rough_string = ET.tostring(root, encoding="utf-8")
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="    ")  # Add indentation of 4 spaces

        # Write the pretty-printed XML to a file
        with open(self.output_path, "w") as xml_file:
            xml_file.write(pretty_xml)

    @staticmethod
    def _json_serial(obj):
        """
        Custom serializer for objects not serializable by default.
        
        :param obj: The object to serialize.
        :return: A serializable format (e.g., string) of the object.
        :raises TypeError: If the object is not serializable.
        """
        if isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal objects to float
        if isinstance(obj, date):
            return obj.isoformat()  # Convert date objects to ISO format (YYYY-MM-DD)
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def _write_json(self, data):
        """
        Outputs data to a JSON file.

        :param data: The data to output.
        :type data: list of dict
        """
        with open(self.output_path, 'w') as json_file:
            json.dump(data, json_file, indent=4, default=self._json_serial)  # Use custom serialization method

    def _write_parquet(self, data):
        """
        Outputs data to a Parquet file with optional compression.

        :param data: The data to output.
        :type data: list of dict
        """
        df = pd.DataFrame(data)  # Convert data to DataFrame
        compression = self.options.get('compression', None)  # Get compression option, if specified
        df.to_parquet(self.output_path, compression=compression)
