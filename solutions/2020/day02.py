from utils.abstract import FileReaderSolution
import re


class Day02:
    def solve(self, input_data: str) -> int:
        valid_passwords = 0
        for line in input_data.split("\n"):
            result = re.match(r"(\d*)-(\d*) (.): (\w*)", line)

            assert result

            pos1 = int(result[1])
            pos2 = int(result[2])
            letter = result[3]
            password = result[4]

            if self.is_valid_password(pos1, pos2, letter, password):
                valid_passwords += 1

        return valid_passwords


class Day02PartA(Day02, FileReaderSolution):
    @staticmethod
    def is_valid_password(pos1, pos2, needle, password):
        letters = []
        letters[:0] = password
        count = 0

        for letter in letters:
            if letter == needle:
                count += 1

        return pos1 <= count <= pos2


class Day02PartB(Day02, FileReaderSolution):
    @staticmethod
    def is_valid_password(pos1, pos2, letter, password):
        return (password[pos1 - 1] == letter) ^ (password[pos2 - 1] == letter)
