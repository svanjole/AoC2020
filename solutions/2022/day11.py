from utils.abstract import FileReaderSolution
import re
from math import prod, lcm
from operator import floordiv, mod


class Monkey:
    items: []
    items_inspected: int

    def __init__(self, id, items, inspect_function, divisor, recipients):
        self.id = id
        self.items = items
        self.inspect_item = inspect_function
        self.divisor = divisor
        self.recipients = recipients
        self.items_inspected = 0

    @staticmethod
    def parse(input_data):
        lines = input_data.split("\n")

        id = int(re.match(r".*(\d):", lines[0]).groups()[0])
        items = [int(x) for x in re.match(r".*Starting items: (.*)", lines[1]).groups()[0].split(", ")]

        function_string = re.match(r".*Operation: new = (.*)", lines[2]).groups()[0]
        function = eval(f"lambda old: {function_string}")

        divisor = int(re.match(r".*Test: divisible by (\d*)", lines[3]).groups()[0])

        recipients = [
            int(re.match(r".* monkey (\d*)", lines[5]).groups()[0]),
            int(re.match(r".* monkey (\d*)", lines[4]).groups()[0])
        ]

        return Monkey(id, items, function, divisor, recipients)

    def inspect(self, value):
        self.items_inspected += 1
        return self.inspect_item(value)


class Day11:
    monkeys: {}

    def __init__(self):
        self.monkeys = {}

    def parse(self, input_data):
        monkeys = input_data.split("\n\n")
        for m in monkeys:
            monkey = Monkey.parse(m)
            self.monkeys[monkey.id] = monkey

    def play_rounds(self, amount, op, number):
        for _ in range(amount):
            for monkey in self.monkeys.values():
                while len(monkey.items) > 0:
                    new_value = op(monkey.inspect(monkey.items.pop(0)), number)
                    recipient_id = monkey.recipients[new_value % monkey.divisor == 0]
                    self.monkeys[recipient_id].items.append(new_value)

        result = [m.items_inspected for m in self.monkeys.values()]
        result.sort()
        return prod(result[-2:])


class Day11PartA(Day11, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        return self.play_rounds(20, floordiv, 3)


class Day11PartB(Day11, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        return self.play_rounds(10000, mod, lcm(*[m.divisor for m in self.monkeys.values()]))

