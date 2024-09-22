import re

class ColValidator:
    """
    Validator class for validating .col configuration files.
    """

    def __init__(self, config):
        """
        Initializes the validator with the parsed configuration.

        :param config: Parsed configuration dictionary.
        :type config: dict
        """
        self.config = config
        self.errors = []

    def validate(self):
        """
        Validates the .col configuration file.

        :return: Boolean indicating whether the validation passed or failed.
        :rtype: bool
        """
        self.validate_version()
        self.validate_sources()
        self.validate_transformations()
        self.validate_output()

        if self.errors:
            for error in self.errors:
                print(f"Validation Error: {error}")
            return False
        return True

    def validate_version(self):
        """
        Validates the version section of the configuration.
        """
        if 'version' not in self.config:
            self.errors.append("Missing 'VERSION' section.")
        elif not re.match(r'^\d+\.\d+$', self.config['version']):
            self.errors.append(f"Invalid version format: {self.config['version']}. Expected format 'X.X'.")

    def validate_sources(self):
        """
        Validates the sources section of the configuration.
        """
        if 'sources' not in self.config:
            self.errors.append("Missing 'SOURCE' section.")
        else:
            for source in self.config['sources']:
                if 'type' not in source:
                    self.errors.append("Each SOURCE must have a 'type' field.")
                elif source['type'] not in ['sql', 'csv', 'api', 'parquet']:
                    self.errors.append(f"Invalid source type: {source['type']}. Must be one of ['sql', 'csv', 'api', 'parquet'].")
                
                if source['type'] == 'sql':
                    self.validate_sql_source(source)

    def validate_sql_source(self, source):
        """
        Validates the SQL source configuration.
        """
        required_fields = ['host', 'port', 'username', 'password', 'database', 'query']
        for field in required_fields:
            if field not in source['details']:
                self.errors.append(f"SQL source missing required field: {field}.")

    def validate_transformations(self):
        """
        Validates the transformations section of the configuration.
        """
        if 'transformations' not in self.config:
            self.errors.append("Missing 'TRANSFORM' section.")
        else:
            for transform in self.config['transformations']:
                if 'source' not in transform:
                    self.errors.append(f"Transformation missing 'source' field.")
                if 'rules' not in transform:
                    self.errors.append(f"Transformation missing 'rules' field.")
                if not isinstance(transform['rules'], list):
                    self.errors.append(f"'rules' in transformation must be a list.")

    def validate_output(self):
        """
        Validates the output section of the configuration.
        """
        if 'output' not in self.config:
            self.errors.append("Missing 'OUTPUT' section.")
        else:
            output = self.config['output']
            if 'type' not in output:
                self.errors.append("Output must have a 'type' field.")
            elif output['type'] not in ['csv', 'xml', 'json', 'parquet']:
                self.errors.append(f"Invalid output type: {output['type']}. Must be one of ['csv', 'json', 'parquet'].")
            if 'details' not in output or 'path' not in output['details']:
                self.errors.append("Output must have a 'path' in 'details'.")
