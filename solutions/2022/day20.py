from utils.abstract import FileReaderSolution
from copy import deepcopy

class Day20:
    def __init__(self):
        self.data = []

    def parse(self, input_data):
        self.data = [(x,v) for x,v in enumerate(list(map(int, input_data.split("\n"))))]
        #print(self.data)

    def mix(self):
        length = len(self.data)
        for i in range(length):
            for j, v in self.data:
                if j == i:
                    idx = self.data.index((j, v))
                    # print(idx, v)
                    # print([v for _, v in self.data])

                    new_idx = (idx + v) % (length - 1)
                    # print(new_idx)
                    del self.data[idx]
                    self.data.insert(new_idx, (j, v))

                    # print([v for _, v in self.data])
                    # print(v, "move", idx, "->", new_idx)
                    # print()
                    break


class Day20PartA(Day20, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        self.mix()

        idx = [i for i, v in enumerate(self.data) if v[1] == 0][0]
        numbers = [self.data[(idx + i * 1000) % len(self.data)][1] for i in [1, 2, 3]]
        return sum(numbers)


class Day20PartB(Day20, FileReaderSolution):
    def transform(self):
        for idx, (i, v) in enumerate(self.data):
            self.data[idx] = (i, v*811589153)

    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        self.transform()
        #print("Initial arrangement:")
        #print(self.data)

        for i in range(10):
            #print(f"Round {i+1}:")
            self.mix()
            #print(self.data)

        idx = [i for i, v in enumerate(self.data) if v[1] == 0][0]
        numbers = [self.data[(idx + i * 1000) % len(self.data)][1] for i in [1, 2, 3]]
        return sum(numbers)