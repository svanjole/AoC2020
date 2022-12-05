from solutions.tools.HandHeld import HandHeld
from solutions.tools.Instruction import Instruction


class ACC(Instruction):
    @staticmethod
    def execute(handheld: HandHeld, argument=None):
        handheld.accumulator += int(argument)
        handheld.pointer += 1
