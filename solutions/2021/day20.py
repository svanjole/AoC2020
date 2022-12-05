import string

from utils.abstract import FileReaderSolution
from abc import abstractmethod
import numpy as np


class Day20:

    image: None
    algo: string

    @abstractmethod
    def solve_part(self):
        pass

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        return self.solve_part()

    def parse_input(self, input_data: str):
        data = input_data.split("\n\n")
        self.algo = list(map(lambda x: 1 if x == "#" else 0, data[0]))

        imagedata = data[1].split()
        height = len(imagedata)
        width = len(imagedata[0])

        self.image = np.zeros((width, height), dtype=int)

        for y in range(height):
            for x in range(width):
                self.image[y][x] = 1 if imagedata[y][x] == "#" else 0



    def common_solver(self):
        pass

    def iteration(self, steps):
        #self.image = np.pad(self.image, 1, mode='constant')
        boundary = 0
        for s in range(steps):
            h, w = np.shape(self.image)
            new_image = np.zeros((h + 2, w +2), dtype=int)

            for y in range(-1, h + 1):
                for x in range(-1, w + 1):
                    pos = 0
                    for dy in range(y-1, y+2):
                        for dx in range(x-1, x+2):
                            pos <<= 1
                            if 0 <= dy < h and 0 <= dx < w:
                                pos += self.image[dy, dx]
                            else:
                                pos += boundary

                    new_image[y+1, x+1] = self.algo[pos]
            self.image = new_image

            if boundary == 0:
                boundary = self.algo[0]
            else:
                boundary = self.algo[-1]


class Day20PartA(Day20, FileReaderSolution):
    def solve_part(self) -> int:
        self.iteration(2)
        return np.count_nonzero(self.image)


class Day20PartB(Day20, FileReaderSolution):
    def solve_part(self) -> int:
        self.iteration(50)
        return np.count_nonzero(self.image)

