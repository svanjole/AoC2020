from utils.abstract import FileReaderSolution
import numpy as np


class BingoBoard:
    def __init__(self, numbers):
        self.numbers = np.array(numbers).reshape((5, 5))
        self.mask = np.zeros((5, 5))
        self.solved = False

    def get_value(self):
        sum = 0
        for y in range(0, 5):
            for x in range(0, 5):
                if self.mask[x][y] == 0:
                    sum += self.numbers[x][y]
        return sum

    def mark_number(self, i):
        result = np.where(self.numbers == i)
        coords = list(zip(result[0], result[1]))

        for coord in coords:
            self.mask[coord[0], coord[1]] = 1

        self.is_solved()

    def is_solved(self):
        for i in range(0,5):
            if np.sum(self.mask[i, :]) == 5:
                self.solved = True

            if np.sum(self.mask[:, i]) == 5:
                self.solved = True


class Day04:
    numbers: []
    boards: []

    def parse_input(self, input_data: str):
        lines = input_data.splitlines()
        self.numbers = list(map(lambda x: int(x), lines[0].split(",")))
        self.boards = []

        for s in range(2,len(lines), 6):
            board_lines = ' '.join(lines[s:s+5])
            numbers = list(map(lambda x: int(x), board_lines.split()))
            self.boards.append(BingoBoard(numbers))


class Day04PartA(Day04, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        for i in self.numbers:
            for board in self.boards:
                board.mark_number(i)
                if board.solved:
                    return board.get_value() * i


class Day04PartB(Day04, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        for i in self.numbers:
            for board in self.boards:
                if board.solved:
                    continue

                board.mark_number(i)

                if board.solved:
                    last_board_solved = board
                    last_number = i

        return last_board_solved.get_value() * last_number