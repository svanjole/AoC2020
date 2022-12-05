from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union


class FileReaderSolution(ABC):
    @abstractmethod
    def solve(self, input_data: str) -> Union[str, int]:
        raise NotImplementedError

    def __call__(self, input_file: str) -> Union[str, int]:
        root_dir = Path(__file__).parent.parent
        with open(root_dir / input_file) as f:
            input_data = f.read()
            res = self.solve(input_data=input_data)
            return res


class TestSolution(ABC):
    @abstractmethod
    def run_tests(self):
        raise NotImplementedError

    def __call__(self):
        self.run_tests()

