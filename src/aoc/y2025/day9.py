from typing import Any, Dict, List, Set, Tuple

from aoc.utils.spatial import RCCoord, XYCoord
from collections import defaultdict, deque

from ..solution import Solution


class Y2025Day9(Solution):
    def parse_data(self, contents: str) -> Any:
        red_tiles = []
        for line in contents.strip().split("\n"):
            [x, y] = [int(v) for v in line.split(",")]
            red_tiles.append((x, y))
        return red_tiles

    def solve_one(self, data: List[XYCoord]) -> Any:
        n = len(data)
        ans = 0
        for i in range(n):
            for j in range(i + 1, n):
                w = abs(data[i][1] - data[j][1]) + 1
                h = abs(data[i][0] - data[j][0]) + 1
                ans = max(ans, w * h)
        return ans

    def solve_two(self, data: List[XYCoord]) -> Any:
        return self.__flood_fill_solve__(data)
        return self.__polygon_solve__(data)

    def __flood_fill_solve__(self, data: List[XYCoord]) -> int:
        x_coords = sorted({p[0] for p in data})
        y_coords = sorted({p[1] for p in data})
        compressed_x = {x: i for i, x in enumerate(x_coords)}
        compressed_y = {y: i for i, y in enumerate(y_coords)}

        H, W = len(y_coords), len(x_coords)
        grid = [["."] * W for _ in range(H)]

        for i in range(len(data)):
            a, b = data[i], data[(i + 1) % len(data)]
            ax = compressed_x[a[0]]
            ay = compressed_y[a[1]]
            bx = compressed_x[b[0]]
            by = compressed_y[b[1]]
            grid[ay][ax] = "X"
            grid[by][bx] = "X"

            if ax == bx:
                start_y, end_y = min(ay, by), max(ay, by)
                for y in range(start_y + 1, end_y):
                    grid[y][ax] = "#"
            else:
                start_x, end_x = min(ax, bx), max(ax, bx)
                for x in range(start_x + 1, end_x):
                    grid[ay][x] = "#"

        for y in range(1, H - 1):
            row = grid[y]
            above = grid[y - 1]
            in_section = False

            for x in range(W):
                top = above[x]
                current = row[x]

                if current in ("X", "#") and top in ("X", "#"):
                    in_section = not in_section
                elif in_section:
                    if all(c not in ("X", "#") for c in row[x + 1 :]):
                        in_section = False
                    else:
                        row[x] = "*"
                else:
                    if (
                        top in ("X", "#")
                        and sum(c in ("X", "#") for c in row[x + 1 :]) == 1
                    ):
                        in_section = False
                        row[x] = "*"

        ans = 0

        for i in range(len(data)):
            ax = compressed_x[data[i][0]]
            ay = compressed_y[data[i][1]]

            for j in range(i + 1, len(data)):
                bx = compressed_x[data[j][0]]
                by = compressed_y[data[j][1]]

                width = abs(data[i][0] - data[j][0]) + 1
                height = abs(data[i][1] - data[j][1]) + 1
                area = height * width

                if area < ans:
                    continue

                start_x, end_x = min(ax, bx), max(ax, bx)
                start_y, end_y = min(ay, by), max(ay, by)

                ok = True
                for y in range(start_y, end_y + 1):
                    for x in range(start_x, end_x + 1):
                        if grid[y][x] == ".":
                            ok = False
                            break
                    if not ok:
                        break

                if ok:
                    print((ax, ay), (bx, by), data[i], data[j])
                    ans = max(ans, area)

        for row in grid:
            print("".join(row))

        return ans

    def __print_grid__(self, grid: Dict[XYCoord, str]) -> None:
        min_x = min(grid.items(), key=lambda x: x[0][0])[0][0]
        max_x = max(grid.items(), key=lambda x: x[0][0])[0][0]
        min_y = min(grid.items(), key=lambda x: x[0][1])[0][1]
        max_y = max(grid.items(), key=lambda x: x[0][1])[0][1]
        for y in range(min_y, max_y + 1):
            line = []
            for x in range(min_x, max_x + 1):
                if (x, y) in grid:
                    line.append(grid[x, y])
                else:
                    line.append(".")
            print("".join(line))

    def __polygon_solve__(self, data: List[XYCoord]) -> int:
        n = len(data)
        ans = 0
        vertical_lines = []
        horizontal_lines = []
        for i in range(n):
            ax, ay = data[i]
            bx, by = data[(i + 1) % n]

            if ax == bx:
                # Vertical line
                y_start = min(ay, by)
                y_end = max(ay, by)
                vertical_lines.append((ax, y_start, y_end))
            else:
                # Horizontal line
                x_start = min(ax, bx)
                x_end = max(ax, bx)
                horizontal_lines.append((ay, x_start, x_end))

        s_data = set(data)
        for i in range(n):
            for j in range(i + 1, n):
                w = abs(data[i][1] - data[j][1]) + 1
                h = abs(data[i][0] - data[j][0]) + 1
                area = w * h

                if area < ans:
                    continue

                if self.__is_rectangle_valid__(
                    data[i], data[j], s_data, vertical_lines, horizontal_lines
                ):
                    ans = max(ans, w * h)
        return ans

    def __is_rectangle_valid__(
        self,
        a: XYCoord,
        b: XYCoord,
        data: Set[XYCoord],
        vertical_lines: List[Tuple[int, int, int]],
        horizontal_lines: List[Tuple[int, int, int]],
    ) -> bool:
        ax, ay = a
        bx, by = b
        x_min, x_max = min(ax, bx), max(ax, bx)
        y_min, y_max = min(ay, by), max(ay, by)

        corners = [(x_min, y_min), (x_min, y_max), (x_max, y_min), (x_max, y_max)]
        for corner in corners:
            if corner not in data and not self.__is_point_in_polygon__(
                corner, vertical_lines
            ):
                return False

        for y, sx, ex in horizontal_lines:
            if y_min < y < y_max and not (ex <= x_min or sx >= x_max):
                return False

        for x, sy, ey in vertical_lines:
            if x_min < x < x_max and not (ey <= y_min or sy >= y_max):
                return False

        return True

    def __is_point_in_polygon__(
        self, xy: XYCoord, lines: List[Tuple[int, int, int]]
    ) -> bool:
        x, y = xy
        inside = False
        for px, ay, by in lines:
            if px > x and ay <= y < by:
                inside = not inside
        return inside
