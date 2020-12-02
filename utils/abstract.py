from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union


class AbstractSolution(ABC):
    @abstractmethod
    def solve(self, input_data: str) -> Union[str, int]:
        raise NotImplementedError


class FileReaderSolution(AbstractSolution, ABC):

    def __call__(self, input_file: str) -> Union[str, int]:
        root_dir = Path(__file__).parent.parent
        with open(root_dir / "solutions" / "data" / input_file) as f:
            input_data = f.read()
            res = self.solve(input_data=input_data)
            return res
