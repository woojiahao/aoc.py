from typing import Any, Dict, List, Set, Tuple, Union
from functools import cmp_to_key

from ..solution import Solution


class Y2024Day5(Solution):
    def parse_data(self, contents: str) -> Any:
        [page_order_rules, pages_to_produce] = contents.strip().split("\n\n")
        return set(
            [
                tuple([int(p) for p in line.split("|")])
                for line in page_order_rules.split("\n")
            ]
        ), [[int(p) for p in line.split(",")] for line in pages_to_produce.split("\n")]

    def solve_one(self, data: Tuple[Set[Tuple[int, int]], List[List[int]]]) -> Any:
        page_order_rules, pages = data
        ans = 0
        for page in pages:
            if self.__validate_order__(page_order_rules, page):
                ans += page[len(page) // 2]
        return ans

    def solve_two(self, data: Tuple[Set[Tuple[int, int]], List[List[int]]]) -> Any:
        page_order_rules, pages = data
        ans = 0

        def cmp(a: int, b: int) -> int:
            if (b, a) in page_order_rules:
                return 1
            return -1

        for page in pages:
            if not self.__validate_order__(page_order_rules, page):
                page.sort(key=cmp_to_key(cmp))
                ans += page[len(page) // 2]
        return ans

    def __validate_order__(
        self, page_order_rules: Set[Tuple[int, int]], page: List[int]
    ) -> bool:
        for a in range(len(page)):
            for b in range(a + 1, len(page)):
                if (page[b], page[a]) in page_order_rules:
                    return False
        return True
