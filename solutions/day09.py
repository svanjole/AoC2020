from utils.abstract import FileReaderSolution


class Day09:
    def find_anomaly(self, list_of_numbers, preamble: int) -> int:
        for index in range(preamble, len(list_of_numbers)):
            if not self.is_valid_number(list_of_numbers[index], list_of_numbers[index-preamble:index]):
                return list_of_numbers[index]

    @staticmethod
    def is_valid_number(number, list_of_numbers) -> bool:
        for n in list_of_numbers:
            temp = number-n
            if temp in list_of_numbers and temp != n:
                return True

        return False


class Day09PartA(Day09, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        list_of_numbers = list(map(lambda x: int(x),input_data.split("\n")))

        return self.find_anomaly(list_of_numbers, 25)


class Day09PartB(Day09, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        list_of_numbers = list(map(lambda x: int(x), input_data.split("\n")))
        anomaly = self.find_anomaly(list_of_numbers, 25)
        subset = self.find_set(list_of_numbers, anomaly)

        return min(subset) + max(subset)

    @staticmethod
    def find_set(list_of_numbers, anomaly):
        length = len(list_of_numbers)
        for i in range(0, length):
            subset = []

            for j in range(i, length):
                subset.append(list_of_numbers[j])
                total = sum(subset)

                if total == anomaly:
                    return subset
                elif total > anomaly:
                    break

        return []
