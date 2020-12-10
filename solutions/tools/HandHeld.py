import importlib
import sys
import re


class HandHeld:
    pointer: int = 0
    accumulator: int = 0
    history: {}
    program: []
    looped: bool
    instructions: {}

    def __init__(self):
        self.reset()

    def load_program(self, input_data):
        self.program = input_data.split("\n")
        self.reset()

    def reset(self):
        self.looped = False
        self.history = {}
        self.accumulator = 0
        self.pointer = 0

    def run(self, input_data: str):
        self.load_program(input_data)

        running = True
        counter = 1

        while running:
            if self.pointer >= len(self.program)-1:
                running = False

            if self.pointer not in self.history.keys():
                self.history[self.pointer] = []

            self.history[self.pointer].append(counter)

            if self.should_stop_running():
                self.looped = True
                break

            self.run_instruction(self.pointer)

            counter += 1

    def run_instruction(self, pointer):
        instruction_str = self.program[pointer]
        result = re.match(r'([a-z]*) ([+-]\d*)', instruction_str)

        assert result

        opcode = result[1].upper()
        argument = result[2]

        try:
            module = importlib.import_module(f"solutions.tools.instructions.{opcode}")
        except ModuleNotFoundError:
            print(f"instruction {opcode} at line {pointer} is not yet available")
            sys.exit(-65)

        instruction = getattr(module, f"{opcode}")()
        instruction.execute(self, argument)

    def should_stop_running(self):
        for key in self.history.keys():
            if len(self.history[key]) > 1:
                return True

        return False
