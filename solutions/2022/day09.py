from utils.abstract import FileReaderSolution
import math


class Day09:
    def pretty_print(self, knots):
        all_positions = [tuple(knot) for knot in knots]

        min_x = min([knot[0] for knot in knots])
        max_x = max([knot[0] for knot in knots])
        min_y = min([knot[1] for knot in knots])
        max_y = max([knot[1] for knot in knots])

        lines = []
        for y in range(min_y, max_y + 5):
            line = ""
            for x in range(min_x, max_x + 5):
                if (x, y) in all_positions:
                    idx = all_positions.index((x, y))
                    line += f"{idx if idx > 0 else 'H'}"
                else:
                    line += "_" if x == 0 and y == 0 else "."
            lines.append(line)

        print("\n".join(lines))

    @staticmethod
    def base_solve(input_data: str, amount) -> int:
        visited = [(0, 0)]
        knots = [[0, 0] for i in range(amount)]

        directions = {
            "R": [1, 0],
            "U": [0, -1],
            "L": [-1, 0],
            "D": [0, 1],
        }

        for instruction in [instruction.split(" ") for instruction in input_data.split("\n")]:
            for step in range(int(instruction[1])):
                knots[0] = [a + b for (a, b) in zip(knots[0], directions[instruction[0]])]
                for i in range(1, amount):
                    if math.dist(knots[i], knots[i-1]) < 2.0:
                        break

                    knots[i] = [a + b for (a, b) in zip(knots[i], [((a - b) > 0) - ((a - b) < 0) for (a, b) in zip(knots[i - 1], knots[i])])]

                visited.append(tuple(knots[amount-1]))

        return len(set(visited))


class Day09PartA(Day09, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        return self.base_solve(input_data, 2)


class Day09PartB(Day09, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        return self.base_solve(input_data, 10)
