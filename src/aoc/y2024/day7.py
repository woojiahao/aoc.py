from typing import Any, List, Tuple

from ..solution import Solution


class Y2024Day7(Solution):
    def parse_data(self, contents: str) -> Any:
        ans = []
        for line in contents.strip().split("\n"):
            [test_value, values] = line.split(": ")
            int_values = [int(v) for v in values.split(" ")]
            ans.append((int(test_value), int_values))
        return ans

    def solve_one(self, data: List[Tuple[int, List[int]]]) -> Any:
        ans = 0
        for test_value, int_values in data:
            if self.__can_equate__(test_value, int_values):
                ans += test_value
        return ans

    def solve_two(self, data: Any) -> Any:
        ans = 0
        for test_value, int_values in data:
            if self.__can_equate_2__(test_value, int_values):
                ans += test_value
        return ans

    def __can_equate__(self, test_value: int, int_values: List[int]) -> bool:
        def dfs(i: int, acc: int) -> bool:
            if i >= len(int_values):
                return acc == test_value
            return dfs(i + 1, acc * int_values[i]) or dfs(i + 1, acc + int_values[i])

        return dfs(1, int_values[0])

    def __can_equate_2__(self, test_value: int, int_values: List[int]) -> bool:
        def dfs(i: int, acc: int) -> bool:
            if i >= len(int_values):
                return acc == test_value
            return (
                dfs(i + 1, acc * int_values[i])
                or dfs(i + 1, acc + int_values[i])
                or dfs(i + 1, int(str(acc) + str(int_values[i])))
            )

        return dfs(1, int_values[0])
