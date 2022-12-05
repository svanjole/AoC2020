from utils.abstract import FileReaderSolution
from abc import abstractmethod
from enum import Enum


class StateEnum(Enum):
    Corrupted = 1
    Incomplete = 2
    Complete = 3


class State:
    def __init__(self, state: StateEnum, output: str = ""):
        self.state = state
        self.output = output


class Day10:
    def __init__(self):
        self.lines = []

    @abstractmethod
    def solve_part(self, median):
        pass

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        return self.solve_part()

    def parse_input(self, input_data: str):
        self.lines = input_data.splitlines()

    def common_solver(self):
        pass

    @staticmethod
    def check_line(line: str):
        chunks = {
            "(": ")",
            "[": "]",
            "{": "}",
            "<": ">"
        }
        open_chunks = []
        for char in line:
            if char in chunks.keys():
                open_chunks.append(char)
            else:
                last_chunk = open_chunks[-1]
                if chunks[last_chunk] != char:
                    return State(StateEnum.Corrupted, char)
                open_chunks.pop()

        if len(open_chunks) == 0:
            return State(StateEnum.Complete)

        open_chunks.reverse()
        remainder = ''.join(list(map(lambda x: chunks[x], open_chunks)))

        return State(StateEnum.Incomplete, remainder)


class Day10PartA(Day10, FileReaderSolution):
    def solve_part(self) -> int:
        chars = []
        scoring = {
            ")": 3,
            "]": 57,
            "}": 1197,
            ">": 25137
        }

        for line in self.lines:
            state = self.check_line(line)
            if state.state == StateEnum.Corrupted:
                chars.append(state.output)

        return sum(list(map(lambda x: scoring[x], chars)))


class Day10PartB(Day10, FileReaderSolution):
    def solve_part(self) -> int:
        scoring = {
            ")": 1,
            "]": 2,
            "}": 3,
            ">": 4
        }
        all_scores = []
        for line in self.lines:
            state = self.check_line(line)
            if state.state == StateEnum.Incomplete:
                score = 0
                for char in state.output:
                    score *= 5
                    score += scoring[char]
                all_scores.append(score)

        all_scores = sorted(all_scores)

        return all_scores[int(len(all_scores) / 2)]

