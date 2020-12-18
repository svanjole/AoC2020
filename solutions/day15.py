from utils.abstract import FileReaderSolution


class Day15:
    def solve(self, input_data, rounds):
        numbers = [int(number) for number in input_data.split(",")]
        previous = {}

        for n in range(0, len(numbers)):
            previous[numbers[n]] = n+1

        last_seen_number = numbers[-1]

        for current_round in range(len(numbers) + 1, rounds + 1):
            if last_seen_number in previous:
                new_number = current_round - 1 - previous[last_seen_number]
            else:
                new_number = 0

            previous[last_seen_number] = current_round - 1
            last_seen_number = new_number

        return last_seen_number


class Day15PartA(Day15, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        return super().solve(input_data, 2020)


class Day15PartB(Day15, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        return super().solve(input_data, 30000000)
