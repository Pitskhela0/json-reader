import unittest
import tempfile
import json
import os
from pathlib import Path
from unittest.mock import patch
from src.json_reader.services.cli_parser import CLIParser
from src.json_reader.services.data_validator import ValidatorContext
from src.json_reader.services.data_combiner import DataCombiner
from src.json_reader.exporters.exporter_factory import ExporterFactory
from src.json_reader.exporters.exporter import JSONExporter, XMLExporter


class TestDataValidator(unittest.TestCase):
    """Test data validation logic"""

    def test_valid_student(self):
        validator = ValidatorContext('student')
        valid_student = {"id": 1, "name": "Alice", "room": 101}
        self.assertTrue(validator.execute_validation(valid_student))

    def test_invalid_student_missing_keys(self):
        validator = ValidatorContext('student')
        invalid_student = {"id": 1, "name": "Alice"}  # Missing room
        self.assertFalse(validator.execute_validation(invalid_student))

    def test_invalid_student_wrong_types(self):
        validator = ValidatorContext('student')
        invalid_student = {"id": "1", "name": "", "room": -5}  # Wrong types
        self.assertFalse(validator.execute_validation(invalid_student))

    def test_valid_room(self):
        validator = ValidatorContext('room')
        valid_room = {"id": 101, "name": "Math Lab"}
        self.assertTrue(validator.execute_validation(valid_room))

    def test_invalid_room(self):
        validator = ValidatorContext('room')
        invalid_room = {"id": 0, "name": ""}  # Invalid values
        self.assertFalse(validator.execute_validation(invalid_room))


class TestDataCombiner(unittest.TestCase):
    """Test data combination logic"""

    def test_group_students_by_room(self):
        students = [
            {"id": 1, "name": "Alice", "room": 101},
            {"id": 2, "name": "Bob", "room": 101},
            {"id": 3, "name": "Charlie", "room": 102}
        ]
        result = DataCombiner.group_students_by_room_id(student for student in students)
        self.assertEqual(len(result[101]), 2)
        self.assertEqual(len(result[102]), 1)
        self.assertEqual(result[101][0]["name"], "Alice")

    def test_combine_students_with_rooms(self):
        students = [{"id": 1, "name": "Alice", "room": 101}]
        rooms = [{"id": 101, "name": "Math Lab"}, {"id": 102, "name": "Physics Lab"}]

        result = list(DataCombiner.combine_students_with_rooms(
            (student for student in students),
            (room for room in rooms)
        ))

        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0]["students"]), 1)  # Math Lab has Alice
        self.assertEqual(len(result[1]["students"]), 0)  # Physics Lab empty
        self.assertEqual(result[0]["students"][0]["name"], "Alice")


class TestExporterFactory(unittest.TestCase):
    """Test exporter factory functionality"""

    def test_create_json_exporter(self):
        exporter = ExporterFactory.create_exporter('json')
        self.assertIsInstance(exporter, JSONExporter)

    def test_create_xml_exporter(self):
        exporter = ExporterFactory.create_exporter('XML')  # case insensitive
        self.assertIsInstance(exporter, XMLExporter)

    def test_unsupported_format(self):
        with self.assertRaises(ValueError) as context:
            ExporterFactory.create_exporter('pdf')
        self.assertIn("Unsupported format", str(context.exception))

    def test_supported_formats(self):
        formats = ExporterFactory.get_supported_formats()
        self.assertIn('json', formats)
        self.assertIn('xml', formats)


class TestExporters(unittest.TestCase):
    """Test export functionality"""

    def setUp(self):
        self.test_data = [
            {"id": 101, "name": "Math Lab", "students": [{"id": 1, "name": "Alice"}]},
            {"id": 102, "name": "Physics Lab", "students": []}
        ]

    def test_json_export(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            exporter = JSONExporter()
            exporter.export_file((item for item in self.test_data), temp_path)

            with open(temp_path, 'r') as f:
                result = json.load(f)

            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["name"], "Math Lab")
            self.assertEqual(len(result[0]["students"]), 1)
        finally:
            os.unlink(temp_path)

    def test_xml_export(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            temp_path = f.name

        try:
            exporter = XMLExporter()
            exporter.export_file((item for item in self.test_data), temp_path)

            self.assertTrue(Path(temp_path).exists())

            with open(temp_path, 'r') as f:
                content = f.read()

            self.assertIn('<?xml version="1.0"', content)
            self.assertIn('<rooms>', content)
            self.assertIn('Math Lab', content)
        finally:
            os.unlink(temp_path)


class TestCLIParser(unittest.TestCase):
    """Test CLI parsing and validation"""

    def setUp(self):
        # Create temporary test files
        self.temp_dir = tempfile.mkdtemp()
        self.student_file = Path(self.temp_dir) / "students.json"
        self.room_file = Path(self.temp_dir) / "rooms.json"

        # Write test data
        with open(self.student_file, 'w') as f:
            json.dump([{"id": 1, "name": "Alice", "room": 101}], f)
        with open(self.room_file, 'w') as f:
            json.dump([{"id": 101, "name": "Math Lab"}], f)

    @patch('sys.argv')
    def test_valid_cli_args(self, mock_argv):
        mock_argv.__getitem__ = lambda _, index: [
            'main.py', '--student-file-path', str(self.student_file),
            '--room-file-path', str(self.room_file),
            '--output-format', 'json', '--output-destination', '/output'
        ][index]
        mock_argv.__len__ = lambda _: 7

        result = CLIParser.parse_cli()
        self.assertEqual(result[2], 'json')  # output_format
        self.assertEqual(result[3], '/output')  # output_destination

    def test_validate_output_path_creates_directory(self):
        output_path = Path(self.temp_dir) / "new_dir" / "output.json"
        CLIParser._validate_output_path(str(output_path))
        self.assertTrue(output_path.parent.exists())


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflow"""

    def test_end_to_end_json_export(self):
        """Test complete workflow from data to JSON export"""
        # Setup test data
        students_data = [
            {"id": 1, "name": "Alice", "room": 101},
            {"id": 2, "name": "Bob", "room": 102},
            {"id": 3, "name": "Charlie", "room": 101}
        ]
        rooms_data = [
            {"id": 101, "name": "Math Lab"},
            {"id": 102, "name": "Physics Lab"}
        ]

        # Combine data using generators
        combined = DataCombiner.combine_students_with_rooms(
            (student for student in students_data),
            (room for room in rooms_data)
        )

        # Export to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            exporter = ExporterFactory.create_exporter('json')
            exporter.export_file(combined, temp_path)

            # Verify export
            with open(temp_path, 'r') as f:
                result = json.load(f)

            self.assertEqual(len(result), 2)
            # Math Lab should have Alice and Charlie
            math_lab = next(room for room in result if room["name"] == "Math Lab")
            self.assertEqual(len(math_lab["students"]), 2)

            # Physics Lab should have Bob
            physics_lab = next(room for room in result if room["name"] == "Physics Lab")
            self.assertEqual(len(physics_lab["students"]), 1)
            self.assertEqual(physics_lab["students"][0]["name"], "Bob")

        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
