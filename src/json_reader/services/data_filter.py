import logging

from .data_validator import ValidatorContext
from typing import Generator

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class DataFilter:
    """Filters data by validating each item and keeping only the valid ones."""

    @staticmethod
    def filter_data(
        data: Generator[dict, None, None], data_type: str
    ) -> Generator[dict, None, None]:
        """
        Takes data items one by one and only returns the valid ones.

        Args:
            data: Stream of data items to check
            data_type: What kind of data we're checking ('student' or 'room')

        Returns:
            Only the valid data items
        """
        validation_context = ValidatorContext(data_type)
        for item in data:
            if validation_context.execute_validation(item):
                yield item
            else:
                logger.warning(f"skipping {item}")
