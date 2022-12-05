from utils.abstract import FileReaderSolution


class Day01:

    pass


class Day01PartA(Day01, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        count = 0
        ints = [int(x) for x in input_data.split("\n")]
        for i in range(0, len(ints)):
            if ints[i] > ints[i-1]:
                count += 1

        return count


class Day01PartB(Day01, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        ints = [int(x) for x in input_data.split("\n")]
        sums = []
        count = 0
        for i in range(0, len(ints)-2):
            sums.append(sum(ints[i:i+3]))

        for i in range(0, len(sums)):
            if sums[i] > sums[i - 1]:
                count += 1

        return count

