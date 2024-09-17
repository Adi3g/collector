import re

class CollectorConfigParser:
    """
    Parses the configuration (.col) files for the Collector.

    :param file_path: Path to the configuration file.
    :type file_path: str
    """

    def __init__(self, file_path):
        """
        Initializes the CollectorConfigParser with the path to the .col file.

        :param file_path: The path to the .col configuration file.
        :type file_path: str
        """
        self.file_path = file_path
        self.config = {
            'version': None,
            'sources': [],
            'transformations': [],
            'output': None
        }

    def parse(self):
        """
        Parses the .col file and extracts configuration details.

        :return: Parsed configuration data including sources, transformations, and output settings.
        :rtype: dict
        :raises FileNotFoundError: If the .col file cannot be found.
        :raises ValueError: If the .col file is not formatted correctly.
        """
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        self._process_lines(lines)
        return self.config

    def _process_lines(self, lines):
        """
        Processes each line of the .col configuration file.

        :param lines: The lines of the configuration file.
        :type lines: list
        """
        current_section = None
        current_data = None
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Skip empty lines and comments

            if line.startswith('VERSION'):
                self.config['version'] = line.split()[1]
            elif line.startswith('SOURCE'):
                current_section = 'source'
                current_data = self._parse_source(line)
                self.config['sources'].append(current_data)
            elif line.startswith('TRANSFORM'):
                current_section = 'transform'
                current_data = self._parse_transform(line)
                self.config['transformations'].append(current_data)
            elif line.startswith('OUTPUT'):
                current_section = 'output'
                current_data = self._parse_output(line)
                self.config['output'] = current_data
            elif current_section and current_data:
                self._parse_nested(line, current_data)

    def _parse_source(self, line):
        """
        Parses a SOURCE section line.

        :param line: A line specifying a data source.
        :type line: str
        :return: A dictionary with source details.
        :rtype: dict
        """
        parts = re.split(r'\s+', line)
        return {
            'name': parts[1],
            'type': parts[3],
            'details': {}
        }

    def _parse_transform(self, line):
        """
        Parses a TRANSFORM section line.

        :param line: A line specifying a transformation.
        :type line: str
        :return: A dictionary with transformation details.
        :rtype: dict
        """
        parts = re.split(r'\s+', line)
        return {
            'target': parts[1],
            'source': parts[3],
            'rules': []
        }

    def _parse_output(self, line):
        """
        Parses an OUTPUT section line.

        :param line: A line specifying output settings.
        :type line: str
        :return: A dictionary with output details.
        :rtype: dict
        """
        parts = re.split(r'\s+', line)
        return {
            'type': parts[1],
            'details': {}
        }

    def _parse_nested(self, line, current_data):
        """
        Parses nested configuration details within a section.

        :param line: A line within a section detailing specific configuration options.
        :type line: str
        :param current_data: The current section data being processed.
        :type current_data: dict
        """
        match = re.match(r'(\w+)\s+"([^"]+)"', line)
        if match:
            key, value = match.groups()
            current_data['details'][key.lower()] = value
