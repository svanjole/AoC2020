from utils.abstract import FileReaderSolution


class Day01:
    @staticmethod
    def get_calories(input_data: str):
        currentSum = 0
        sum = []
        for line in input_data.split("\n"):
            if line == "":
                sum.append(currentSum)
                currentSum = 0
            else:
                currentSum += int(line)

        return sum

class Day01PartA(Day01, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        totals = self.get_calories(input_data)
        return max(totals)


class Day01PartB(Day01, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        totals = self.get_calories(input_data)
        totals.sort()
        return sum(totals[-3:])
