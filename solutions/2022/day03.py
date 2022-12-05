from utils.abstract import FileReaderSolution


class Day03:
    @staticmethod
    def solve_puzzle(groups):
        score = 0

        for group in groups:
            overlap = group.pop()
            for rucksack in group:
                overlap = ''.join(set(overlap).intersection(rucksack))

            if ord(overlap) >= 97:
                score += ord(overlap) - 96
            else:
                score += ord(overlap) - 38

        return score


class Day03PartA(Day03, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        groups = []
        for line in input_data.split("\n"):
            length = len(line)
            size = length // 2
            group = [line[i:i + size] for i in range(0, length, size)]
            groups.append(group)

        return self.solve_puzzle(groups)


class Day03PartB(Day03, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        groups = []
        group = []
        i = 1

        for line in input_data.split("\n"):
            group.append(line)
            if i % 3 == 0:
                groups.append(group)
                group = []

            i += 1

        return self.solve_puzzle(groups)
