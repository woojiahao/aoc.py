from typing import Any, Dict, List, Tuple

from ..solution import Solution


class Y2024Day19(Solution):
    def parse_data(self, contents: str) -> Any:
        [available_raw, designs_raw] = contents.strip().split("\n\n")
        return available_raw.split(", "), designs_raw.split("\n")

    def solve_one(self, data: Tuple[List[str], List[str]]) -> Any:
        available, designs = data
        ans = 0
        for design in designs:
            ans += int(self.__is_design_possible__(available, design))
        return ans

    def solve_two(self, data: Any) -> Any:
        available, designs = data
        ans = 0
        available_dict: Dict[str, List[str]] = {}
        for a in available:
            if a[0] not in available_dict:
                available_dict[a[0]] = []
            available_dict[a[0]].append(a)
        for design in designs:
            ans += self.__try_design__(design, 0, available_dict, {})
        return ans

    def __is_design_possible__(self, available: List[str], design: str) -> bool:
        n = len(design)
        dp = [False] * (n + 1)
        dp[0] = True
        available_set = set(available)

        for i in range(n + 1):
            for j in range(i):
                if design[j:i] in available_set:
                    dp[i] = dp[j]
                if dp[i]:
                    break
        return dp[-1]

    def __try_design__(
        self,
        design: str,
        i: int,
        available_dict: Dict[str, List[str]],
        memo: Dict[int, int],
    ) -> int:
        if i in memo:
            return memo[i]

        if i >= len(design):
            return 1

        ways = 0
        for a in available_dict.get(design[i], []):
            if a == design[i : i + len(a)]:
                ways += self.__try_design__(design, i + len(a), available_dict, memo)
        memo[i] = ways
        return ways
