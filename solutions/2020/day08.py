from utils.abstract import FileReaderSolution
from solutions.tools.HandHeld import HandHeld
import re


class Day08:
    pass


class Day08PartA(Day08, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        handheld = HandHeld()
        handheld.run(input_data)

        return handheld.accumulator


class Day08PartB(Day08, FileReaderSolution):
    last_line_changed: int;

    def solve(self, input_data: str) -> int:
        self.last_line_changed = -1

        exited_normally = False
        original_input_data = input_data
        handheld = HandHeld()

        while not exited_normally:

            handheld.run(input_data)

            if not handheld.looped:
                exited_normally = True
            else:
                input_data = self.fix_program(original_input_data)

        return handheld.accumulator

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
