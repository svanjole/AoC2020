from utils.abstract import FileReaderSolution
from abc import abstractmethod
import statistics


class Day08:
    def __init__(self):
        self.numbers = []
        self.signals = []
        self.mapping = {}
        self.digits = {
            "ABCEFG": 0,
            "CF": 1,
            "ACDEG": 2,
            "ACDFG": 3,
            "BCDF": 4,
            "ABDFG": 5,
            "ABDEFG": 6,
            "ACF": 7,
            "ABCDEFG": 8,
            "ABCDFG": 9,


        }

    @abstractmethod
    def solve_part(self):
        pass

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)
        return self.solve_part()

    def find_signal_of_length(self, length):
        return list(map(lambda x: set(x), [number for number in self.signals if len(number) == length]))

    def get_unknown_keys(self):
        unknowns = set()
        for key in self.mapping.keys():
            if self.mapping[key] == "":
                unknowns.add(key)

        return unknowns

    def create_mappings(self):
        self.mapping = {
            "a": "",
            "b": "",
            "c": "",
            "d": "",
            "e": "",
            "f": "",
            "g": ""
        }
        number_1 = self.find_signal_of_length(2)[0]
        number_4 = self.find_signal_of_length(4)[0]
        number_7 = self.find_signal_of_length(3)[0]
        number_8 = self.find_signal_of_length(7)[0]

        diff = number_7.difference(number_1)
        # difference of 7 and 1 is segment A
        self.mapping[diff.pop()] = "A"

        numbers_6 = self.find_signal_of_length(6) # return 0, 6 and 9, but only 6 does not have C AND F
        for number in numbers_6:
            diff = number.intersection(number_1)
            if len(diff) == 1:
                self.mapping[diff.pop()] = "F"
        # we know F now, remaining one is C
        for number in numbers_6:
            diff = number.intersection(number_1)
            if len(diff) == 1:
                continue
            for d in diff:
                if self.mapping[d] == "":
                    self.mapping[d] = "C"

        # 4 has B D as unknowns, 9 has B D and G as unknowns, difference is G.
        # Find number 9
        for number in numbers_6:
            intersect = number.intersection(number_4)
            if len(intersect) == 4: # found number 9
                difference = number.difference(number_4)
                for diff in difference:
                    if self.mapping[diff] == "":
                        self.mapping[diff] = "G"

        # we know A C F and G. Number 3 has only one unknown D
        numbers_5 = self.find_signal_of_length(5)
        for number in numbers_5:
            intersect = number.intersection(self.get_unknown_keys())
            if len(intersect) == 1:
                self.mapping[intersect.pop()] = "D"
                break

        # we now know A C D F and G. Number 4 has only one unknown "B"
        intersect = number_4.intersection(self.get_unknown_keys())
        self.mapping[intersect.pop()] = "B"

        intersect = number_8.intersection(self.get_unknown_keys())
        self.mapping[intersect.pop()] = "E"

    def parse_input(self, input_data: str):
        self.lines = input_data.splitlines()

    def convert_number_to_digit(self, number):
        fixed = ""

        for n in number:
            fixed += self.mapping[n]

        fixed = ''.join(sorted(fixed))

        return self.digits[fixed]

    def common_solver(self):
        pass


class Day08PartA(Day08, FileReaderSolution):
    def solve_part(self) -> int:

        valid_numbers = [1, 4, 7, 8]
        count = 0
        for line in self.lines:
            data = line.split("|")
            self.signals = list(map(lambda x: ''.join(sorted(x)), data[0].split()))
            self.numbers = list(map(lambda x: ''.join(sorted(x)), data[1].split()))
            self.create_mappings()

            for number in self.numbers:
                digit = self.convert_number_to_digit(number)
                if digit in valid_numbers:
                    count += 1

        return count


class Day08PartB(Day08, FileReaderSolution):
    def solve_part(self) -> int:
        total = 0
        for line in self.lines:
            data = line.split("|")
            self.signals = list(map(lambda x: ''.join(sorted(x)), data[0].split()))
            self.numbers = list(map(lambda x: ''.join(sorted(x)), data[1].split()))
            self.create_mappings()
            result = 0

            for number in self.numbers:
                digit = int(self.convert_number_to_digit(number))
                print(result, digit)
                result *= 10
                result += digit

            total += result

        return total
