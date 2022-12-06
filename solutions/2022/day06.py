from utils.abstract import FileReaderSolution


class Day06:
    @staticmethod
    def base_solve(s, l):
        return next(i + l for i in range(0, len(s)) if len(set(s[i:i + l])) == l)


class Day06PartA(Day06, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        return self.base_solve(input_data, 4)


class Day06PartB(Day06, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        return self.base_solve(input_data, 14)
