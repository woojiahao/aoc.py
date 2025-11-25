from typing import Any, Dict, List, Tuple
from collections import Counter

from ..solution import Solution


class Y2024Day11(Solution):
    def parse_data(self, contents: str) -> Any:
        line = contents.strip().split(" ")
        return line

    def solve_one(self, data: List[str]) -> Any:
        stones = data
        for _ in range(25):
            stones = self.__blink__(stones)
        return len(stones)

    def solve_two(self, data: Any) -> Any:
        stones = dict(Counter(data))
        for _ in range(75):
            stones = self.__blink_fast__(stones)
        ans = 0
        for _, f in stones.items():
            ans += f
        return ans

    def __blink__(self, stones: List[str]) -> List[str]:
        new_stones = []
        for s in stones:
            i_s = int(s)
            if s == "0":
                new_stones.append("1")
            elif len(s) % 2 == 0:
                new_stones.append(str(int(s[: len(s) // 2])))
                new_stones.append(str(int(s[len(s) // 2 :])))
            else:
                new_stones.append(str(i_s * 2024))
        return new_stones

    def __blink_fast__(self, stones: Dict[str, int]) -> Dict[str, int]:
        new_stones: Dict[str, int] = {}
        for s, f in stones.items():
            i_s = int(s)
            if s == "0":
                new_stones["1"] = new_stones.get("1", 0) + f
            elif len(s) % 2 == 0:
                l, r = str(int(s[: len(s) // 2])), str(int(s[len(s) // 2 :]))
                new_stones[l] = new_stones.get(l, 0) + f
                new_stones[r] = new_stones.get(r, 0) + f
            else:
                new_stones[str(i_s * 2024)] = new_stones.get(str(i_s * 2024), 0) + f
        return new_stones
