from typing import Generator

import ijson


class FileLoader:
    @staticmethod
    def load_file_data(path: str) -> Generator[dict, None, None]:
        with open(path, 'r') as file:
            for item in ijson.items(file, 'item'):
                yield item
