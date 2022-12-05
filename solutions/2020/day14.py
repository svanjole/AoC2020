from utils.abstract import FileReaderSolution
import re
import math


class Day14:
    mask: str
    memory: {}

    def __init__(self):
        self.memory = {}

    def set_mask(self, mask):
        self.mask = mask.split(" = ")[1]

    def set_memory(self, address, value):
        self.memory[address] = value


class Day14PartA(Day14, FileReaderSolution):
    def apply_mask(self, value):
        binary_value = list(f"{value:036b}")
        for i in range(0, len(self.mask)):
            if self.mask[i] == 'X':
                continue

            if self.mask[i] is not binary_value[i]:
                binary_value[i] = self.mask[i]

        return "".join(binary_value)

    def solve(self, input_data: str) -> int:
        lines = input_data.splitlines()
        for line in lines:
            if line.find('mask') >= 0:
                self.set_mask(line)
                continue

            matches = re.match(r'mem\[(\d*)?] = (\d*)?', line)
            address = int(matches[1])
            value = int(matches[2])

            masked_binary_value = self.apply_mask(value)

            self.set_memory(address, int(masked_binary_value, 2))

        return sum(self.memory.values())


class Day14PartB(Day14, FileReaderSolution):
    def apply_mask(self, value):
        binary_value = list(f"{value:036b}")
        for i in range(0, len(self.mask)):
            if self.mask[i] != '0':
                binary_value[i] = self.mask[i]

        return "".join(binary_value)

    def solve(self, input_data: str) -> int:
        lines = input_data.splitlines()
        for line in lines:
            if line.find('mask') >= 0:
                self.set_mask(line)
                continue

            matches = re.match(r'mem\[(\d*)?] = (\d*)?', line)
            address = int(matches[1])
            value = int(matches[2])

            masked_address = self.apply_mask(address)
            addresses = self.create_addresses(list(masked_address))

            for address in addresses:
                self.set_memory(int(address, 2), value)

        return sum(self.memory.values())

    @staticmethod
    def create_addresses(input_lst):
        count = input_lst.count('X')
        addresses = []

        for number in range(0, int(math.pow(2, count))):
            address = input_lst.copy()
            binary = list(f"{number:0{count}b}")
            pos = 0

            for j in range(0, len(address)):
                if address[j] == 'X':
                    address[j] = binary[pos]
                    pos += 1

            addresses.append("".join(address))

        return addresses

    @staticmethod
    def change_character(input_str, index, char):
        s = list(input_str)
        s[index] = char

        return "".join(s)
