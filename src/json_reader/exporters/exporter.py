from __future__ import annotations

import json
import logging
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Any, Dict, Generator
from ..constants.exporter_constants import ExporterConstants

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class Exporter(ABC):
    """Abstract base class for all exporters"""

    default_path_counter = 0

    @abstractmethod
    def export_file(
        self, data_generator: Generator[Dict[str, Any], None, None], output_path: str
    ) -> None:
        """Export data to file"""
        pass


class JSONExporter(Exporter):
    """JSON format exporter"""

    def export_file(
        self, data_generator: Generator[Dict[str, Any], None, None], output_path: str
    ) -> None:
        """
        Export data to JSON format.

        Args:
            data_generator: Stream of room data with students
            output_path: Target JSON file path
            (auto-generates if no .json extension)
        """
        if not output_path.endswith(ExporterConstants.JSON_EXTENSION):
            Exporter.default_path_counter += 1
            output_path = (ExporterConstants.DEFAULT_OUTPUT_DIR +
                           ExporterConstants.DEFAULT_FILE_NAME +
                           str(Exporter.default_path_counter) +
                           ExporterConstants.JSON_EXTENSION)

        with open(output_path, "w") as file:
            file.write("[")
            first_item = True

            for item in data_generator:
                if not first_item:
                    file.write(",")
                file.write(json.dumps(item))
                first_item = False

            file.write("]")

        logger.info(f"exported JSON file at {output_path}")


class XMLExporter(Exporter):
    """XML format exporter"""

    def export_file(
        self, data_generator: Generator[Dict[str, Any], None, None], output_path: str
    ) -> None:
        """Export data to XML format

        Args:
            data_generator: Stream of room data with students
            output_path: Target XML file path
            (auto-generates if no .xml extension)
        """
        if not output_path.endswith(ExporterConstants.XML_EXTENSION):
            Exporter.default_path_counter += 1
            output_path = (ExporterConstants.DEFAULT_OUTPUT_DIR +
                           ExporterConstants.DEFAULT_FILE_NAME +
                           str(Exporter.default_path_counter) +
                           ExporterConstants.XML_EXTENSION)

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(ExporterConstants.XML_DECLARATION)
            file.write(f"<{ExporterConstants.XML_ROOT_ELEMENT}>\n")

            for room_data in data_generator:
                room_elem = ET.Element(ExporterConstants.XML_ROOM_ELEMENT,
                                       id=str(room_data[ExporterConstants.ID_FIELD]))

                name_elem = ET.SubElement(room_elem, ExporterConstants.XML_NAME_ELEMENT)
                name_elem.text = room_data[ExporterConstants.NAME_FIELD]

                students_elem = ET.SubElement(room_elem, ExporterConstants.XML_STUDENTS_ELEMENT)
                for student in room_data[ExporterConstants.STUDENTS_FIELD]:
                    student_elem = ET.SubElement(
                        students_elem, ExporterConstants.XML_STUDENT_ELEMENT,
                        id=str(student[ExporterConstants.ID_FIELD])
                    )
                    student_name = ET.SubElement(student_elem, ExporterConstants.XML_NAME_ELEMENT)
                    student_name.text = student[ExporterConstants.NAME_FIELD]

                room_xml = ET.tostring(room_elem, encoding=ExporterConstants.UNICODE_ENCODING)
                file.write(f"  {room_xml}\n")

            file.write(f"</{ExporterConstants.XML_ROOT_ELEMENT}>\n")

        logger.info(ExporterConstants.LOG_XML_EXPORTED.format(output_path))
