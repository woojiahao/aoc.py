from collections import defaultdict
from functools import cache
from typing import Any, Dict, List

from ..solution import Solution


class Y2025Day11(Solution):
    def parse_data(self, contents: str) -> Any:
        graph = defaultdict(list)
        for line in contents.strip().split("\n"):
            [input, outputs_raw] = line.split(": ")
            outputs = outputs_raw.split(" ")
            graph[input] = outputs
        return graph

    def solve_one(self, data: Dict[str, List[str]]) -> Any:
        def paths(node: str) -> int:
            if node == "out":
                return 1

            p = 0
            for output in data[node]:
                p += paths(output)
            return p

        return paths("you")

    def solve_two(self, data: Dict[str, List[str]]) -> Any:
        @cache
        def paths(node: str, dac: bool, fft: bool) -> int:
            if node == "out":
                return int(dac and fft)

            p = 0
            for output in data[node]:
                dac_p = output == "dac" or dac
                fft_p = output == "fft" or fft
                p += paths(output, dac_p, fft_p)
            return p

        return paths("svr", False, False)
