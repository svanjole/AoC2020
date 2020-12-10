from solutions.tools.HandHeld import HandHeld
from solutions.tools.Instruction import Instruction


class NOP(Instruction):
    @staticmethod
    def execute(handheld: HandHeld, argument=None):
        handheld.pointer += 1
        pass
