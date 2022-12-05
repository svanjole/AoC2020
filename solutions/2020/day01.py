from utils.abstract import FileReaderSolution


class Day01:
    pass


class Day01PartA(Day01, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        ints = [int(x) for x in input_data.split("\n")]
        for a in ints:
            for b in ints:
                if a+b == 2020:
                    return a*b


class Day01PartB(Day01, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        ints = [int(x) for x in input_data.split("\n")]
        for a in ints:
            for b in ints:
                for c in ints:
                    if a+b+c == 2020:
                        return a * b * c
