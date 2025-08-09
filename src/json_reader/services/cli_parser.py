import argparse


class CLIParser:
    """Command-line interface parser for application arguments."""

    @staticmethod
    def parse_cli() -> tuple[str, str, str, str]:
        """
        Parse command-line arguments for the application.

        Returns:
            tuple: (student_file_path, room_file_path, output_format, output_destination)
        """
        parser = argparse.ArgumentParser(description='parse CLI')

        parser.add_argument(
            "--student-file-path",
            type=str,
            required=True,
            help="path to students' json file")

        parser.add_argument(
            "--room-file-path",
            type=str,
            required=True,
            help="path to room json file"
        )

        parser.add_argument(
            "--output-format",
            type=str,
            choices=["json", "xml"],
            help="output file format"
        )

        parser.add_argument(
            "--output-destination",
            type=str,
            default="/output",
            help="output destination"
        )

        arguments = parser.parse_args()

        if (arguments.output_destination != "/output" and
                (not arguments.output_destination.endswith(".json") and
                 not arguments.output_destination.endswith(".xml"))):
            raise ValueError(f"Custom output path must end with .json "
                             f"or .xml, got: {arguments.output_destination}")

        return (
            arguments.student_file_path,
            arguments.room_file_path,
            arguments.output_format,
            arguments.output_destination
        )
