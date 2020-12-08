from utils.abstract import FileReaderSolution
import re


class Day08:
    pointer: int = 0
    accumulator: int = 0
    history: {}
    instructions: []
    looped: bool

    def initialize(self, input_data):
        self.looped = False
        self.instructions = input_data.split("\n")
        self.history = {}
        self.accumulator = 0
        self.pointer = 0

    def run(self, input_data: str):
        self.initialize(input_data)

        running = True
        counter = 1

        while running:
            if self.pointer >= len(self.instructions)-1:
                running = False

            if self.pointer not in self.history.keys():
                self.history[self.pointer] = []

            self.history[self.pointer].append(counter)

            if self.should_stop_running():
                self.looped = True
                break

            self.run_instruction(self.pointer)
            self.pointer += 1

            counter += 1

    def run_instruction(self, pointer):
        instruction_str = self.instructions[pointer]
        result = re.match(r'([a-z]*) ([+-]\d*)', instruction_str)

        assert result

        opcode = result[1]
        number = int(result[2])

        if opcode == "nop":
            self.instruction_nop()
        elif opcode == "acc":
            self.instruction_acc(number)
        elif opcode == "jmp":
            self.instruction_jmp(number)
        else:
            raise Exception("Unknown opcode %s on line %s"%(opcode, pointer))

    def instruction_jmp(self, number):
        self.pointer += number - 1

    def instruction_nop(self):
        return

    def instruction_acc(self, number):
        self.accumulator += number

    def should_stop_running(self):
        for key in self.history.keys():
            if len(self.history[key]) > 1:
                return True

        return False


class Day08PartA(Day08, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.run(input_data)

        return self.accumulator


class Day08PartB(Day08, FileReaderSolution):
    last_line_changed: int;

    def solve(self, input_data: str) -> int:
        self.last_line_changed = -1

        exited_normally = False
        original_input_data = input_data

        while not exited_normally:
            self.run(input_data)

            if not self.looped:
                exited_normally = True
            else:
                input_data = self.fix_program(original_input_data)

        return self.accumulator

    def fix_program(self, input_data):
        lines = input_data.split("\n")
        changed = False
        for i in range(max(0, self.last_line_changed+1), len(lines)):
            line = lines[i]

            result = re.match(r'([a-z]*) ([+-]\d*)', line)
            assert result

            if result[1] == "jmp":
                lines[i] = line.replace("jmp", "nop")
                self.last_line_changed = i
                changed = True
                break
            elif result[1] == "nop":
                lines[i] = line.replace("nop", "jmp")
                changed = True
                self.last_line_changed = i
                break

        if not changed:
            print("No more to change.... No solution found")
            exit()

        return "\n".join(lines)
