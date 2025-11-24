from typing import Any, List, Tuple

from ..solution import Solution


class Y2024Day4(Solution):
    def parse_data(self, contents: str) -> Any:
        grid = []
        for line in contents.strip().split("\n"):
            row = list(line)
            grid.append(row)
        return grid

    def solve_one(self, data: List[List[str]]) -> Any:
        ans = 0
        for i in range(len(data)):
            for j in range(len(data[0])):
                dirs = [
                    (0, 1),
                    (0, -1),
                    (1, 0),
                    (-1, 0),
                    (1, 1),
                    (-1, -1),
                    (1, -1),
                    (-1, 1),
                ]
                for dr, dc in dirs:
                    ans += self.__has_xmas__(data, i, j, dr, dc, 0)
        return ans

    def solve_two(self, data: Any) -> Any:
        ans = 0
        for i in range(1, len(data) - 1):
            for j in range(1, len(data[0]) - 1):
                if data[i][j] == "A":
                    diagonal_one = (
                        data[i - 1][j - 1] == "M" and data[i + 1][j + 1] == "S"
                    ) or (data[i - 1][j - 1] == "S" and data[i + 1][j + 1] == "M")
                    diagonal_two = (
                        data[i - 1][j + 1] == "M" and data[i + 1][j - 1] == "S"
                    ) or (data[i - 1][j + 1] == "S" and data[i + 1][j - 1] == "M")
                    if diagonal_one and diagonal_two:
                        ans += 1
        return ans

    def __has_xmas__(
        self, grid: List[List[str]], r: int, c: int, dr: int, dc: int, expected: int
    ) -> bool:
        if expected >= 4:
            return True
        if (
            not 0 <= r < len(grid)
            or not 0 <= c < len(grid[0])
            or "XMAS"[expected] != grid[r][c]
        ):
            return False
        acc = False
        nr, nc = r + dr, c + dc
        acc |= self.__has_xmas__(grid, nr, nc, dr, dc, expected + 1)
        return acc
