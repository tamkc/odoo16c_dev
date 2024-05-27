import random
import string
from typing import List, Dict


class CsvStringGenerator:
    def __init__(self, field_configs: List[Dict[str, str]]):
        self.field_configs = field_configs
        self.csv_content: List[str] = []

    def _generate_random_value(self, config: Dict[str, str]) -> str:
        # Example random value generation logic based on field type
        field_type = config.get('type')
        if field_type == 'char':
            return 'text'
        elif field_type == 'integer':
            return str(random.randint(config.get('min', 0), config.get('max', 1000)))
        # Add more field types as necessary
        else:
            return " "

    def _generate_data(self, num_rows: int) -> List[List[str]]:
        field_configs = self.field_configs
        data = []
        for _ in range(num_rows):
            row = [self._generate_random_value(
                config) for config in field_configs]
            data.append(row)
        return data
