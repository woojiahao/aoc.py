from typing import Any, List, Tuple

from ..solution import Solution


class Y2024Day1(Solution):
    def parse_data(self, contents: str) -> Any:
        first, second = [], []
        for line in contents.strip().split("\n"):
            [a, b] = line.split("   ")
            first.append(int(a))
            second.append(int(b))
        return first, second

    def solve_one(self, data: Tuple[List[int], List[int]]) -> Any:
        first, second = data
        first.sort()
        second.sort()
        ans = 0
        for a, b in zip(first, second):
            ans += abs(a - b)
        return ans

    def solve_two(self, data: Any) -> Any:
        print(data)
