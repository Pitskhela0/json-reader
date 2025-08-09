import ijson

from collections.abc import Generator


class FileLoader:
    """Utility class for streaming JSON data from a file."""

    @staticmethod
    def load_file_data(path: str) -> Generator[dict, None, None]:
        """
        Stream JSON items from the given file one by one.

        Args:
            path: Path to the JSON file.
        Yields:
            dict: A JSON object parsed from the file.

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If access to the file is denied.
            ValueError: If the file contains invalid JSON.
            OSError: If an unexpected I/O error occurs.
        """
        try:
            with open(path, "r", encoding="utf-8") as file:
                try:
                    yield from ijson.items(file, "item")
                except ijson.JSONError as e:
                    raise ValueError(f"Invalid JSON format in file: {path}") from e
        except (FileNotFoundError, PermissionError):
            raise
        except OSError as e:
            raise OSError(f"Error reading file: {path}") from e
