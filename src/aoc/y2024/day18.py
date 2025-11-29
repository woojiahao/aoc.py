from collections import deque
from typing import Any, List, Set, Tuple

from ..solution import Solution
from ..utils.spatial import RCCoord, XYCoord


class Y2024Day18(Solution):
    def parse_data(self, contents: str) -> Any:
        memory: List[XYCoord] = []
        for line in contents.strip().split("\n"):
            [C, R] = [int(v) for v in line.split(",")]
            memory.append((R, C))
        return memory

    def solve_one(self, data: List[RCCoord]) -> Any:
        return self.__find_shortest_path__(data[:1024])

    def solve_two(self, data: Any) -> Any:
        l, r = 0, len(data) - 1
        while l < r:
            m = l + (r - l) // 2
            if self.__find_shortest_path__(data[: m + 1]) == -1:
                r = m
            else:
                l = m + 1
        return data[l][::-1]

    def __find_shortest_path__(self, data: List[RCCoord]):
        walls = set(data)

        q = deque([(0, 0, 0)])
        visited: Set[RCCoord] = set()
        grid_size = self.__get_grid_size__()
        while q:
            row, col, steps = q.popleft()
            if (row, col) == (grid_size - 1, grid_size - 1):
                return steps

            if (row, col) in visited:
                continue

            visited.add((row, col))
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                if (
                    (nr, nc) not in walls
                    and 0 <= nr < grid_size
                    and 0 <= nc < grid_size
                ):
                    q.append((nr, nc, steps + 1))

        return -1

    def __get_grid_size__(self):
        return 7 if self.is_test_mode() else 71
