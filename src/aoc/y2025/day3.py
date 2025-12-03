from typing import Any, Dict, List, Tuple

from ..solution import Solution


class Y2025Day3(Solution):
    def parse_data(self, contents: str) -> Any:
        banks = []
        for line in contents.strip().split("\n"):
            banks.append([int(battery) for battery in line])
        return banks

    def solve_one(self, data: List[List[int]]) -> Any:
        return self.__solve__(data, 2)

    def solve_two(self, data: List[List[int]]) -> Any:
        return self.__solve__(data, 12)

    def __solve__(self, data: List[List[int]], max_taken: int) -> int:
        ans = 0
        for bank_ in data:
            ans += self.__take_batteries__(bank_, max_taken)
        return ans

    def __take_batteries__(self, bank: List[int], max_taken: int) -> int:
        taken = 0
        n = len(bank)
        l, r = 0, n - 1
        joltage = 0
        while taken < max_taken:
            remaining = max_taken - taken - 1
            max_seen = bank[l]
            max_seen_i = l
            for i in range(l, r + 1):
                remaining_digits = n - i - 1
                if bank[i] > max_seen and remaining_digits >= remaining:
                    max_seen = bank[i]
                    max_seen_i = i
            joltage = joltage * 10 + max_seen
            l = max_seen_i + 1
            taken += 1
        return joltage
