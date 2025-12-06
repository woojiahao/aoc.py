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
        numbers = lines[:-1]
        operations = lines[-1]
        col_starts = []
        for i, ch in enumerate(operations):
            if ch == " ":
                continue
            col_starts.append(i)

        cols = []
        for row in numbers:
            cells = []
            padded_row = row.replace(" ", "0")
            for i, start in enumerate(col_starts):
                if i + 1 < len(col_starts):
                    cells.append(padded_row[start : col_starts[i + 1] - 1])
                else:
                    cells.append(padded_row[start:])
            cols.append(cells)
        transposed_cols = list(zip(*cols))

        col_numbers = []
        for col in transposed_cols:
            l_col = list(col)
            transposed_l_col = list(zip(*l_col))
            nums = []
            for raw_num in transposed_l_col:
                num_s = "".join(raw_num).strip("0")
                nums.append(int(num_s))
            col_numbers.append(nums)

        return self.__perform_operations__(col_numbers, operations.split())

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
