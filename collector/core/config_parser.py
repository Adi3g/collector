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
        current_line_idx = 0
        
        while current_line_idx < len(lines):
            line = lines[current_line_idx].strip()
            if not line or line.startswith('#'):
                current_line_idx += 1
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
                current_data['section'] = 'output'
                self.config['output'] = current_data
            elif current_section and current_data:
                current_line_idx = self._parse_nested(line, current_data, lines, current_line_idx)

            current_line_idx += 1

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
            'name': parts[1],
            'type': parts[3],
            'details': {}
        }

    def _parse_output_details(self, output, line, lines, current_line_idx):
        """
        Parses the details inside an OUTPUT block and stores them inside the 'details' key.

        :param output: The current output dictionary being processed.
        :type output: dict
        :param line: The line from the configuration file to parse.
        :type line: str
        :param lines: All lines of the configuration file.
        :type lines: list of str
        :param current_line_idx: Current index in the lines to track the nested block.
        :type current_line_idx: int
        :return: Updated line index after processing.
        :rtype: int
        """
        # Ensure 'details' is initialized
        if 'details' not in output:
            output['details'] = {}

        if line.startswith('PATH'):
            key, value = line.split(" ", 1)
            output['details']['path'] = value.strip('"')  # Store in 'details'
        elif line.startswith('OPTIONS'):
            output['details']['options'] = {}  # Initialize the options dict inside 'details'
            current_line_idx += 1

            # Continue parsing nested fields inside the OPTIONS block
            while not lines[current_line_idx].strip().startswith('}'):
                option_line = lines[current_line_idx].strip()
                if option_line:
                    key, value = option_line.split(" ", 1)
                    output['details']['options'][key.lower()] = value.strip('"')
                current_line_idx += 1

        return current_line_idx



    def _parse_nested(self, line, current_data, lines, current_line_idx):
        """
        Parses nested configuration details within a section.

        :param line: A line within a section detailing specific configuration options.
        :type line: str
        :param current_data: The current section data being processed.
        :type current_data: dict
        :param lines: All lines of the configuration file.
        :type lines: list of str
        :param current_line_idx: Current index in the lines to track the nested block.
        :type current_line_idx: int
        :return: Updated line index after processing.
        :rtype: int
        """
        if 'section' in current_data and current_data['section'] == 'output':
            # Delegate to the output-specific handler
            return self._parse_output_details(current_data, line, lines, current_line_idx)
        else:
            # General handling for nested lines in other sections
            match = re.match(r'(\w+)\s+("[^"]+"|\S+)', line)
            if match:
                key, value = match.groups()
                value = value.strip('"')
                if value.isdigit():
                    value = int(value)
                if 'details' not in current_data:
                    current_data['details'] = {}
                current_data['details'][key.lower()] = value
        return current_line_idx
