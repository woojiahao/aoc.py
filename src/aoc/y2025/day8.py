from typing import Any, List, Tuple

from ..solution import Solution
from ..utils.math import euclidean_distance
from ..utils.spatial import XYZCoord
from ..utils.ufds import UFDS


class Y2025Day8(Solution):
    def parse_data(self, contents: str) -> Any:
        junction_boxes: List[XYZCoord] = []
        for line in contents.strip().split("\n"):
            [x, y, z] = [int(v) for v in line.split(",")]
            junction_boxes.append((x, y, z))
        return junction_boxes

    def solve_one(self, data: List[XYZCoord]) -> Any:
        pick = 10 if self.is_test_mode() else 1000

        ufds = UFDS(len(data))
        for pair in self.__get_ordered_pairs__(data)[:pick]:
            ufds.union(pair[0], pair[1])

        ans = 1
        for v in sorted(ufds.union_sizes.values(), reverse=True)[:3]:
            ans *= v
        return ans

    def solve_two(self, data: List[XYZCoord]) -> Any:
        ufds = UFDS(len(data))

        for pair in self.__get_ordered_pairs__(data):
            ufds.union(pair[0], pair[1])
            if ufds.unions == 1:
                return data[pair[0]][0] * data[pair[1]][0]
        return -1

    def __get_ordered_pairs__(
        self, data: List[XYZCoord]
    ) -> List[Tuple[int, int, float]]:
        n = len(data)
        all_pairs = []
        for i in range(n):
            for j in range(i + 1, n):
                all_pairs.append((i, j, euclidean_distance(data[i], data[j])))
        all_pairs.sort(key=lambda x: x[2])
        return all_pairs
