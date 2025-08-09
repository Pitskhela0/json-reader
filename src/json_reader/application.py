import logging

from .exporters.exporter_factory import ExporterFactory
from .services.cli_parser import CLIParser
from .services.data_combiner import DataCombiner
from .services.data_filter import DataFilter
from .services.file_loader import FileLoader

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def start_application() -> None:
    """
    Run the main application workflow:
    1. Parse CLI arguments.
    2. Load input data from files.
    3. Combine students with rooms.
    4. Export the result in the specified format.
    """
    try:
        student_file, room_file, output_format, output_destination = (
            CLIParser.parse_cli()
        )
        logger.info(student_file, room_file, output_format, output_destination)

        rooms = DataFilter.filter_data(FileLoader.load_file_data(room_file), "room")

        students = DataFilter.filter_data(
            FileLoader.load_file_data(student_file), "student"
        )

        combined_data = DataCombiner.combine_students_with_rooms(students, rooms)

        exporter = ExporterFactory.create_exporter(output_format)
        exporter.export_file(combined_data, output_destination)
    except Exception as e:
        logger.error(f"Application failed: {e}")
        raise
