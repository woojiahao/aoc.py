import re
import sys
from typing import Any, Dict, List, Tuple

from ..solution import Solution

sys.setrecursionlimit(10**7)


class Y2024Day13(Solution):
    INVALID = 10**15

    def parse_data(self, contents: str) -> Any:
        data = []
        button_a_regex = re.compile("Button A: X\\+(\\d+), Y\\+(\\d+)")
        button_b_regex = re.compile("Button B: X\\+(\\d+), Y\\+(\\d+)")
        prize_regex = re.compile("Prize: X=(\\d+), Y=(\\d+)")
        for chunk in contents.strip().split("\n\n"):
            [button_a_raw, button_b_raw, prize_raw] = chunk.split("\n")
            a = button_a_regex.match(button_a_raw)
            b = button_b_regex.match(button_b_raw)
            p = prize_regex.match(prize_raw)
            assert a is not None and b is not None and p is not None
            button_a = (int(a.group(1)), int(a.group(2)))
            button_b = (int(b.group(1)), int(b.group(2)))
            prize = (int(p.group(1)), int(p.group(2)))
            data.append((button_a, button_b, prize))
        return data

    def solve_one(
        self, data: List[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]]
    ) -> Any:
        ans = 0
        for button_a, button_b, prize in data:
            tokens = self.__play_claw_machine__(button_a, button_b, prize)
            if tokens != self.INVALID:
                ans += tokens
        return ans

    def solve_two(
        self, data: List[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]]
    ) -> Any:
        ans = 0
        for button_a, button_b, prize in data:
            prize = (prize[0] + 10000000000000, prize[1] + 10000000000000)
            tokens = self.__play_claw_machine__(button_a, button_b, prize)
            if tokens != self.INVALID:
                ans += tokens
        return ans

    def __play_claw_machine__(
        self,
        button_a: Tuple[int, int],
        button_b: Tuple[int, int],
        prize: Tuple[int, int],
    ) -> Any:
        ax, ay = button_a
        bx, by = button_b
        px, py = prize

        m = (ax * py - ay * px) / (ax * by - ay * bx)
        n = (px - m * bx) / ax
        if int(m) == m and int(n) == n:
            return int(n) * 3 + int(m)
        return self.INVALID
