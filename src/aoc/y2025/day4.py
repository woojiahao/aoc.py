from typing import Any, List, Tuple

from ..solution import Solution

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


class Y2025Day4(Solution):
    def parse_data(self, contents: str) -> Any:
        grid = []
        for line in contents.strip().split("\n"):
            row = list(line)
            grid.append(row)
        return grid

    def solve_one(self, data: List[List[str]]) -> Any:
        accessible, _ = self.__remove_accessible__(data)
        return accessible

    def solve_two(self, data: Any) -> Any:
        accessible_removed = 0
        self.__toposort__(data)
        while True:
            cur_accessible, new_grid = self.__remove_accessible__(data)
            if cur_accessible == 0:
                break
            accessible_removed += cur_accessible
            data = new_grid
        return accessible_removed

    def __remove_accessible__(
        self, grid: List[List[str]]
    ) -> Tuple[int, List[List[str]]]:
        m, n = len(grid), len(grid[0])
        accessible = 0
        new_grid = [["."] * n for _ in range(m)]
        for r in range(m):
            for c in range(n):
                if grid[r][c] == "@":
                    neighbors = 0
                    for dr, dc in DIRS:
                        nr, nc = r + dr, c + dc
                        in_grid = 0 <= nr < m and 0 <= nc < n
                        if in_grid and grid[nr][nc] == "@":
                            neighbors += 1
                    if neighbors < 4:
                        accessible += 1
                    else:
                        new_grid[r][c] = "@"
        return accessible, new_grid

    def __toposort__(self, data: List[List[str]]) -> int:
        m, n = len(data), len(data[0])
        graph = {}
        for r in range(m):
            for c in range(n):
                graph[(r, c)] = {"in": 0, "out": set()}

        for r in range(m):
            for c in range(n):
                if data[r][c] == "@":
                    for dr, dc in DIRS:
                        nr, nc = r + dr, c + dc
                        in_grid = 0 <= nr < m and 0 <= nc < n
                        if not in_grid:
                            continue
                        graph[(nr, nc)]["in"] += 1
                        graph[(r, c)]["in"] += 1
                        graph[(nr, nc)]["out"].add((r, c))
                        graph[(r, c)]["out"].add((nr, nc))

        frontier = []
        for r in range(m):
            for c in range(n):
                if graph[(r, c)]["in"] < 4:
                    frontier.append((r, c))

        removed = 0
        while frontier:
            new_frontier = []
            for r, c in frontier:
                for nr, nc in graph[(r, c)]["out"]:
                    graph[(nr, nc)]["out"].discard((r, c))
                    if len(graph[(nr, nc)]["out"]) < 4:
                        new_frontier.append((nr, nc))
            removed += len(frontier)
            frontier = new_frontier

        return removed
