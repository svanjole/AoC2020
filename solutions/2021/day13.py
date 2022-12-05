from utils.abstract import FileReaderSolution
from abc import abstractmethod
import numpy as np
import pytesseract

class Day13:
    def __init__(self):
        self.coords = []
        self.instructions = []
        self.grid = np.zeros(0)

    @abstractmethod
    def solve_part(self, median):
        pass

    def solve(self, input_data: str) -> str:
        self.parse_input(input_data)

        return self.solve_part()

    def setup_grid(self):
        h = 1 + 2 * max(list(map(lambda x: x[1] if x[0] == 1 else 0, self.instructions)))
        w = 1 + 2 * max(list(map(lambda x: x[1] if x[0] == 0 else 0, self.instructions)))
        self.grid = np.zeros((w, h), dtype=int)
        for c in self.coords:
            self.grid[c[1]][c[0]] = 1

    def parse_input(self, input_data: str):
        lines = input_data.splitlines()
        fold_instruction = False
        for line in lines:
            if line == "":
                fold_instruction = True
                continue

            if fold_instruction:
                line = line.replace("fold along ", "")
                parts = line.split("=")

                self.instructions.append((0 if parts[0] == "y" else 1, int(parts[1])))
            else:
                coords = line.split(",")
                self.coords.append((int(coords[0]), int(coords[1])))

        self.setup_grid()

    def fold(self, amount_of_folds):
        for fold in range(amount_of_folds):
            instruction = self.instructions[fold]

            self.grid = np.delete(self.grid, instruction[1], instruction[0])
            parts = np.split(self.grid, [instruction[1]], instruction[0])
            parts[1] = np.flip(parts[1], instruction[0])
            self.grid = np.where(parts[0] != 0, parts[0], parts[1])


class Day13PartA(Day13, FileReaderSolution):
    def solve_part(self) -> int:
        amount_of_folds = 1
        self.fold(amount_of_folds)

        return np.count_nonzero(self.grid == 1)


class Day13PartB(Day13, FileReaderSolution):
    def solve_part(self) -> int:
        amount_of_folds = len(self.instructions)
        self.fold(amount_of_folds)
        output = "\n"
        for row in self.grid:
            output += ''.join(map(lambda x: "#" if x == 1 else " ", row)) + "\n"

        return output

