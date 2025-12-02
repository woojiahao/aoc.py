from typing import Any, List, Tuple

from ..solution import Solution


class Y2025Day2(Solution):
    def parse_data(self, contents: str) -> Any:
        line = contents.strip().split(",")
        ranges = []
        for range_raw in line:
            [start, end] = range_raw.split("-")
            ranges.append((int(start), int(end)))
        return ranges

    def solve_one(self, data: List[Tuple[int, int]]) -> Any:
        ans = 0
        for start, end in data:
            for i in range(start, end + 1):
                sn = str(i)
                if len(sn) % 2 != 0:
                    continue

                if self.__is_repeated__(sn, len(sn) // 2):
                    ans += i
        return ans

    def solve_two(self, data: Any) -> Any:
        ans = 0
        for start, end in data:
            for i in range(start, end + 1):
                sn = str(i)
                for chunk_size in range(1, len(sn) // 2 + 1):
                    if self.__is_repeated__(sn, chunk_size):
                        ans += i
                        break
        return ans

    def __is_repeated__(self, sn: str, chunk_size: int) -> bool:
        if len(sn) % chunk_size != 0:
            return False
        chunks = [sn[i : i + chunk_size] for i in range(0, len(sn), chunk_size)]
        return all([chunk == chunks[0] for chunk in chunks])
