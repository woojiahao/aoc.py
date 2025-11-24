from typing import Any, List, Tuple
import re

from ..solution import Solution


class Y2024Day3(Solution):
    def parse_data(self, contents: str) -> str:
        line = contents.strip()
        return line

    def solve_one(self, data: str) -> Any:
        regex = re.compile("mul\\((\\d+),(\\d+)\\)")
        matches = regex.findall(data)
        ans = 0
        for a, b in matches:
            ans += int(a) * int(b)
        return ans

    def solve_two(self, data: str) -> Any:
        regex = re.compile("mul\\((\\d+),(\\d+)\\)")
        matches = regex.finditer(data)
        ops: List[Any] = []
        ans = 0
        for match in matches:
            ops.append((match.start(), int(match.group(1)), int(match.group(2))))
        other_regex = re.compile("do(?:n't)?\\(\\)")
        other_matches = other_regex.finditer(data)
        for match in other_matches:
            ops.append((match.start(), match.group(0) == "do()"))
        ops.sort()
        acc = True
        for op in ops:
            if len(op) == 2:
                acc = op[1]
            elif acc:
                ans += op[1] * op[2]
        return ans
