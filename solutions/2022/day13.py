from utils.abstract import FileReaderSolution


class Day13:
    def compare(self, a, b):
        for i in range(min(len(a), len(b))):
            a_is_number = isinstance(a[i], int)
            b_is_number = isinstance(b[i], int)

            if a_is_number and b_is_number:
                if a[i] == b[i]:
                    continue
                return a[i] < b[i]
            elif a_is_number or b_is_number:
                result = self.compare([a[i]], b[i]) if a_is_number else self.compare(a[i], [b[i]])
                if result is None:
                    continue
                return result
            else:
                result = self.compare(a[i], b[i])
                if result is None:
                    continue
                return result

        if len(a) != len(b):
            return len(a) < len(b)

        return None


class Day13PartA(Day13, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        indices = []
        for (index, block) in enumerate(input_data.split("\n\n")):
            parts = [eval(line) for line in block.split("\n")]
            if self.compare(parts[0], parts[1]):
                indices.append(index+1)

        return sum(indices)


class Day13PartB(Day13, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        items = [eval(line) for line in input_data.replace("\n\n", "\n").split("\n")]
        item_a = eval("[[2]]")
        item_b = eval("[[6]]")
        items.append(item_a)
        items.append(item_b)

        n = len(items)

        for i in range(n):
            sorted = True

            for j in range(n-i-1):
                if not self.compare(items[j], items[j+1]):
                    items[j], items[j+1] = items[j+1], items[j]
                    sorted = False

            if sorted:
                break

        return (items.index(item_a)+1) * (items.index(item_b)+1)
