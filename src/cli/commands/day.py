import importlib
from typing import Literal, Optional, Union

import click
from aoc.solution import Solution


@click.command
@click.argument("year")
@click.argument("day")
@click.option(
    "--part", default=None, help="specify either part 1 or 2, defaults to running both"
)
@click.option(
    "--test",
    default=False,
    is_flag=True,
    help="run solution against test data instead of live data",
)
def day(year: int, day: int, part: Optional[str], test: bool):
    module_name = f"aoc.y{year}.day{day}"
    solution_class_name = f"Y{year}Day{day}"

    module = importlib.import_module(module_name)
    SolutionClass = getattr(module, solution_class_name)

    solution: Solution = SolutionClass(year=year, day=day)
    solve_type: Union[Literal["live"], Literal["test"]] = "test" if test else "live"
    print(f"===== Advent of Code {year} Day {day} =====")
    if part is None or part == "1":
        print(f"Part one: {solution.part_one(solve_type)}")
    if part is None or part == "2":
        print(f"Part two: {solution.part_two(solve_type)}")
    print(f"===== Advent of Code {year} Day {day} =====")
