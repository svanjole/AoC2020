from utils.abstract import FileReaderSolution
from typing import List


class Day25:

    def __init__(self):
        pass


class Day25PartA(Day25, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        keys = [int(x) for x in input_data.splitlines()]
        card_pk = keys[0]
        door_pk = keys[1]

        print(card_pk,door_pk)
        card_loop = self.find_loop_size(7, card_pk)
        door_loop = self.find_loop_size(7, door_pk)

        print(card_loop, door_loop)
        encryption_key = self.calculate_encryption_key(door_pk, card_loop)

        return encryption_key

    def calculate_encryption_key(self, subject_number, loop):
        value = 1

        for i in range(loop):
            value *= subject_number
            value %= 20201227

        return value

    def find_loop_size(self, subject_number: int, public_key: int) -> int:
        loop_size = 0
        value = 1

        while value != public_key:
            value *= subject_number
            value %= 20201227

            loop_size += 1

        return loop_size


class Day25PartB(Day25, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        return 0