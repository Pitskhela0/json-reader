from collections import defaultdict
from collections.abc import Generator
from typing import Any


class DataCombiner:

    @staticmethod
    def group_students_by_room_id(
        students: Generator[dict[str, Any], None, None]
    ) -> dict[int, list[dict[str, Any]]]:

        students_by_room: dict[int, list[dict[str, Any]]] = defaultdict(list)

        for student in students:
            try:
                room_id = student["room"]
                students_by_room[room_id].append({
                    "id": student["id"],
                    "name": student["name"]
                })
            except KeyError as e:
                raise ValueError(f"Student record missing required key: {e}") from e

        return students_by_room

    @staticmethod
    def combine_students_with_rooms(
        students: Generator[dict[str, Any], None, None],
        rooms: Generator[dict[str, Any], None, None]
    ) -> Generator[dict[str, Any], None, None]:

        students_by_room = DataCombiner.group_students_by_room_id(students)

        for room in rooms:
            try:
                yield {
                    "id": room["id"],
                    "name": room["name"],
                    "students": students_by_room.get(room["id"], [])
                }
            except KeyError as e:
                raise ValueError(f"Room record missing required key: {e}") from e
