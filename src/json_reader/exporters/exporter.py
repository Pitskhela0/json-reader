from __future__ import annotations
import logging
import json
from abc import ABC, abstractmethod
from typing import Generator, Dict, Any
import xml.etree.ElementTree as ET

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class Exporter(ABC):
    """Abstract base class for all exporters"""
    default_path_counter = 0

    @abstractmethod
    def export_file(self, data_generator: Generator[Dict[str, Any], None, None], output_path: str) -> None:
        """Export data to file"""
        pass


class JSONExporter(Exporter):
    """JSON format exporter"""

    def export_file(self, data_generator: Generator[Dict[str, Any], None, None], output_path: str) -> None:
        """
        Export data to JSON format.

        Args:
            data_generator: Stream of room data with students
            output_path: Target JSON file path (auto-generates if no .json extension)
        """
        if not output_path.endswith(".json"):
            Exporter.default_path_counter += 1
            output_path = f"output/default{Exporter.default_path_counter}.json"

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

    def export_file(self, data_generator: Generator[Dict[str, Any], None, None], output_path: str) -> None:
        """Export data to XML format

        Args:
            data_generator: Stream of room data with students
            output_path: Target XML file path (auto-generates if no .xml extension)
        """
        if not output_path.endswith(".xml"):
            Exporter.default_path_counter += 1
            output_path = f"output/default{Exporter.default_path_counter}.xml"

        with open(output_path, "w", encoding='utf-8') as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<rooms>\n')

            for room_data in data_generator:
                room_elem = ET.Element("room", id=str(room_data["id"]))

                name_elem = ET.SubElement(room_elem, "name")
                name_elem.text = room_data["name"]

                students_elem = ET.SubElement(room_elem, "students")
                for student in room_data["students"]:
                    student_elem = ET.SubElement(students_elem, "student", id=str(student["id"]))
                    student_name = ET.SubElement(student_elem, "name")
                    student_name.text = student["name"]

                room_xml = ET.tostring(room_elem, encoding='unicode')
                file.write(f"  {room_xml}\n")

            file.write('</rooms>\n')

        logger.info(f"exported XML file at {output_path}")

