from utils.abstract import FileReaderSolution
import operator

class Day03:
    @staticmethod
    def calculate_gamma(count):
        gamma = ""

        for c in count:
            if c["0"] > c["1"]:
                gamma += "0"
            else:
                gamma += "1"

        return gamma

    @staticmethod
    def calculate_epsilon(val):
        return ''.join('1' if x == '0' else '0' for x in val)


class Day03PartA(Day03, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        binary_numbers = input_data.splitlines()
        length = len(binary_numbers[0])
        count = []

        for i in range(0, length):
            count.append({"0": 0, "1": 0})

        for number in binary_numbers:
            for i in range(0, length):
                count[i][number[i]] += 1

        gamma = self.calculate_gamma(count)
        epsilon = self.calculate_epsilon(gamma)
        return int(gamma,2) * int(epsilon,2)


class Day03PartB(Day03, FileReaderSolution):
    @staticmethod
    def create_new_list(numbers, pos, bit):
        new_numbers = []
        for number in numbers:
            if number[pos] == bit:
                new_numbers.append(number)

        return new_numbers

    def calculate_number(self, numbers, relate):
        length = len(numbers[0])

        for pos in range(0, length):
            if len(numbers) == 1:
                return numbers[0]

            count = {"0": 0, "1": 0}

            for number in numbers:
                count[number[pos]] += 1

            if relate(count["0"], count["1"]):
                numbers = self.create_new_list(numbers, pos, "0")
            else:
                numbers = self.create_new_list(numbers, pos, "1")

        return numbers[0]

    def solve(self, input_data: str) -> int:
        binary_numbers = input_data.splitlines()

        x = self.calculate_number(binary_numbers, operator.gt)
        y = self.calculate_number(binary_numbers, operator.le)

        return int(x, 2) * int(y, 2)

