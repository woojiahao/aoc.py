from typing import Any, Dict, List, Set, Tuple

from ..solution import Solution
from ..utils.spatial import RCCoord

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
        total_removed = self.__toposort__(data)
        return total_removed

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
        graph: Dict[RCCoord, Set[RCCoord]] = {}

        for r in range(m):
            for c in range(n):
                if data[r][c] == "@":
                    if (r, c) not in graph:
                        graph[(r, c)] = set()
                    for dr, dc in DIRS:
                        nr, nc = r + dr, c + dc
                        in_grid = 0 <= nr < m and 0 <= nc < n
                        if not in_grid:
                            continue
                        if data[nr][nc] == "@":
                            if (nr, nc) not in graph:
                                graph[(nr, nc)] = set()
                            graph[(nr, nc)].add((r, c))
                            graph[(r, c)].add((nr, nc))

        frontier = []
        for r in range(m):
            for c in range(n):
                if data[r][c] == "@" and len(graph[(r, c)]) < 4:
                    frontier.append((r, c))

        visited = set(frontier)
        while frontier:
            new_frontier = []
            for r, c in frontier:
                for nr, nc in graph[(r, c)]:
                    graph[(nr, nc)].discard((r, c))
                    if len(graph[(nr, nc)]) < 4 and (nr, nc) not in visited:
                        new_frontier.append((nr, nc))
                        visited.add((nr, nc))
            frontier = new_frontier

        return len(visited)
