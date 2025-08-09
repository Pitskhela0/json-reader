# JSON Reader
This Python module provides data processing and export functionality for student and room management systems.

---

## Overview
This script helps you process student and room data from JSON files. 

## Features
- Parse and validate student and room JSON data
- Combine students with their assigned rooms
- Export data to multiple formats (JSON, XML)
- Command-line interface for batch processing
- Comprehensive data validation with type checking
- Flexible exporter factory pattern
- Generator pattern
- Strategy pattern for validation

## Installation
```
git clone https://github.com/Pitskhela0/json-reader.git
cd json-reader
uv sync
```

## Examples and Operations

### Supported Operations
- Data validation for students and rooms
- Grouping students by room assignments
- Combining student and room data
- Exporting to JSON and XML formats
- CLI-based batch processing

### Basic Usage Example
```python
from src.json_reader.services.data_validator import ValidatorContext
from src.json_reader.services.data_combiner import DataCombiner
from src.json_reader.exporters.exporter_factory import ExporterFactory

# validate student data
validator = ValidatorContext('student')
student = {"id": 1, "name": "Alice", "room": 101}
is_valid = validator.execute_validation(student)

# combine students with rooms
students_data = [
    {"id": 1, "name": "Alice", "room": 101},
    {"id": 2, "name": "Bob", "room": 102}
]
rooms_data = [
    {"id": 101, "name": "Math Lab"},
    {"id": 102, "name": "Physics Lab"}
]

combined = DataCombiner.combine_students_with_rooms(
    (student for student in students_data),
    (room for room in rooms_data)
)

# export to JSON
exporter = ExporterFactory.create_exporter('json')
exporter.export_file(combined, 'output.json')
```

### Data Validation Example
```python
valid_student = {
    "id": 1,          
    "name": "Alice",   
    "room": 101       
}

valid_room = {
    "id": 101,        
    "name": "Math Lab" 
}

validator_student = ValidatorContext('student')
validator_room = ValidatorContext('room')

assert validator_student.execute_validation(valid_student)
assert validator_room.execute_validation(valid_room)
```

### CLI Usage Example
```bash
python main.py \
    --student-file-path students.json \
    --room-file-path rooms.json \
    --output-format json \
    --output-destination ./output/combined_data.json
```

## Testing
```bash
uv run pytest
```

## Supported Export Formats
- **JSON** - Standard JSON format for easy integration
- **XML** - Structured XML with proper formatting
