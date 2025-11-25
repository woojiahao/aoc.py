from collections import deque
from typing import Any, Deque, List, Tuple

from ..solution import Solution


class Y2024Day9(Solution):
    def parse_data(self, contents: str) -> Any:
        line = [int(ch) for ch in list(contents.strip())]
        return line

    def solve_one(self, data: List[int]) -> Any:
        # Behaves as a queue for front most empty slots
        empty: Deque[int] = deque([])

        # Behaves as a stack for end most available slots
        filled: List[Tuple[int, int]] = []

        is_file = True
        i = 0
        id = 0
        for d in data:
            if is_file:
                for _ in range(d):
                    filled.append((id, i))
                    i += 1
                id += 1
            else:
                for _ in range(d):
                    empty.append(i)
                    i += 1
            is_file = not is_file
        compacted_positions = []
        while empty and filled and empty[0] < filled[-1][1]:
            empty_position = empty.popleft()
            filled_id, _ = filled.pop()
            compacted_positions.append((filled_id, empty_position))
        while filled:
            compacted_positions.append(filled.pop())
        checksum = 0
        for id, position in compacted_positions:
            checksum += id * position
        return checksum

    def solve_two(self, data: List[int]) -> Any:
        # Behaves as a queue for front most empty slots
        empty: Deque[Tuple[int, int]] = deque([])

        # Behaves as a stack for end most available slots
        filled: List[Tuple[int, int, int]] = []

        is_file = True
        i = 0
        id = 0
        for d in data:
            if is_file:
                filled.append((id, i, d))
                id += 1
            else:
                empty.append((i, d))
            i += d
            is_file = not is_file
        compacted_positions = []
        j = len(filled) - 1
        while j >= 0 and empty:
            last_block_id, last_block_start, last_block_length = filled.pop()
            for k in range(len(empty)):
                if empty[k][0] < last_block_start and empty[k][1] >= last_block_length:
                    remaining = empty[k][1] - last_block_length
                    empty_start = empty[k][0]
                    del empty[k]
                    if remaining > 0:
                        empty.insert(k, (empty_start + last_block_length, remaining))
                    compacted_positions.append(
                        (last_block_id, empty_start, last_block_length)
                    )
                    break
            else:
                compacted_positions.append(
                    (last_block_id, last_block_start, last_block_length)
                )
            j -= 1

        while filled:
            compacted_positions.append(filled.pop())

        checksum = 0
        for id, position, d in compacted_positions:
            for k in range(d):
                checksum += id * (position + k)

        return checksum
