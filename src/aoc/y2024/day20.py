from typing import Any, List, Tuple

from ..solution import Solution


class Y2024Day20(Solution):
    def parse_data(self, contents: str) -> Any:
        grid = []
        start_r, start_c = -1, -1
        end_r, end_c = -1, -1
        for line in contents.strip().split("\n"):
            row = []
            r = 0
            for c, cell in enumerate(line):
                if cell == "S":
                    start_r, start_c = r, c
                elif cell == "E":
                    end_r, end_c = r, c
                elif cell == "#":
                    row.append("#")
                    continue
                row.append(".")
            r += 1
            grid.append(row)

        return grid, (start_r, start_c), (end_r, end_c)

    def solve_one(self, data: Any) -> Any:
        pass

    def solve_two(self, data: Any) -> Any:
        pass
