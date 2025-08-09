from .data_validator import ValidatorContext
from typing import Generator


class DataFilter:
    @staticmethod
    def filter_data(
            data: Generator[dict, None, None],
            data_type: str
    ) -> Generator[dict, None, None]:

        validation_context = ValidatorContext(data_type)
        for item in data:
            if validation_context.execute_validation(item):
                yield item
            else:
                print(f"Skipping {item}")
