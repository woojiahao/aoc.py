from typing import Any, List, Tuple

from ..solution import Solution


class Y2025Day1(Solution):
    def parse_data(self, contents: str) -> Any:
        rotations = [
            int(rotation_raw[1:]) * (-1 if rotation_raw[0] == "L" else 1)
            for rotation_raw in contents.strip().split("\n")
        ]
        return rotations

    def solve_one(self, data: List[int]) -> Any:
        pos = 50
        dial_size = 100
        ans = 0
        for rotation in data:
            pos = (pos + rotation) % dial_size
            if pos == 0:
                ans += 1
        return ans

    def solve_two(self, data: Any) -> Any:
        pos = 50
        dial_size = 100
        ans = 0
        # Rotate right past 0 -> number X -> number Y => X > Y
        # Rotate left past 0 -> number X -> number Y => X < Y
        # Pass 0 iff (pos + rotation) > 99 (pos + rotation) < 0
        for rotation in data:
            for _ in range(abs(rotation)):
                if rotation < 0:
                    pos = (pos - 1) % dial_size
                else:
                    pos = (pos + 1) % dial_size
                if pos == 0:
                    ans += 1

        return ans
