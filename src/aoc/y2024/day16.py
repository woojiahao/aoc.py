import heapq
from collections import deque
from math import inf
from typing import Any, Dict, List, Set, Tuple

from ..solution import Solution
from ..utils.spatial import RCCoord

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Y2024Day16(Solution):
    def parse_data(self, contents: str) -> Any:
        start_r, start_c = -1, -1
        end_r, end_c = -1, -1
        rows, cols = 0, 0
        walls = set()
        r = 0
        for line in contents.strip().split("\n"):
            cols = len(line)
            for c, ch in enumerate(line):
                if ch == "S":
                    start_r, start_c = r, c
                elif ch == "E":
                    end_r, end_c = r, c
                elif ch == "#":
                    walls.add((r, c))
            r += 1
            rows += 1
        return (start_r, start_c), (end_r, end_c), walls, rows, cols

    def solve_one(
        self, data: Tuple[RCCoord, RCCoord, Set[Tuple[RCCoord]], int, int]
    ) -> Any:
        start, end, walls, rows, cols = data
        ans = self.__walk__(walls, start, end, rows, cols)
        return ans

    def solve_two(self, data: Any) -> Any:
        start, end, walls, rows, cols = data
        ans = self.__walk_2__(walls, start, end, rows, cols)
        return ans

    def __walk__(
        self,
        walls: Set[Tuple[RCCoord]],
        start: RCCoord,
        end: RCCoord,
        rows: int,
        cols: int,
    ):
        q = deque([(start, 0, 0)])
        scores = [[10**10] * cols for _ in range(rows)]
        while q:
            (r, c), d, score = q.popleft()
            for move, add_score in ((0, 1), (-1, 1001), (1, 1001)):
                new_d = (d + move) % 4
                dr, dc = DIRECTIONS[new_d]
                nr, nc = r + dr, c + dc
                in_grid = 0 <= nr < rows and 0 <= nc < cols
                if not in_grid or (nr, nc) in walls:
                    continue
                new_score = score + add_score
                if scores[nr][nc] > new_score:
                    scores[nr][nc] = new_score
                    q.append(((nr, nc), new_d, new_score))
        return scores[end[0]][end[1]]

    def __walk_2__(
        self,
        walls: Set[RCCoord],
        start: RCCoord,
        end: RCCoord,
        rows: int,
        cols: int,
    ):
        q = deque([(start, 0, 0)])
        scores = [[10**10] * cols for _ in range(rows)]
        while q:
            (r, c), d, score = q.popleft()
            for move, add_score in ((0, 1), (-1, 1001), (1, 1001)):
                new_d = (d + move) % 4
                dr, dc = DIRECTIONS[new_d]
                nr, nc = r + dr, c + dc
                in_grid = 0 <= nr < rows and 0 <= nc < cols
                if not in_grid or (nr, nc) in walls:
                    continue
                new_score = score + add_score
                if scores[nr][nc] > new_score:
                    scores[nr][nc] = new_score
                    q.append(((nr, nc), new_d, new_score))

        q = deque([(end, 1, scores[end[0]][end[1]]), (end, 2, scores[end[0]][end[1]])])
        visited = set()
        ans = 2

        while q:
            (r, c), d, score = q.popleft()

            for move, add_score in ((0, -1), (-1, -1001), (1, -1001)):
                new_d = (d + move) % 4
                dr, dc = DIRECTIONS[new_d]
                nr, nc = r + dr, c + dc
                in_grid = 0 <= nr < rows and 0 <= nc < cols
                if not in_grid or (nr, nc) in walls:
                    continue
                new_score = score + add_score
                if (
                    scores[nr][nc] in [new_score, new_score - 1000]
                    and (nr, nc) not in visited
                ):
                    visited.add((nr, nc))
                    q.append(((nr, nc), new_d, new_score))
                    ans += 1
        return ans

    def __print_map__(
        self, walls: Set[RCCoord], rows: int, cols: int, path_points: Set[RCCoord]
    ) -> None:
        for r in range(rows):
            line = []
            for c in range(cols):
                if (r, c) in walls:
                    line.append("#")
                elif (r, c) in path_points:
                    line.append("O")
                else:
                    line.append(".")
            print("".join(line))
