import argparse
import os
from pathlib import Path


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
                    raise ValueError(
                        f"No write permission " f"for output directory: {output_dir}"
                    )
            else:
                try:
                    output_dir.mkdir(parents=True, exist_ok=True)
                    print(f"Created default output directory: {output_dir}")
                except OSError as e:
                    raise ValueError(
                        f"Cannot create output directory {output_dir}: {e}"
                    ) from e
            return

        path = Path(output_path)
        parent_dir = path.parent

        if parent_dir.exists():
            if not os.access(parent_dir, os.W_OK):
                raise ValueError(f"No write permission " f"for directory: {parent_dir}")
        else:
            try:
                parent_dir.mkdir(parents=True, exist_ok=True)
                print(f"Created output directory: {parent_dir}")
            except OSError as e:
                raise ValueError(
                    f"Cannot create output directory {parent_dir}: {e}"
                ) from e

        if path.exists():
            if not os.access(path, os.W_OK):
                raise ValueError(
                    f"No write permission for existing file: {output_path}"
                )
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
            "--student-file-path",
            type=str,
            required=True,
            help="path to students' json file",
        )

        parser.add_argument(
            "--room-file-path", type=str, required=True, help="path to room json file"
        )

        parser.add_argument(
            "--output-format",
            type=str,
            choices=["json", "xml"],
            help="output file format",
        )

        parser.add_argument(
            "--output-destination",
            type=str,
            default="/output",
            help="output destination",
        )

        arguments = parser.parse_args()

        if arguments.output_destination != "/output" and (
            not arguments.output_destination.endswith(".json")
            and not arguments.output_destination.endswith(".xml")
        ):
            raise ValueError(
                f"Custom output path must end with .json "
                f"or .xml, got: {arguments.output_destination}"
            )

        if (
            arguments.output_destination.endswith(".json")
            and arguments.output_format == "xml"
        ):
            raise ValueError("Output format is " "xml and destination types is JSON")

        if (
            arguments.output_destination.endswith(".xml")
            and arguments.output_format == "json"
        ):
            raise ValueError("Output format" " is JSON and destination types is xml")

        try:
            CLIParser._validate_output_path(arguments.output_destination)
        except ValueError:
            raise ValueError("Invalid output path")

        return (
            arguments.student_file_path,
            arguments.room_file_path,
            arguments.output_format,
            arguments.output_destination,
        )
