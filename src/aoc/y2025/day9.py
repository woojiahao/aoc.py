from typing import Any, List, Set, Tuple

from aoc.utils.spatial import XYCoord

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
        return self.__polygon_solve__(data)

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
