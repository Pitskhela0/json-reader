from .cli_parser import CLIParser
from .services.file_loader import FileLoader
from .services.data_combiner import DataCombiner
from .exporters.exporter import Exporter


def start_application() -> None:
    # parse cli commands
    student_file_path, room_file_path, output_format, output_destination = CLIParser.parse_cli()
    print(student_file_path, " ", room_file_path, " ", output_format, " ", output_destination)

    # load data
    rooms_generator = FileLoader.load_file_data(room_file_path)
    students_generator = FileLoader.load_file_data(student_file_path)

    # combine data
    combined_data_generator = DataCombiner.combine_students_with_rooms(students_generator, rooms_generator)

    # export in specified file
    Exporter.export_file(combined_data_generator)
