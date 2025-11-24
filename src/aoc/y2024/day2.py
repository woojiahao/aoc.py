from typing import Any, List, Tuple

from aoc.utils.math import sign

from ..solution import Solution


class Y2024Day2(Solution):
    def parse_data(self, contents: str) -> Any:
        data = []
        for line in contents.strip().split("\n"):
            level_parts = [int(a) for a in line.strip().split(" ")]
            data.append(level_parts)
        return data

    def solve_one(self, data: List[List[int]]) -> Any:
        safe_count = 0
        for report in data:
            safe_count += int(self.__is_safe__(report))
        return safe_count

    def solve_two(self, data: List[List[int]]) -> Any:
        safe_count = 0
        for report in data:
            for i in range(len(report)):
                if self.__is_safe__(report[:i] + report[i + 1 :]):
                    safe_count += 1
                    break
        return safe_count

    def __is_safe__(self, report: List[int]) -> bool:
        diffs = []
        for i in range(1, len(report)):
            d = report[i] - report[i - 1]
            diffs.append(d)
        return (
            all(abs(a) >= 1 and abs(a) <= 3 for a in diffs)
            and len(set(sign(a) for a in diffs)) == 1
        )
