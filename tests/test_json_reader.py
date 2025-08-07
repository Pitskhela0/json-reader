
from src.json_reader.cli_parser import CLIParser
from src.json_reader.services.file_loader import FileLoader
from src.json_reader.services.data_combiner import DataCombiner
import unittest
import tempfile
import json
import os
from unittest.mock import patch


class TestCLIParser(unittest.TestCase):
    @patch('sys.argv', ['script.py', '--student-file-path', 'students.json',
                        '--room-file-path', 'rooms.json', '--output-format', 'json'])
    def test_parse_basic_args(self):
        student_path, room_path, format_type, destination = CLIParser.parse_cli()
        self.assertEqual(student_path, 'students.json')
        self.assertEqual(room_path, 'rooms.json')
        self.assertEqual(format_type, 'json')
        self.assertEqual(destination, '/output')


class TestFileLoader(unittest.TestCase):
    def test_load_file_data(self):
        # Create temporary JSON file
        test_data = [{"id": 1, "name": "Test"}, {"id": 2, "name": "Test2"}]

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(test_data, f)
            temp_file = f.name

        try:
            # Test loading
            generator = FileLoader.load_file_data(temp_file)
            loaded_data = list(generator)

            self.assertEqual(len(loaded_data), 2)
            self.assertEqual(loaded_data[0]['id'], 1)
            self.assertEqual(loaded_data[1]['name'], 'Test2')
        finally:
            os.unlink(temp_file)


class TestDataCombiner(unittest.TestCase):
    def test_group_students_by_roomID(self):
        students = [
            {"id": 1, "name": "John", "room": 101},
            {"id": 2, "name": "Jane", "room": 101},
            {"id": 3, "name": "Bob", "room": 102}
        ]

        def student_generator():
            for student in students:
                yield student

        grouped = DataCombiner.group_students_by_roomID(student_generator())

        self.assertEqual(len(grouped[101]), 2)
        self.assertEqual(len(grouped[102]), 1)
        self.assertEqual(grouped[101][0]['name'], 'John')

    def test_combine_students_with_rooms(self):
        students = [
            {"id": 1, "name": "John", "room": 101},
            {"id": 2, "name": "Jane", "room": 102}
        ]

        rooms = [
            {"id": 101, "name": "Room A"},
            {"id": 102, "name": "Room B"},
            {"id": 103, "name": "Room C"}
        ]

        def student_gen():
            for s in students:
                yield s

        def room_gen():
            for r in rooms:
                yield r

        combined = list(DataCombiner.combine_students_with_rooms(student_gen(), room_gen()))

        self.assertEqual(len(combined), 3)  # 3 rooms

        # Room 101 should have John
        room_101 = next(r for r in combined if r['id'] == 101)
        self.assertEqual(len(room_101['students']), 1)
        self.assertEqual(room_101['students'][0]['name'], 'John')

        # Room 103 should be empty
        room_103 = next(r for r in combined if r['id'] == 103)
        self.assertEqual(len(room_103['students']), 0)


class TestIntegration(unittest.TestCase):
    def test_full_workflow(self):
        # Create test files
        students = [{"id": 1, "name": "Alice", "room": 1}]
        rooms = [{"id": 1, "name": "Room 1"}, {"id": 2, "name": "Room 2"}]

        # Create temp files
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as sf:
            json.dump(students, sf)
            students_file = sf.name

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as rf:
            json.dump(rooms, rf)
            rooms_file = rf.name

        try:
            # Test full workflow
            students_gen = FileLoader.load_file_data(students_file)
            rooms_gen = FileLoader.load_file_data(rooms_file)
            combined = list(DataCombiner.combine_students_with_rooms(students_gen, rooms_gen))

            # Verify results
            self.assertEqual(len(combined), 2)
            self.assertEqual(combined[0]['students'][0]['name'], 'Alice')
            self.assertEqual(len(combined[1]['students']), 0)
        finally:
            os.unlink(students_file)
            os.unlink(rooms_file)


if __name__ == '__main__':
    unittest.main(verbosity=2)