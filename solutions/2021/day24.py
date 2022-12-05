from utils.abstract import FileReaderSolution
from abc import abstractmethod
from enum import Enum


class Day24:
    registers = {}
    pointer = 0
    instruction = []
    inputs_read = 0
    inputs = []
    input_pointer = 0

    def __init__(self):
        self.instructions = []
        self.reset()

    def reset(self):
        self.registers = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0
        }
        self.pointer = 0
        self.inputs_read = 0
        self.inputs = []
        self.input_pointer = 0

    @abstractmethod
    def solve_part(self):
        pass

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        return self.solve_part()

    def parse_input(self, input_data: str):
        self.instructions = input_data.splitlines()

    def common_solver(self):
        pass

    def execute_instruction(self):
        instruction = self.instructions[self.pointer]

        instr, a, *b = instruction.split(" ")
        #print(instr, a, b)
        if len(b) > 0:
            if b[0].isnumeric() or b[0][0] == "-":
                b = int(b[0])
            else:
                b = self.registers[b[0]]

        if instr == "inp":
            self.registers[a] = self.inputs[self.input_pointer]
            self.input_pointer += 1
            self.inputs_read += 1
        elif instr == "mul":
            self.registers[a] *= b
        elif instr == "add":
            self.registers[a] += b
        elif instr == "mod":
            self.registers[a] %= b
        elif instr == "div":
            self.registers[a] = int(self.registers[a] / b)
        elif instr == "eql":
            self.registers[a] = 1 if self.registers[a] == b else 0

        else:
            raise Exception(f"Unknown instruction {instruction} at line: {self.pointer}")

        self.pointer += 1
        return instruction


class Day24PartA(Day24, FileReaderSolution):
    def solve_part(self) -> int:
        # 01234567890123
        # 00000000000009
        possibilities = {
            "0": [1],
            "1": [1],
            "2": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            "3": [1],
            "4": [9],
            "5": [2],
            "6": [1],
            "7": [1],
            "8": [8],
            "9": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            "10": [1, 6]
        }

        lowest = 9999999999999999
        for x in range(1, 10):
            self.reset()
            self.inputs = [1, 1, 1, 9, 9, 2, 1, 1, 8, 1, 1, 7, 5, 5]
            self.inputs[0] = x

            while self.pointer < len(self.instructions):
                instr = self.execute_instruction()
                #if self.pointer == 18:

            if self.registers["z"] < lowest:
                lowest = self.registers["z"]
                lowest_digit = x
            print(self.inputs, self.registers["z"])
        print(lowest_digit, lowest)

class Day24PartB(Day24, FileReaderSolution):
    def solve_part(self) -> int:
        pass

