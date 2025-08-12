import argparse
import os
from pathlib import Path
from ..constants.errors_messages import ErrorMessages
from ..constants.cli_parser_constants import CLIParserConstants


class CLIParser:
    """Command-line interface parser for application arguments."""

    @staticmethod
    def _validate_output_path(output_path: str) -> None:
        """
        Validate output path and ensure directory can be created.

        Args:
            output_path: Path for output file

        Raises:
            ValueError: If path is invalid or directory cannot be created
        """
        if output_path == "/output":
            output_dir = Path("output")
            if output_dir.exists():
                if not os.access(output_dir, os.W_OK):
                    raise ValueError(ErrorMessages.NO_WRITE_PERMISSION_DIR.format(output_dir))
            else:
                try:
                    output_dir.mkdir(parents=True, exist_ok=True)
                    print(f"Created default output directory: {output_dir}")
                except OSError as e:
                    raise ValueError(ErrorMessages.CANNOT_CREATE_OUTPUT_DIR.format(output_dir, e)) from e
            return

        path = Path(output_path)
        parent_dir = path.parent

        if parent_dir.exists():
            if not os.access(parent_dir, os.W_OK):
                raise ValueError(ErrorMessages.NO_WRITE_PERMISSION_DIR.format(parent_dir))
        else:
            try:
                parent_dir.mkdir(parents=True, exist_ok=True)
                print(f"Created output directory: {parent_dir}")
            except OSError as e:
                raise ValueError(ErrorMessages.CANNOT_CREATE_OUTPUT_DIR.format(parent_dir, e)) from e

        if path.exists():
            if not os.access(path, os.W_OK):
                raise ValueError(ErrorMessages.NO_WRITE_PERMISSION_FILE.format(output_path))
            else:
                print(
                    f"Warning: Output file {output_path} "
                    f"already exists and will be overwritten"
                )

    @staticmethod
    def parse_cli() -> tuple[str, str, str, str]:
        """
        Parse command-line arguments for the application.

        Returns:
            tuple: (student_file_path, room_file_path,
             output_format, output_destination)
        """
        parser = argparse.ArgumentParser(description="parse CLI")

        parser.add_argument(
            CLIParserConstants.STUDENT_FILE_PATH_ARG,
            type=str,
            required=True,
            help="path to students' json file",
        )

        parser.add_argument(
            CLIParserConstants.ROOM_FILE_PATH_ARG, type=str, required=True, help="path to room json file"
        )

        parser.add_argument(
            CLIParserConstants.OUTPUT_FORMAT_ARG,
            type=str,
            choices=[CLIParserConstants.JSON_FILE_TYPE, CLIParserConstants.XML_FILE_TYPE],
            help="output file format",
        )

        parser.add_argument(
            CLIParserConstants.OUTPUT_DESTINATION_ARG,
            type=str,
            default=CLIParserConstants.DEFAULT_OUTPUT_DIRECTORY,
            help="output destination",
        )

        arguments = parser.parse_args()

        if arguments.output_destination != CLIParserConstants.DEFAULT_OUTPUT_DIRECTORY and (
                not arguments.output_destination.endswith(CLIParserConstants.JSON_EXTENSION)
                and not arguments.output_destination.endswith(CLIParserConstants.XML_EXTENSION)
        ):
            raise ValueError(ErrorMessages.INVALID_FILE_EXTENSION.format(arguments.output_destination))

        if (
                arguments.output_destination.endswith(CLIParserConstants.JSON_EXTENSION)
                and arguments.output_format == CLIParserConstants.XML_FILE_TYPE
        ):
            raise ValueError(ErrorMessages.FORMAT_MISMATCH_XML_JSON)

        if (
                arguments.output_destination.endswith(CLIParserConstants.XML_EXTENSION)
                and arguments.output_format == CLIParserConstants.JSON_FILE_TYPE
        ):
            raise ValueError(ErrorMessages.FORMAT_MISMATCH_JSON_XML)

        try:
            CLIParser._validate_output_path(arguments.output_destination)
        except ValueError:
            raise ValueError(ErrorMessages.INVALID_OUTPUT_PATH)

        return (
            arguments.student_file_path,
            arguments.room_file_path,
            arguments.output_format,
            arguments.output_destination,
        )
