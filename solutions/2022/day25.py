from utils.abstract import FileReaderSolution
import math


class Day25:
    pass


class Day25PartA(Day25, FileReaderSolution):
    def convert_to_snafu(self, number):
        snafu = []
        translation = {-2: '=', -1: '-'}
        while number:
            number, res = divmod(number, 5)
            if res == 3:
                number += 1
                res = -2
            elif res == 4:
                number += 1
                res = -1
            snafu.append(res)

        return "".join([str(digit) if digit >= 0 else translation[digit] for digit in reversed(snafu)])
    def convert_to_decimal(self, number):
        decimal = 0
        length = len(number)
        for x in range(length-1, -1, -1):
            pos = length-x-1
            match number[x]:
                case "2":
                    decimal += 2 * int(math.pow(5,pos))
                case "1":
                    decimal += 1 * int(math.pow(5, pos))
                case "-":
                    decimal += -1 * int(math.pow(5, pos))
                case "=":
                    decimal += -2 * int(math.pow(5, pos))

        return decimal

    def solve(self, input_data: str) -> int:
        total = sum([self.convert_to_decimal(number) for number in input_data.split("\n")])
        print(total)
        return self.convert_to_snafu(total)


class Day25PartB(Day25, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        return 0
