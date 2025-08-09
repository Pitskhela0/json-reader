from collections.abc import Generator
from abc import ABC, abstractmethod
from typing import Dict, Any
import ijson


class FileLoader:
    """Utility class for streaming JSON data from a file."""

    @staticmethod
    def load_file_data(path: str, data_type: str) -> Generator[dict, None, None]:
        """
        Stream JSON items from the given file one by one.

        Args:
            path: Path to the JSON file.
            data_type: Type of data, for example: room, student etc.
        Yields:
            dict: A JSON object parsed from the file.

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If access to the file is denied.
            ValueError: If the file contains invalid JSON.
            OSError: If an unexpected I/O error occurs.
        """
        try:
            validation_context = ValidatorContext(data_type)
            with open(path, "r", encoding="utf-8") as file:
                try:
                    # yield from ijson.items(file, "item")
                    for i in ijson.items(file, "item"):
                        if validation_context.execute_validation(i):
                            yield i
                        else:
                            print(f"Unsuccessful validation: skipping {i}")
                except ijson.JSONError as e:
                    raise ValueError(f"Invalid JSON format in file: {path}") from e
        except (FileNotFoundError, PermissionError):
            raise
        except OSError as e:
            raise OSError(f"Error reading file: {path}") from e


class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, item: Dict[str, Any]) -> bool:
        pass


class RoomValidator(ValidationStrategy):
    def validate(self, item: dict) -> bool:
        try:
            if 'id' not in item or 'name' not in item:
                raise ValueError("Room data is incomplete")

            room_id, room_name = item['id'], item['name']

            if not isinstance(room_id, int) or room_id <= 0:
                raise ValueError(f"Room ID must be positive integer, got: {room_id}")

            if not isinstance(room_name, str) or not room_name.strip():
                raise ValueError(f"Room name must be non-empty string, got: {room_name}")

            return True
        except Exception as e:
            print(f"Room validation failed {e}")
            return False


class StudentValidator(ValidationStrategy):
    def validate(self, item: dict) -> bool:
        try:
            if 'id' not in item or 'name' not in item or 'room' not in item:
                raise ValueError("Student data is incomplete")

            student_id, student_name, room_id = item['id'], item['name'], item['room']

            if not isinstance(student_id, int) or student_id <= 0:
                raise ValueError(f"Student ID must be positive integer, got: {student_id}")

            if not isinstance(student_name, str) or not student_name.strip():
                raise ValueError(f"Student name must be non-empty string, got: {student_name}")

            if not isinstance(room_id, int) or room_id <= 0:
                raise ValueError(f"Room ID must be positive integer, got: {room_id}")

            return True

        except Exception as e:
            print(f"Student validation failed: {e}")
            return False


class ValidatorContext:
    _strategies = {
        'student': StudentValidator,
        'room': RoomValidator
    }

    def __init__(self, strategy_type: str):
        if strategy_type not in self._strategies:
            raise ValueError(f"{strategy_type} is unknown to the application")
        self.strategy = self._strategies[strategy_type]()

    def execute_validation(self, item: dict) -> bool:
        return self.strategy.validate(item)
