import logging
from abc import ABC, abstractmethod
from typing import Any, Dict
from ..constants.errors_messages import ErrorMessages
from ..constants.data_item_constants import ItemConstants

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class ValidationStrategy(ABC):
    """Base class for all validators.
    Each validator checks different types of data."""

    @abstractmethod
    def validate(self, item: Dict[str, Any]) -> bool:
        """Check if a data item is valid. Return True if good, False if bad."""
        pass


class RoomValidator(ValidationStrategy):
    """Checks if room data is correct and complete."""

    def validate(self, item: dict) -> bool:
        """
        Makes sure a room has valid ID and name.

        A valid room must have:
        - An 'id' that's a positive number
        - A 'name' that's not empty
        """
        try:
            if ItemConstants.ID_FIELD not in item or ItemConstants.NAME_FIELD not in item:
                raise ValueError(ErrorMessages.ROOM_INCOMPLETE_DATA)

            room_id, room_name = item[ItemConstants.ID_FIELD], item[ItemConstants.NAME_FIELD]

            if not isinstance(room_id, int) or room_id < ItemConstants.MIN_ROOM_ID:
                raise ValueError(ErrorMessages.ROOM_INVALID_ID.format(room_id))

            if not isinstance(room_name, str) or not room_name.strip():
                raise ValueError(ErrorMessages.ROOM_INVALID_NAME.format(room_name))

            return True
        except Exception as e:
            logger.error(ErrorMessages.ROOM_VALIDATION_FAILED.format(e))
            return False


class StudentValidator(ValidationStrategy):
    """Checks if student data is correct and complete."""

    def validate(self, item: dict) -> bool:
        """
        Makes sure a student has valid ID, name, and room assignment.

        A valid student must have:
        - An 'id' that's a positive number
        - A 'name' that's not empty
        - A 'room' that's a positive number
        """
        try:
            if ItemConstants.ID_FIELD not in item or ItemConstants.NAME_FIELD not in item or ItemConstants.ROOM_FIELD not in item:
                raise ValueError(ErrorMessages.STUDENT_INCOMPLETE_DATA)

            student_id, student_name, room_id = (item[ItemConstants.ID_FIELD], item[ItemConstants.NAME_FIELD], item[ItemConstants.ROOM_FIELD])

            if not isinstance(student_id, int) or student_id < ItemConstants.MIN_STUDENT_ID:
                raise ValueError(ErrorMessages.STUDENT_INVALID_ID.format(student_id))

            if not isinstance(student_name, str) or not student_name.strip():
                raise ValueError(ErrorMessages.STUDENT_INVALID_NAME.format(student_name))

            if not isinstance(room_id, int) or room_id < ItemConstants.MIN_ROOM_ID:
                raise ValueError(ErrorMessages.STUDENT_INVALID_ROOM_ID.format(room_id))

            return True

        except Exception as e:
            logger.error(ErrorMessages.STUDENT_VALIDATION_FAILED.format(e))
            return False


class ValidatorContext:
    """Picks the right validator for the type of data you're checking."""

    _strategies = {ItemConstants.STUDENT_STRATEGY: StudentValidator, ItemConstants.ROOM_STRATEGY: RoomValidator}

    def __init__(self, strategy_type: str):
        """
        Set up the validator for a specific data type.

        Args:
            strategy_type: Either 'student' or 'room'
        """
        if strategy_type not in self._strategies:
            raise ValueError(ErrorMessages.UNKNOWN_VALIDATION_STRATEGY.format(strategy_type))
        self.strategy = self._strategies[strategy_type]()

    def execute_validation(self, item: dict) -> bool:
        """Check if the item is valid using the right validator."""
        return self.strategy.validate(item)
