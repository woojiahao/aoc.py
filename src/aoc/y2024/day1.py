from typing import Any, List, Tuple
from collections import Counter

from ..solution import Solution


class Y2024Day1(Solution):
    def parse_data(self, contents: str) -> Any:
        first, second = [], []
        for line in contents.strip().split("\n"):
            [a, b] = line.split("   ")
            first.append(int(a))
            second.append(int(b))
        first.sort()
        second.sort()
        return first, second

    def solve_one(self, data: Tuple[List[int], List[int]]) -> Any:
        ans = 0
        for a, b in zip(data[0], data[1]):
            ans += abs(a - b)
        return ans

    def solve_two(self, data: Tuple[List[int], List[int]]) -> Any:
        second_frequency = Counter(data[1])
        ans = 0
        for a in data[0]:
            ans += a * second_frequency.get(a, 0)
        return ans
