from utils.abstract import FileReaderSolution
from abc import abstractmethod
from enum import Enum
import numpy as np


class Rule:
    value: int

    def __init__(self):
        self.ranges = {}
        self.value = 0

    @staticmethod
    def parse(line):
        rule = Rule()

        parts = line.split(" ")
        ranges = parts[1].split(",")

        rule.value = 1 if parts[0] == "on" else 0

        rule.ranges['x'] = Rule.parse_range(ranges[0])
        rule.ranges['y'] = Rule.parse_range(ranges[1])
        rule.ranges['z'] = Rule.parse_range(ranges[2])

        return rule

    @staticmethod
    def parse_range(range):
        range = range[2:].split("..")
        return (
           int(range[0]),
           int(range[1])+1
        )

    def __str__(self):
        return f"{self.value} {str(self.ranges)}"

    def __repr__(self):
        return self.__str__()


class Day22:
    def __init__(self):
        self.rules = []

    @abstractmethod
    def solve_part(self):
        pass

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        return self.solve_part()

    def parse_input(self, input_data: str):
        rules = input_data.splitlines()
        for rule in rules:
            self.rules.append(Rule.parse(rule))

    def common_solver(self):
        pass


class Day22PartA(Day22, FileReaderSolution):
    def fix_ranges(self):
        for rule in self.rules:
            for range in rule.ranges:
                rule.ranges[range] = (
                    max(-51, min(51, int(rule.ranges[range][0]))),
                    max(-51, min(51, int(rule.ranges[range][1]))),
                )

    def solve_part(self) -> int:
        cubes = np.zeros((100, 100, 100), dtype=bool)
        self.fix_ranges()
        for rule in self.rules:
            count = 0
            for x in range(*rule.ranges['x']):
                for y in range(*rule.ranges['y']):
                    for z in range(*rule.ranges['z']):
                        if x < -50 or x > 50:
                            continue
                        if y < -50 or y > 50:
                            continue
                        if z < -50 or z > 50:
                            continue
                        count += 1
                        cubes[x, y, z] = rule.value
        return np.count_nonzero(cubes)


class Day22PartB(Day22, FileReaderSolution):
    def solve_part(self) -> int:
        count = 0
        for rule in self.rules:
            cube_size = (rule.ranges['x'][1] - rule.ranges['x'][0])
            cube_size *= (rule.ranges['y'][1] - rule.ranges['y'][0])
            cube_size *= (rule.ranges['z'][1] - rule.ranges['z'][0])

            if rule.value == 1:
                count += cube_size
            else:
                count -= cube_size
        return count


