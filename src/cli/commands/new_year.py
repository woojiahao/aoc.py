import os
import textwrap

import click


@click.command
@click.argument("year")
@click.argument("days")
def new_year(year, days):
    data_folder_name = f"data/y{year}"
    os.makedirs(data_folder_name)
    os.chdir(data_folder_name)
    for i in range(1, days + 1):
        with open(f"day{i}.txt", "w") as _:
            ...
        with open(f"day{i}-test.txt", "w") as _:
            ...

    os.chdir("../..")

    solution_folder_name = f"src/aoc/y{year}"
    os.makedirs(solution_folder_name)
    os.chdir(solution_folder_name)

    for i in range(1, days + 1):
        with open(f"day{i}.py", "w") as f:
            f.write(
                textwrap.dedent(f"""
from typing import Any, List, Tuple

from ..solution import Solution


class Y{year}Day{i}(Solution):
    def parse_data(self, contents: str) -> Any:
        for line in contents.strip().split("\n"):
            pass
        return

    def solve_one(self, data: Any) -> Any:
        pass

    def solve_two(self, data: Any) -> Any:
        pass
            """)
            )
