import re

class CollectorConfigParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = {
            'version': None,
            'sources': [],
            'transformations': [],
            'output': None
        }

    def parse(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        self._process_lines(lines)
        return self.config

    def _process_lines(self, lines):
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
        parts = re.split(r'\s+', line)
        return {
            'name': parts[1],
            'type': parts[3],
            'details': {}
        }

    def _parse_transform(self, line):
        parts = re.split(r'\s+', line)
        return {
            'target': parts[1],
            'source': parts[3],
            'rules': []
        }

    def _parse_output(self, line):
        parts = re.split(r'\s+', line)
        return {
            'type': parts[1],
            'details': {}
        }

    def _parse_nested(self, line, current_data):
        match = re.match(r'(\w+)\s+"([^"]+)"', line)
        if match:
            key, value = match.groups()
            current_data['details'][key.lower()] = value
