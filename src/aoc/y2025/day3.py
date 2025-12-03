from typing import Any, Dict, List, Tuple

from ..solution import Solution


class Y2025Day3(Solution):
    def parse_data(self, contents: str) -> Any:
        banks = []
        for line in contents.strip().split("\n"):
            banks.append([int(battery) for battery in line])
        return banks

    def solve_one(self, data: List[List[int]]) -> Any:
        # ans = 0
        # for bank in data:
        #     n = len(bank)
        #     max_joltage = 0
        #     for i in range(n):
        #         for j in range(i + 1, n):
        #             max_joltage = max(max_joltage, bank[i] * 10 + bank[j])
        #     ans += max_joltage
        # return ans
        #
        ans = 0
        for bank_ in data:
            ans += self.__take__(bank_, 0, 0, 2, 0, {})
        return ans

    def solve_two(self, data: List[List[int]]) -> Any:
        ans = 0
        for bank_ in data:
            ans += self.__take__(bank_, 0, 0, 12, 0, {})
        return ans

    def __take__(
        self,
        bank: List[int],
        i: int,
        taken: int,
        max_taken: int,
        acc: int,
        memo: Dict[Tuple[int, int, int], int],
    ) -> int:
        key = (i, taken, acc)
        if key in memo:
            return memo[key]

        if i >= len(bank) and taken < max_taken:
            return 0

        if i >= len(bank) or taken >= max_taken:
            return acc

        memo[key] = max(
            self.__take__(bank, i + 1, taken + 1, max_taken, acc * 10 + bank[i], memo),
            self.__take__(bank, i + 1, taken, max_taken, acc, memo),
        )
        return memo[key]
