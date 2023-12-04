from utils.abstract import FileReaderSolution


class Day04:
    @staticmethod
    def parse(input_data):
        matches = []

        for line in input_data.splitlines():
            numbers = line.split(": ")[1].split(" | ")

            winners = [int(x) for x in numbers[0].split(" ") if x]
            numbers = [int(x) for x in numbers[1].split(" ") if x]

            matches.append(len(set(winners) & set(numbers)))

        return matches


class Day04PartA(Day04, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        matches = self.parse(input_data)

        return sum([pow(2, match-1) if match > 0 else 0 for match in matches])


class Day04PartB(Day04, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        matches = self.parse(input_data)
        amounts = [0] * len(matches)

        for key, match in enumerate(matches):
            amounts[key] += 1

            for copy in range(key+1, key+1+match):
                amounts[copy] += amounts[key]

        return sum(amounts)
