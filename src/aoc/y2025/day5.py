from typing import Any, List, Tuple

from ..solution import Solution


class Y2025Day5(Solution):
    def parse_data(self, contents: str) -> Any:
        [ingredient_ranges_raw, ingredients_raw] = contents.strip().split("\n\n")
        ingredient_ranges = []
        for r in ingredient_ranges_raw.split("\n"):
            s, e = r.split("-")
            ingredient_ranges.append([int(s), int(e)])

        ingredient_ranges.sort()
        merged_intervals = [ingredient_ranges[0]]
        for i in range(1, len(ingredient_ranges)):
            cur_range = ingredient_ranges[i]
            if cur_range[0] <= merged_intervals[-1][1]:
                merged_intervals[-1][1] = max(merged_intervals[-1][1], cur_range[1])
            else:
                merged_intervals.append(cur_range)

        ingredients = [int(l) for l in ingredients_raw.strip().split("\n")]
        return merged_intervals, ingredients

    def solve_one(self, data: Tuple[List[List[int]], List[int]]) -> Any:
        ingredient_ranges, ingredients = data
        ans = 0
        for ingredient in ingredients:
            for s, e in ingredient_ranges:
                if s <= ingredient <= e:
                    print(s, ingredient, e)
                    ans += 1
        return ans

    def solve_two(self, data: Tuple[List[List[int]], List[int]]) -> Any:
        ingredient_ranges, _ = data
        ans = 0
        for s, e in ingredient_ranges:
            ans += e - s + 1
        return ans
