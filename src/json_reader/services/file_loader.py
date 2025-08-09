from typing import Generator
import ijson


class FileLoader:
    @staticmethod
    def load_file_data(path: str) -> Generator[dict, None, None]:
        """
        Load items from file one by one.
        :param path: Path to JSON file
        :yields: dict: JSON item
        """
        try:
            with open(path, 'r') as file:
                try:
                    for item in ijson.items(file, 'item'):
                        yield item
                except ijson.JSONError as e:
                    raise ValueError(f"Invalid JSON format in file: {path}") from e
        except (FileNotFoundError, PermissionError):
            raise
        except OSError as e:
            raise OSError(f"Error reading file: {path}") from e
