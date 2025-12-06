from typing import Any, List, Tuple

from ..solution import Solution


class Y2025Day6(Solution):
    def parse_data(self, contents: str) -> Any:
        return contents

    def solve_one(self, data: str) -> Any:
        lines = data.strip().split("\n")
        numbers = lines[:-1]
        operations = lines[-1].split()
        col_numbers: List[List[int]] = []
        for row in numbers:
            row_ints = [int(r) for r in row.split()]
            for c, cell in enumerate(row_ints):
                if len(col_numbers) <= c:
                    col_numbers.append([])
                col_numbers[c].append(cell)
        return self.__perform_operations__(col_numbers, operations)

    def solve_two(self, data: str) -> Any:
        lines = data.strip().split("\n")
        nums = lines[:-1]
        col_starts = [i for i, ch in enumerate(lines[-1]) if ch != " "]
        rows, ans = len(nums), 0
        for s, e in zip(col_starts, col_starts[1:] + [len(nums[0]) + 1]):
            ans += eval(
                lines[-1][s].join(
                    [
                        "".join([nums[r][c] for r in range(rows) if nums[r][c] != " "])
                        for c in range(s, e - 1)
                    ]
                )
            )
        return ans

    def __perform_operations__(
        self, col_numbers: List[List[int]], operations: List[str]
    ) -> int:
        ans = 0
        for col, operation in zip(col_numbers, operations):
            if operation == "+":
                acc = sum(col)
            else:
                acc = 1
                for n in col:
                    acc *= n
            ans += acc
        return ans
