from functools import cache
from typing import Any, Dict, List

from ..solution import Solution


class Y2025Day11(Solution):
    def parse_data(self, contents: str) -> Any:
        graph = {}
        for line in contents.strip().split("\n"):
            [input, outputs_raw] = line.split(": ")
            graph[input] = outputs_raw.split(" ")
        return graph

    def solve_one(self, data: Dict[str, List[str]]) -> Any:
        def paths(node: str) -> int:
            if node == "out":
                return 1
            return sum(paths(output) for output in data[node])

        return paths("you")

    def solve_two(self, data: Dict[str, List[str]]) -> Any:
        @cache
        def paths(node: str, dac: bool, fft: bool) -> int:
            if node == "out":
                return int(dac and fft)

            return sum(
                paths(output, output == "dac" or dac, output == "fft" or fft)
                for output in data[node]
            )

        return paths("svr", False, False)
