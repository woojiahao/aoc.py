import abc
from dataclasses import dataclass
from typing import Any, Literal, Union

import click

TYPE = Union[Literal["live", "test"]]


@dataclass
class Solution(abc.ABC):
    year: int
    day: int

    def load_data(self, type: TYPE) -> str:
        suffix = "-test" if type == "test" else ""
        with open(f"data/y{self.year}/day{self.day}{suffix}.txt", "r") as f:
            contents = f.read().strip()
        return contents

    @abc.abstractmethod
    def parse_data(self, contents: str) -> Any:
        pass

    @abc.abstractmethod
    def solve_one(self, data: Any) -> Any:
        pass

    @abc.abstractmethod
    def solve_two(self, data: Any) -> Any:
        pass

    def part_one(self, type: TYPE) -> Any:
        data = self.load_data(type)
        parsed_data = self.parse_data(data)
        return self.solve_one(parsed_data)

    def part_two(self, type: TYPE) -> Any:
        data = self.load_data(type)
        parsed_data = self.parse_data(data)
        return self.solve_two(parsed_data)

    def is_test_mode(self) -> bool:
        return click.get_current_context().obj["test"]
