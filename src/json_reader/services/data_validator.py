import logging

from abc import ABC, abstractmethod
from typing import Dict, Any

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class ValidationStrategy(ABC):
    """Base class for all validators. Each validator checks different types of data."""

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
            if "id" not in item or "name" not in item:
                raise ValueError("Room data is incomplete")

            room_id, room_name = item["id"], item["name"]

            if not isinstance(room_id, int) or room_id < 0:
                raise ValueError(f"Room ID must be positive integer, got: {room_id}")

            if not isinstance(room_name, str) or not room_name.strip():
                raise ValueError(
                    f"Room name must be non-empty string, got: {room_name}"
                )

            return True
        except Exception as e:
            logger.error(f"Room validation failed {e}")
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
            if "id" not in item or "name" not in item or "room" not in item:
                raise ValueError("Student data is incomplete")

            student_id, student_name, room_id = item["id"], item["name"], item["room"]

            if not isinstance(student_id, int) or student_id < 0:
                raise ValueError(
                    f"Student ID must be positive integer, got: {student_id}"
                )

            if not isinstance(student_name, str) or not student_name.strip():
                raise ValueError(
                    f"Student name must be non-empty string, got: {student_name}"
                )

            if not isinstance(room_id, int) or room_id < 0:
                raise ValueError(f"Room ID must be positive integer, got: {room_id}")

            return True

        except Exception as e:
            logger.error(f"Student validation failed: {e}")
            return False


class ValidatorContext:
    """Picks the right validator for the type of data you're checking."""

    _strategies = {"student": StudentValidator, "room": RoomValidator}

    def __init__(self, strategy_type: str):
        """
        Set up the validator for a specific data type.

        Args:
            strategy_type: Either 'student' or 'room'
        """
        if strategy_type not in self._strategies:
            raise ValueError(f"{strategy_type} is unknown to the application")
        self.strategy = self._strategies[strategy_type]()

    def execute_validation(self, item: dict) -> bool:
        """Check if the item is valid using the right validator."""
        return self.strategy.validate(item)
