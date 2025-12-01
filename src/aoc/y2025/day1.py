from typing import Any, List, Tuple

from ..solution import Solution
from ..utils.math import sign


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
        #   Case: X = 50, R80, Y = 30
        # Rotate left past 0 -> number X -> number Y => X < Y
        #   Case: X = 50, L80, Y = 69
        # If rotation >= 100 -> MUST rotate past 0 so at the minimum, it's rotation // dial_size
        # For all excess -> (rotation - (rotation // dial_size) * 100) = excess

        """
        Rules:
        1. (a) Rotate right past 0 and you don't start or land on 0, prev_pos > new_pos
           (b) Rotate left past 0 and you don't start or land on 0, prev_pos < new_pos 

        2. If abs(rotation) > dial_size, then 
           (a) Always going to rotate around 0 at least once
           (b) Excess (abs(rotation) - (# of times it was already rotated) * 100))
                (prev_pos + excess) % dial_size is subject to (1)
        """
        for rotation in data:
            # Rule 2
            exceed_dial_size_rotations = 0
            if abs(rotation) >= dial_size:
                exceed_dial_size_rotations = abs(rotation) // dial_size

            excess = sign(rotation) * (
                abs(rotation) - (exceed_dial_size_rotations * dial_size)
            )

            # Rule 1
            new_pos = (pos + excess) % dial_size
            excess_past_zero = 0
            if rotation < 0 and new_pos != 0 and pos != 0 and pos < new_pos:
                excess_past_zero = 1
            elif rotation > 0 and new_pos != 0 and pos != 0 and pos > new_pos:
                excess_past_zero = 1

            new_pos_at_zero = int(new_pos == 0)
            ans += exceed_dial_size_rotations + excess_past_zero + new_pos_at_zero

            pos = new_pos

        return ans
