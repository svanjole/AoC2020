from utils.abstract import FileReaderSolution


class Day05:
    def solve(self, input_data):
        sections = input_data.split("\n\n")
        config = sections[0].split("\n")

        stacks = [[] for _ in range(int(config[-1].split()[-1]))]

        for line in config[:-1]:
            for pos, crate in enumerate(line.replace("    ", " ").replace("]", "").replace("[", "").split(" ")):
                if crate:
                    stacks[pos].append(crate)

        for move in [[int(x) - 1 for x in move.split(" ") if x.isdigit()] for move in sections[1].split("\n")]:
            crates = stacks[move[1]][:move[0]+1]
            stacks[move[2]][0:0] = crates[::-1] if isinstance(self, Day05PartA) else crates
            del stacks[move[1]][:move[0]+1]

        return ''.join([stack[0] for stack in stacks])


class Day05PartA(Day05, FileReaderSolution):
    pass


class Day05PartB(Day05, FileReaderSolution):
    pass
