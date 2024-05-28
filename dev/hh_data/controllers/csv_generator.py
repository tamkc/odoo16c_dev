import random
import string
from typing import List, Dict
import re
from faker import Faker
fake = Faker()


class CsvStringGenerator:
    def __init__(self, field_configs: List[Dict[str, str]]):
        self.field_configs = field_configs
        self.csv_content: List[str] = []

    def _generate_data(self, num_rows: int) -> List[List[str]]:
        field_configs = self.field_configs
        data = []
        for _ in range(num_rows):
            row = [self._generate_random_value(
                config) for config in field_configs]
            data.append(row)
        return data

    def _generate_random_value(self, config: Dict[str, str]) -> str:

        def handle_char():
            return fake.name()

        def handle_integer():
            return str(random.randint(config.get('min', 0), config.get('max', 1000)))

        def handle_selection():
            selection_list = re.findall(r"\((.*?)\)", config.get('value'))
            selection_list = [tuple(eval(x) for x in t.split(","))
                              for t in selection_list]
            random_value = random.choice(selection_list)
            return str(random_value[0])

        def handle_float():
            min_value = config.get('min', 0)
            max_value = config.get('max', 1000)
            decimals = config.get('decimals', 2)
            if min_value is None or max_value is None or decimals is None:
                raise ValueError("min, max, and decimals must not be None")
            return str(round(random.uniform(min_value, max_value), decimals))

        def handle_date():
            date_from = config.get('date_from')
            date_to = config.get('date_to')
            if date_from is None or date_to is None:
                raise ValueError("date_from and date_to must not be None")
            return str(fake.date_between(start_date=date_from, end_date=date_to))

        def handle_datetime():
            date_from = config.get('date_from')
            date_to = config.get('date_to')
            if date_from is None or date_to is None:
                raise ValueError("date_from and date_to must not be None")
            return str(fake.date_time_between(start_date=date_from, end_date=date_to))

        def handle_boolean():
            return str(random.choice([True, False]))

        def handle_text():
            return fake.text()

        def handle_many2one():
            return str(random.choice(config.get('value')))

        def handle_default():
            return " "

        type_handlers = {
            'char': handle_char,
            'integer': handle_integer,
            'selection': handle_selection,
            'float': handle_float,
            'date': handle_date,
            'datetime': handle_datetime,
            'boolean': handle_boolean,
            'text': handle_text,
            'many2one': handle_many2one,
        }

        handler = type_handlers.get(config.get('type'), handle_default)
        return handler()
