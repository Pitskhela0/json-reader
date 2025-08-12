class ErrorMessages:
    """ Error messages for application"""

    APPLICATION_FAILED = "Application failed: {}"

    INVALID_JSON_FORMAT = "Invalid JSON format in file: {}"
    FILE_READ_ERROR = "Error reading file: {}"

    ROOM_INCOMPLETE_DATA = "Room data is incomplete"
    ROOM_INVALID_ID = "Room ID must be positive integer, got: {}"
    ROOM_INVALID_NAME = "Room name must be non-empty string, got: {}"
    ROOM_VALIDATION_FAILED = "Room validation failed: {}"

    STUDENT_INCOMPLETE_DATA = "Student data is incomplete"
    STUDENT_INVALID_ID = "Student ID must be positive integer, got: {}"
    STUDENT_INVALID_NAME = "Student name must be non-empty string, got: {}"
    STUDENT_INVALID_ROOM_ID = "Room ID must be positive integer, got: {}"
    STUDENT_VALIDATION_FAILED = "Student validation failed: {}"

    UNKNOWN_VALIDATION_STRATEGY = "Unknown validation strategy: {}"

    STUDENT_MISSING_KEY = "Student record missing required key: {}"
    ROOM_MISSING_KEY = "Room record missing required key: {}"

    NO_WRITE_PERMISSION_DIR = "No write permission for output directory: {}"
    CANNOT_CREATE_OUTPUT_DIR = "Cannot create output directory {}: {}"
    NO_WRITE_PERMISSION_FILE = "No write permission for file: {}"
    INVALID_FILE_EXTENSION = "Custom output path must end with .json or .xml, got: {}"
    FORMAT_MISMATCH_XML_JSON = "Output format is XML but destination has .json extension"
    FORMAT_MISMATCH_JSON_XML = "Output format is JSON but destination has .xml extension"
    INVALID_OUTPUT_PATH = "Invalid output path"

    UNSUPPORTED_FORMAT = "Unsupported format: {}"
