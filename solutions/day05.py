from utils.abstract import FileReaderSolution


class Passport:
    row: int
    col: int
    id: int

    def __init__(self, input_data: str):
        self.row = 0
        self.col = 0
        self.id = 0

        self.parse(input_data)

    def parse(self, input_data: str):
        row_lower = 0
        row_upper = 127

        col_lower = 0
        col_upper = 7

        for letter in input_data:
            if letter == "F":
                row_upper -= (row_upper - row_lower + 1) / 2
            elif letter == "B":
                row_lower += (row_upper - row_lower + 1) / 2
            elif letter == "R":
                col_lower += (col_upper - col_lower + 1) / 2
            elif letter == "L":
                col_upper -= (col_upper - col_lower + 1) / 2

        if row_lower != row_upper:
            raise ValueError

        if col_lower != col_upper:
            raise ValueError

        self.row = int(row_upper)
        self.col = int(col_upper)

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
