from utils.abstract import FileReaderSolution
import re


class Day01:
    numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    def solve(self, input_data: str) -> int:
        total = 0
        for line in input_data.split("\n"):
            total += self.find_digits(line)

        return total


class Day01PartA(Day01, FileReaderSolution):
    def find_digits(self, line: str) -> int:
        matches = list(map(lambda x: int(x), re.findall(r'\d', line)))
        return matches[0]*10 + matches[-1]


class Day01PartB(Day01, FileReaderSolution):
    def find_digits(self, line: str) -> int:
        first_digit, last_digit = None, None
        for i in range(len(line)):
            if line[i].isnumeric():
                if first_digit is None:
                    first_digit, last_digit = int(line[i]), int(line[i])
                else:
                    last_digit = int(line[i])
            else:
                for key, value in enumerate(self.numbers):
                    if line[i:i+len(value)] == value:
                        if first_digit is None:
                            first_digit, last_digit = key + 1, key + 1
                        else:
                            last_digit = key + 1
                        break

        return first_digit*10+last_digit

