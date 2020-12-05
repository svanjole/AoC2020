from utils.abstract import FileReaderSolution
import re

class Passport:
    row: int
    col: int
    id: int

    def __init__(self, input: str):
        self.row = 0
        self.col = 0
        self.id = 0

        self.parse(input)

    def parse(self, input: str):
        rowlower = 0
        rowupper = 127

        collower = 0
        colupper = 7

        for l in input:
            if l == "F":
                rowupper -= (rowupper - rowlower + 1) / 2
            elif l == "B":
                rowlower += (rowupper - rowlower + 1) / 2
            elif l == "R":
                collower += (colupper - collower + 1) / 2
            elif l == "L":
                colupper -= (colupper - collower + 1) / 2

        if rowlower != rowupper:
            raise ValueError

        if collower != colupper:
            raise ValueError

        self.row = int(rowupper)
        self.col = int(colupper)

        self.id = self.row * 8 + self.col


class Day05:
    @staticmethod
    def solve_internal(input_data: str):
        return map(
            lambda x: Passport(x),
            input_data.split("\n")
        )


class Day05PartA(Day05, FileReaderSolution):

    def solve(self, input_data: str) -> int:
        passports = self.solve_internal(input_data)
        max_id = 0

        for passport in passports:
            if passport.id > max_id:
                max_id = passport.id

        return max_id


class Day05PartB(Day05, FileReaderSolution):

    def solve(self, input_data: str) -> int:
        passports = self.solve_internal(input_data)
        ids = sorted(list(map(lambda x: x.id, passports)))

        for pos in range(1, len(ids)-2):
            if ids[pos-1] == ids[pos] - 2 and ids[pos+1] == ids[pos] + 1:
                return ids[pos] - 1
            elif ids[pos-1] == ids[pos] - 1 and ids[pos+1] == ids[pos] + 2:
                return ids[pos] + 1

        return 0
