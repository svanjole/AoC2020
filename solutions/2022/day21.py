from utils.abstract import FileReaderSolution
import operator


class Day21:
    def __init__(self):
        self.unknown = {}
        self.known = {}

    @staticmethod
    def cmp(a, b):
        return (a > b) - (a < b)

    def parse(self, input_data, override_root=False):
        self.unknown = {}
        self.known = {}
        for line in input_data.split("\n"):
            parts = line.split(" ")
            key = parts[0][0:4]
            if len(parts) == 2:
                self.known[key] = int(parts[1])
            else:
                op = None
                if override_root and key == "root":
                    op = self.cmp
                else:
                    match parts[2]:
                        case "+":
                            op = operator.add
                        case "-":
                            op = operator.sub
                        case "/":
                            op = operator.truediv
                        case "*":
                            op = operator.mul

                self.unknown[key] = (parts[1], op, parts[3])

    def base_solve(self):
        while len(self.unknown) > 0:
            key = list(self.unknown.keys())[0]
            unknown = self.unknown[key]
            del self.unknown[key]
            a = unknown[0]
            b = unknown[2]
            known = 0
            if a in self.known.keys():
                a = self.known[unknown[0]]
                known += 1
            if b in self.known.keys():
                b = self.known[unknown[2]]
                known += 1

            if known == 2:
                self.known[key] = unknown[1](a, b)
            else:
                self.unknown[key] = unknown


class Day21PartA(Day21, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        self.base_solve()

        return int(self.known["root"])


class Day21PartB(Day21, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        for j in range(2):
            low = 0
            high = 9999999999999 + 1
            i = low + ((high - low) // 2)
            prev = None

            while prev != i:
                self.parse(input_data, True)
                self.known["humn"] = i
                self.base_solve()
                prev = i
                if self.known["root"] == 0:
                    return i

                if self.known["root"] == 1:
                    low, high = (i, high) if j == 0 else (low, i)
                elif self.known["root"] == -1:
                    low, high = (i, high) if j == 1 else (low, i)

                i = low + ((high - low) // 2)

        return -1
