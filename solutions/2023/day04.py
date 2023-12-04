from utils.abstract import FileReaderSolution


class Day04:
    @staticmethod
    def parse(input_data):
        cards = []

        for line in input_data.splitlines():
            numbers = line.split(": ")[1].split(" | ")

            winners = [int(x.strip(" ")) for x in numbers[0].split(" ") if x]
            numbers = [int(x.strip(" ")) for x in numbers[1].split(" ") if x]

            cards.append(len(set(winners) & set(numbers)))

        return cards


class Day04PartA(Day04, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        cards = self.parse(input_data)

        return sum([pow(2, matches-1) if matches > 0 else 0 for matches in cards])


class Day04PartB(Day04, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        cards = self.parse(input_data)
        amounts = [0 for _ in cards]

        for key, matches in enumerate(cards):
            amounts[key] += 1

            for copy in range(key+1, key+1+matches):
                amounts[copy] += amounts[key]

        return sum(amounts)
