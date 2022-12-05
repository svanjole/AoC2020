from utils.abstract import FileReaderSolution
import re


class Day04:
    def solve(self, input_data: str) -> int:
        passports = self.parse_input_file(input_data)
        valid_passports = 0

        for passport in passports:
            if self.is_valid_passport(passport):
                valid_passports += 1

        return valid_passports

    def parse_input_file(self, input_data: str):
        passports = map(
            lambda x: self.create_passport(x),
            input_data.split("\n\n")
        )
        return passports

    @staticmethod
    def create_passport(passportlines):
        keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
        passportstr = ' '.join(map(str, passportlines.split("\n"))).split(' ')
        passport = {}

        for key in keys:
            passport[key] = None

        for field in passportstr:
            data = field.split(":")
            passport[data[0]] = data[1]

        return passport

    @staticmethod
    def are_all_field_present(passport) -> bool:
        return not any(passport[key] is None for key in passport)

    def is_valid_passport(self, passport):
        raise NotImplementedError


class Day04PartA(Day04, FileReaderSolution):

    def is_valid_passport(self, passport: str):
        return self.are_all_field_present(passport)


class Day04PartB(Day04, FileReaderSolution):

    def is_valid_passport(self, passport: str):
        if not self.are_all_field_present(passport):
            return False

        if not self.is_value_between(int(passport["byr"]), 1920, 2002):
            return False

        if not self.is_value_between(int(passport["iyr"]), 2010, 2020):
            return False

        if not self.is_value_between(int(passport["eyr"]), 2020, 2030):
            return False

        if not self.validate_height(passport["hgt"]):
            return False

        if not self.validate_regex(passport["hcl"], r'#[a-fA-F0-9]{6}$'):
            return False

        if not passport["ecl"] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            return False

        if not self.validate_regex(passport["pid"], r'[0-9]{9}$'):
            return False

        return True

    @staticmethod
    def is_value_between(value: int, minval: int, maxval: int) -> bool:
        return minval <= value <= maxval

    @staticmethod
    def validate_regex(value, regex):
        return bool(re.compile(regex).match(value))

    @staticmethod
    def validate_height(height: str) -> bool:
        if height.endswith("cm"):
            number = int(height[:-2])
            return 150 <= number <= 193
        elif height.endswith("in"):
            number = int(height[:-2])
            return 59 <= number <= 76
        else:
            return False
