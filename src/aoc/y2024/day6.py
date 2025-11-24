from typing import Any, List, Set, Tuple
import sys

from ..solution import Solution

sys.setrecursionlimit(10**5)


class Y2024Day5(Solution):
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def parse_data(self, contents: str) -> Any:
        grid = []
        r = 0
        sr, sc = -1, -1
        for line in contents.strip().split("\n"):
            row = list(line)
            for c in range(len(row)):
                if row[c] == "^":
                    sr, sc = r, c
            grid.append(row)
            r += 1
        return grid, sr, sc

    def solve_one(self, data: Tuple[List[List[str]], int, int]) -> Any:
        grid, sr, sc = data
        visited: Set[Tuple[int, int]] = set()
        self.__walk__(grid, sr, sc, 0, visited)
        self.__print_grid__(grid, visited)
        return len(visited)

    def solve_two(self, data: Tuple[List[List[str]], int, int]) -> Any:
        grid, sr, sc = data
        all_walked: Set[Tuple[int, int]] = set()
        self.__walk__(grid, sr, sc, 0, all_walked)
        ans = 0
        for r, c in all_walked:
            grid[r][c] = "#"
            ans += self.__walk_2__(grid, sr, sc, 0, set())
            grid[r][c] = "."
        return ans

    def __walk_2__(
        self,
        grid: List[List[str]],
        r: int,
        c: int,
        d: int,
        visited: Set[Tuple[int, int, int]],
    ) -> int:
        if (r, c, d) in visited:
            return 1

        visited.add((r, c, d))
        dr, dc = self.moves[d]
        nr, nc = r + dr, c + dc

        if not 0 <= nr < len(grid) or not 0 <= nc < len(grid[0]):
            return 0

        if grid[nr][nc] == "#":
            return self.__walk_2__(grid, r, c, (d + 1) % 4, visited)
        else:
            return self.__walk_2__(grid, nr, nc, d, visited)

    def __walk__(
        self,
        grid: List[List[str]],
        r: int,
        c: int,
        d: int,
        visited: Set[Tuple[int, int]],
    ) -> None:
        visited.add((r, c))
        dr, dc = self.moves[d]
        nr, nc = r + dr, c + dc

        if not 0 <= nr < len(grid) or not 0 <= nc < len(grid[0]):
            return

        if grid[nr][nc] == "#":
            self.__walk__(grid, r, c, (d + 1) % 4, visited)
        else:
            self.__walk__(grid, nr, nc, d, visited)

    def __print_grid__(
        self, grid: List[List[str]], visited: Set[Tuple[int, int]]
    ) -> None:
        for r in range(len(grid)):
            row = []
            for c in range(len(grid[0])):
                if (r, c) in visited:
                    row.append("X")
                else:
                    row.append(grid[r][c])
            print("".join(row))
