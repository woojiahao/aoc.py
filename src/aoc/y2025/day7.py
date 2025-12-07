from typing import Any, List, Set, Tuple

from ..solution import Solution
from ..utils.spatial import RCCoord
from functools import cache


class Y2025Day7(Solution):
    def parse_data(self, contents: str) -> Any:
        tr, tc = -1, -1
        splitters: Set[RCCoord] = set()
        rows, cols = 0, 0
        for line in contents.strip().split("\n"):
            for c, cell in enumerate(line):
                if cell == "S":
                    tr, tc = rows, c
                elif cell == "^":
                    splitters.add((rows, c))
            cols = len(line)
            rows += 1
        return (tr, tc), splitters, rows, cols

    def solve_one(self, data: Tuple[RCCoord, Set[RCCoord], int, int]) -> Any:
        (tr, tc), splitters, rows, cols = data

        splits = 0

        @cache
        def dfs(r: int, c: int) -> None:
            nonlocal splits
            if not 0 <= r < rows or not 0 <= c < cols:
                return

            if (r + 1, c) in splitters:
                splits += 1
                dfs(r + 1, c - 1)
                dfs(r + 1, c + 1)
            else:
                dfs(r + 1, c)

        dfs(tr, tc)
        return splits

    def solve_two(self, data: Tuple[RCCoord, Set[RCCoord], int, int]) -> Any:
        (tr, tc), splitters, rows, cols = data

        @cache
        def dfs(r: int, c: int) -> int:
            if r >= rows:
                return 1

            if not 0 <= r < rows or not 0 <= c < cols:
                return 0

            if (r + 1, c) in splitters:
                return dfs(r + 1, c - 1) + dfs(r + 1, c + 1)
            else:
                return dfs(r + 1, c)

        return dfs(tr, tc)
