from copy import copy
from dataclasses import dataclass
from typing import Any, List, Tuple, Type

from ..solution import Solution

Present = List[List[bool]]


@dataclass
class Region:
    width: int
    height: int
    present_distribution: List[int]
    grid: List[List[bool]]

    @classmethod
    def from_region_str(cls: Type["Region"], region: str) -> "Region":
        [dimensions_raw, present_distribution_raw] = region.split(": ")
        present_distribution = [int(v) for v in present_distribution_raw.split(" ")]
        [width, height] = [int(v) for v in dimensions_raw.split("x")]
        return cls(
            width=width,
            height=height,
            present_distribution=present_distribution,
            grid=[[False] * width for _ in range(height)],
        )

    def try_fitting(self, presents: List[List[Present]]) -> bool:
        H, W = self.height, self.width

        # Immediately terminate if the presents we want to choose can never be fit
        # within the region by area
        total_present_area = 0
        for i, v in enumerate(self.present_distribution):
            if v != 0:
                present = presents[i][0]
                present_area = 0
                for row in present:
                    for cell in row:
                        if cell:
                            present_area += 1
                total_present_area += present_area * v
        if total_present_area > (self.width * self.height):
            print("too small!")
            return False

        placed = 0

        def can_place(present, r, c):
            ph, pw = len(present), len(present[0])
            for dr in range(ph):
                for dc in range(pw):
                    if present[dr][dc] and self.grid[r + dr][c + dc]:
                        return False

            if placed == 0:
                return True

            for rr in range(max(0, r - 1), min(H, r + 4)):
                for cc in range(max(0, c - 1), min(W, c + 4)):
                    if self.grid[rr][cc]:
                        return True

            return False

        def place(present, r, c, val):
            nonlocal placed

            if val:
                placed += 1
            else:
                placed -= 1

            ph, pw = len(present), len(present[0])
            for dr in range(ph):
                for dc in range(pw):
                    if present[dr][dc]:
                        self.grid[r + dr][c + dc] = val

        to_place = []
        for i, c in enumerate(self.present_distribution):
            if c != 0:
                for _ in range(c):
                    to_place.append(i)

        def grid_repr():
            return "".join(
                "".join("." if not c else "#" for c in line) for line in self.grid
            )

        visited = set()

        def dfs():
            if len(to_place) == 0:
                return True

            repr = grid_repr()
            if repr in visited:
                return False
            visited.add(repr)

            present_id = to_place.pop()
            for r in range(H - 3 + 1):
                for c in range(W - 3 + 1):
                    for variant in presents[present_id]:
                        if can_place(variant, r, c):
                            place(variant, r, c, True)
                            if dfs():
                                return True
                            place(variant, r, c, False)
            to_place.append(present_id)
            return False

        return dfs()


def print_grid(grid: List[List[bool]]) -> None:
    for row in grid:
        line = []
        for ch in row:
            if ch:
                line.append("#")
            else:
                line.append(".")
        print("".join(line))


class Y2025Day12(Solution):
    def parse_data(self, contents: str) -> Any:
        sections = contents.strip().split("\n\n")
        regions_raw = sections[-1]
        presents_raw = sections[:-1]
        regions = []
        for region in regions_raw.split("\n"):
            regions.append(Region.from_region_str(region))

        presents = []
        for present in presents_raw:
            present_all = []
            for line in present.split("\n")[1:]:
                present_line = []
                for ch in line:
                    present_line.append(ch == "#")
                present_all.append(present_line)
            presents.append(self.__generate_presents__(present_all))

        return regions, presents

    def solve_one(self, data: Tuple[List[Region], List[List[Present]]]) -> Any:
        regions, presents = data
        ans = 0
        for i, region in enumerate(regions):
            print(f"{i + 1}.")
            if region.try_fitting(presents):
                print("solved")
                ans += 1
        return ans

    def solve_two(self, data: Any) -> Any:
        pass

    def __generate_presents__(self, present: Present) -> List[Present]:
        presents: List[Present] = []
        for i in range(4):
            rotated_present = copy(present)
            for _ in range(i):
                rotated_present = self.__rotate__(rotated_present)

            if not self.__has_present__(presents, rotated_present):
                presents.append(rotated_present)

            flipped_vertical_present = self.__flip_vertical__(rotated_present)
            if not self.__has_present__(presents, flipped_vertical_present):
                presents.append(flipped_vertical_present)

            flipped_horizontal_present = self.__flip_horizontal__(rotated_present)
            if not self.__has_present__(presents, flipped_horizontal_present):
                presents.append(flipped_horizontal_present)

        return presents

    def __has_present__(self, presents: List[Present], present: Present) -> bool:
        for p in presents:
            all_same = True
            for a, b in zip(p, present):
                if a != b:
                    all_same = False
                    break
            if all_same:
                return True
        return False

    def __rotate__(self, present: Present) -> Present:
        t = zip(*present)
        return [list(r[::-1]) for r in t]

    def __flip_vertical__(self, present: Present) -> Present:
        result = []
        for row in present:
            line = [False] * len(row)
            l, r = 0, len(row) - 1
            while l <= r:
                line[l], line[r] = row[r], row[l]
                l, r = l + 1, r - 1
            result.append(line)
        return result

    def __flip_horizontal__(self, present: Present) -> Present:
        result = [[False] * len(present[0]) for _ in range(len(present))]
        l, r = 0, len(present) - 1
        while l <= r:
            result[l], result[r] = present[r], present[l]
            l, r = l + 1, r - 1
        return result
