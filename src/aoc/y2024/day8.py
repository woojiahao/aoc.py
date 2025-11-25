from itertools import combinations
from typing import Any, List, Set, Tuple

from aoc.utils.math import sign

from ..solution import Solution


class Y2024Day8(Solution):
    def parse_data(self, contents: str) -> Any:
        grid = []
        antenna_positions = set()
        r = 0
        for line in contents.strip().split("\n"):
            row = list(line)
            for c in range(len(row)):
                if row[c] != ".":
                    antenna_positions.add((r, c))
            grid.append(row)
            r += 1
        return grid, sorted(antenna_positions)

    def solve_one(self, data: Tuple[List[List[str]], Set[Tuple[int, int]]]) -> Any:
        grid, antenna_positions = data
        n, m = len(grid), len(grid[0])
        distinct_pairs = list(combinations(antenna_positions, 2))
        antinodes = set()
        # Given that we sort the antennas by (r, c), a will always occur row-wise
        # before b
        # There are then two positions we can be in: either b is before or after a
        # column-wise
        # If b comes before a column-wise, then we have m = 1 where m is the gradient
        # If b comes after a column-wise, then we have m = -1 where m is the gradient
        # If b is in the same column as a, then we have m = 0 where m is the gradient
        for [(ar, ac), (br, bc)] in distinct_pairs:
            if grid[ar][ac] != grid[br][bc]:
                # Not the same antenna frequency
                continue

            r_dist = abs(ar - br)
            c_dist = abs(ac - bc)
            g = -sign(ac - bc)
            first_antinode = (ar - r_dist, ac - g * c_dist)
            if 0 <= first_antinode[0] < n and 0 <= first_antinode[1] < m:
                antinodes.add(first_antinode)

            second_antinode = (ar + 2 * r_dist, ac + 2 * g * c_dist)
            if 0 <= second_antinode[0] < n and 0 <= second_antinode[1] < m:
                antinodes.add(second_antinode)
        self.__print_grid__(grid, antinodes)
        return len(antinodes)

    def solve_two(self, data: Tuple[List[List[str]], Set[Tuple[int, int]]]) -> Any:
        grid, antenna_positions = data
        n, m = len(grid), len(grid[0])
        distinct_pairs = list(combinations(antenna_positions, 2))
        antinodes = set()
        # Given that we sort the antennas by (r, c), a will always occur row-wise
        # before b
        # There are then two positions we can be in: either b is before or after a
        # column-wise
        # If b comes before a column-wise, then we have m = 1 where m is the gradient
        # If b comes after a column-wise, then we have m = -1 where m is the gradient
        # If b is in the same column as a, then we have m = 0 where m is the gradient

        def in_grid(r, c):
            return 0 <= r < n and 0 <= c < m

        for [(ar, ac), (br, bc)] in distinct_pairs:
            if grid[ar][ac] != grid[br][bc]:
                # Not the same antenna frequency
                continue

            r_dist = abs(ar - br)
            c_dist = abs(ac - bc)
            g = -sign(ac - bc)
            first_factor = 0

            def first_antinode(factor):
                return (ar - factor * r_dist, ac - g * factor * c_dist)

            while in_grid(*first_antinode(first_factor)):
                print(first_antinode(first_factor))
                antinodes.add(first_antinode(first_factor))
                first_factor += 1

            def second_antinode(factor):
                return (ar + factor * r_dist, ac + g * factor * c_dist)

            second_factor = 1
            while in_grid(*second_antinode(second_factor)):
                antinodes.add(second_antinode(second_factor))
                second_factor += 1

        self.__print_grid__(grid, antinodes)
        return len(antinodes)

    def __print_grid__(
        self, grid: List[List[str]], antinodes: Set[Tuple[int, int]]
    ) -> None:
        n, m = len(grid), len(grid[0])
        for i in range(n):
            row = []
            for j in range(m):
                if grid[i][j] != ".":
                    row.append(grid[i][j])
                elif (i, j) in antinodes:
                    row.append("#")
                else:
                    row.append(grid[i][j])
            print("".join(row))
