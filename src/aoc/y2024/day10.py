from typing import Any, List, Tuple, Set
from typing_extensions import final

from ..solution import Solution


class Y2024Day10(Solution):
    def parse_data(self, contents: str) -> Any:
        grid = []
        trailheads = []
        r = 0
        for line in contents.strip().split("\n"):
            row = []
            for c in range(len(line)):
                if line[c] == "0":
                    trailheads.append((r, c))
                if line[c] == ".":
                    row.append(-1)
                else:
                    row.append(int(line[c]))
            grid.append(row)
            r += 1
        return grid, trailheads

    def solve_one(self, data: Tuple[List[List[int]], List[Tuple[int, int]]]) -> Any:
        grid, trailheads = data
        scores = 0
        for r, c in trailheads:
            scores += self.__walk__(grid, r, c, set())
        return scores

    def solve_two(self, data: Any) -> Any:
        grid, trailheads = data
        rating = 0
        for r, c in trailheads:
            rating += self.__walk_2__(grid, r, c)
        return rating

    def __walk__(
        self, grid: List[List[int]], r: int, c: int, visited: Set[Tuple[int, int]]
    ) -> int:
        n, m = len(grid), len(grid[0])
        visited.add((r, c))
        if grid[r][c] == 9:
            return 1
        ways = 0
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            in_grid = 0 <= nr < n and 0 <= nc < m
            if in_grid and grid[nr][nc] - grid[r][c] == 1 and (nr, nc) not in visited:
                ways += self.__walk__(grid, nr, nc, visited)
        return ways

    def __walk_2__(self, grid: List[List[int]], r: int, c: int) -> int:
        n, m = len(grid), len(grid[0])
        if grid[r][c] == 9:
            return 1
        ways = 0
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            in_grid = 0 <= nr < n and 0 <= nc < m
            if in_grid and grid[nr][nc] - grid[r][c] == 1:
                ways += self.__walk_2__(grid, nr, nc)
        return ways
