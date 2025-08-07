from collections import defaultdict
from typing import Generator


class DataCombiner:
    @staticmethod
    def group_students_by_roomID(students_generator: Generator[dict, None, None]) -> dict:
        student_by_room = defaultdict(list)

        for student in students_generator:
            student_by_room[student['room']].append({
                "id": student['id'],
                "name": student['name']
            })

        return student_by_room

    @staticmethod
    def combine_students_with_rooms(students_generator: Generator[dict, None, None],
                                    rooms_generator: Generator[dict, None, None]
                                    ) -> Generator[dict, None, None]:
        student_by_room = DataCombiner.group_students_by_roomID(students_generator)

        for room in rooms_generator:
            combined_room = {
                "id": room['id'],
                "name": room['name'],
                "students": student_by_room.get(room['id'], [])
            }
            yield combined_room
