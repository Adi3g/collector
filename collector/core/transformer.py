class DataTransformer:
    """
    DataTransformer applies transformations to collected data according to rules defined in the configuration.

    :param transformations: A list of transformation rules from the configuration.
    :type transformations: list
    """

    def __init__(self, transformations):
        """
        Initializes the DataTransformer with the specified transformation rules.

        :param transformations: Transformation rules to apply.
        :type transformations: list
        """
        self.transformations = transformations

    def transform(self, data):
        """
        Applies transformation rules to the collected data.

        :param data: The raw data collected from sources.
        :type data: list of dict
        :return: Transformed data.
        :rtype: list of dict
        """
        transformed_data = []
        for item in data:
            transformed_item = self._apply_transformations(item)
            transformed_data.append(transformed_item)
        return transformed_data

    def _apply_transformations(self, item):
        """
        Applies transformation rules to a single data item.

        :param item: A dictionary representing a single data row.
        :type item: dict
        :return: Transformed data row.
        :rtype: dict
        """
        for transform in self.transformations:
            # Apply transformation rules based on the configuration
            # Example: type conversion, field renaming, default values
            # Placeholder logic:
            for rule in transform['rules']:
                field = rule.get('field')
                if field in item:
                    item[field] = self._convert_type(item[field], rule.get('type'))
                if 'rename' in rule:
                    item[rule['rename']] = item.pop(field)
                if 'default' in rule and item.get(field) is None:
                    item[field] = rule['default']
        return item

    def _convert_type(self, value, target_type):
        """
        Converts the value to the specified target type.

        :param value: The value to convert.
        :type value: Any
        :param target_type: The target type (e.g., 'string', 'int', 'float', 'date').
        :type target_type: str
        :return: The converted value.
        :rtype: Any
        """
        try:
            if target_type == 'int':
                return int(value)
            elif target_type == 'float':
                return float(value)
            elif target_type == 'string':
                return str(value)
            # Add more conversions as needed (e.g., date formatting)
        except (ValueError, TypeError):
            print(f"Warning: Failed to convert value {value} to {target_type}. Returning original value.")
        return value
