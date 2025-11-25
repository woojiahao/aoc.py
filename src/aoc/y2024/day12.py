from typing import Any, List, Set, Tuple
from itertools import product
from collections import deque

from ..solution import Solution


class Y2024Day12(Solution):
    def parse_data(self, contents: str) -> Any:
        grid = []
        for line in contents.strip().split("\n"):
            row = list(line)
            grid.append(row)
        return grid

    def solve_one(self, data: List[List[str]]) -> Any:
        n, m = len(data), len(data[0])
        ans = 0
        visited: Set[Tuple[int, int]] = set()
        for r in range(n):
            for c in range(m):
                if (r, c) in visited:
                    continue
                area, perimeter = 0, 0
                q = deque([(r, c)])
                while q:
                    tr, tc = q.popleft()
                    area += 1
                    matching_neighbors = 0
                    visited.add((r, c))
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = tr + dr, tc + dc
                        in_grid = 0 <= nr < n and 0 <= nc < m
                        if in_grid and data[nr][nc] == data[r][c]:
                            matching_neighbors += 1
                            if (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                    perimeter += 4 - matching_neighbors
                ans += area * perimeter
        return ans

    def solve_two(self, data: Any) -> Any:
        n, m = len(data), len(data[0])
        ans = 0
        visited: Set[Tuple[int, int]] = set()
        for r in range(n):
            for c in range(m):
                if (r, c) in visited:
                    continue
                area = 0
                corners = 0
                points = set()
                q = deque([(r, c)])
                while q:
                    tr, tc = q.popleft()
                    area += 1
                    visited.add((tr, tc))
                    points.add((tr, tc))
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = tr + dr, tc + dc
                        in_grid = 0 <= nr < n and 0 <= nc < m
                        if in_grid and data[nr][nc] == data[r][c]:
                            if (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))

                for point in points:
                    row, col = point
                    for dr, dc in product([1, -1], repeat=2):
                        row_neighbor = (row + dr, col)
                        col_neighbor = (row, col + dc)
                        diag_neighbor = (row + dr, col + dc)

                        if row_neighbor not in points and col_neighbor not in points:
                            corners += 1
                        if (
                            row_neighbor in points
                            and col_neighbor in points
                            and diag_neighbor not in points
                        ):
                            corners += 1

                ans += area * corners
        return ans
