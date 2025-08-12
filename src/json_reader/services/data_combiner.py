from collections import defaultdict
from collections.abc import Generator
from typing import Any
from ..constants.errors_messages import ErrorMessages


class DataCombiner:
    """Provides functionality to combine student and room data."""

    @staticmethod
    def group_students_by_room_id(
        students: Generator[dict[str, Any], None, None],
    ) -> dict[int, list[dict[str, Any]]]:
        """
        Group students by their room ID.

        Args:
            students: A generator yielding student dictionaries.

        Returns:
            dict: Mapping of room ID to a list of student dictionaries.

        Raises:
            ValueError: If a student record is missing required keys.
        """
        students_by_room: dict[int, list[dict[str, Any]]] = defaultdict(list)

        for student in students:
            try:
                room_id = student["room"]
                students_by_room[room_id].append(
                    {"id": student["id"], "name": student["name"]}
                )
            except KeyError as e:
                raise ValueError(ErrorMessages.STUDENT_MISSING_KEY.format(e)) from e

        return students_by_room

    @staticmethod
    def combine_students_with_rooms(
        students: Generator[dict[str, Any], None, None],
        rooms: Generator[dict[str, Any], None, None],
    ) -> Generator[dict[str, Any], None, None]:
        """
        Combine student and room data into a unified structure.

        Args:
            students: A generator yielding student dictionaries.
            rooms: A generator yielding room dictionaries.

        Yields:
            dict: Room data with an added 'students' list.

        Raises:
            ValueError: If a room record is missing required keys.
        """
        students_by_room = DataCombiner.group_students_by_room_id(students)

        for room in rooms:
            try:
                yield {
                    "id": room["id"],
                    "name": room["name"],
                    "students": students_by_room.get(room["id"], []),
                }
            except KeyError as e:
                raise ValueError(ErrorMessages.ROOM_MISSING_KEY.format(e)) from e