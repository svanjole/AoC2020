from solutions.tools.HandHeld import HandHeld
from solutions.tools.Instruction import Instruction


class JMP(Instruction):

    @staticmethod
    def execute(handheld: HandHeld, argument=None):
        handheld.pointer += int(argument)
        pass
