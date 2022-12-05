from solutions.tools.HandHeld import HandHeld


class Instruction:
    def execute(self, handheld: HandHeld, argument=None):
        raise NotImplementedError
