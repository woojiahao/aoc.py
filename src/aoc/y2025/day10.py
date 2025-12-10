from collections import deque
from typing import Any, List, Self, Tuple, Type

from scipy.optimize import linprog

from ..solution import Solution


class Machine:
    def __init__(
        self,
        indicator_lights: int,
        button_wirings: List[int],
        button_wirings_original: List[List[int]],
        joltage_requirements: Tuple[int, ...],
    ) -> None:
        self.indicator_lights_final = indicator_lights
        self.indicator_lights = 0
        self.button_wirings = button_wirings
        self.button_wirings_original = button_wirings_original
        self.joltage_requirements = joltage_requirements

    def find_total_presses_for_indicator_lights(self) -> int:
        q = deque([(self.indicator_lights, 0)])
        visited = set()
        while q:
            arrangement, steps = q.popleft()
            if arrangement == self.indicator_lights_final:
                return steps
            for wiring in self.button_wirings:
                new_wiring = arrangement ^ wiring
                if new_wiring in visited:
                    continue
                q.append((new_wiring, steps + 1))
                visited.add((new_wiring))
        return 0

    def find_total_presses_for_joltage_requirements(self) -> int:
        """
        N = number of buttons
        M = joltages
        J = joltage requirements (M x 1)
        K = buttons (binary matrix of M x N)
        X = button clicks (N x 1)

        J = K . X
        (M x N) . (N x 1) = (M x 1) -> linear equation
        """
        M = len(self.joltage_requirements)
        N = len(self.button_wirings_original)

        K = []
        for i in range(M):
            row = []
            for j in range(N):
                row.append(1 if i in self.button_wirings_original[j] else 0)
            K.append(row)

        c = [1] * N

        res = linprog(
            c,
            A_eq=K,
            b_eq=self.joltage_requirements,
            bounds=(0, None),
            method="highs",
            integrality=1,
        )

        if res.success:
            return int(sum(res.x))  # type: ignore
        return 0

    @classmethod
    def from_str(cls: Type["Machine"], line: str) -> "Machine":
        parts = line.split(" ")
        indicator_lights_raw = parts[0]
        joltage_requirements_raw = parts[-1]
        button_wirings_raw = parts[1:-1]

        indicator_lights = 0
        for i, ch in enumerate(indicator_lights_raw[1:-1]):
            if ch == "#":
                indicator_lights |= 1 << i

        button_wirings = []
        button_wirings_original = []
        for wiring in button_wirings_raw:
            wiring = wiring[1:-1]
            w_original = []
            w = 0
            for ch in wiring.split(","):
                w |= 1 << int(ch)
                w_original.append(int(ch))
            button_wirings.append(w)
            button_wirings_original.append(w_original)

        joltage_requirements = tuple(
            [int(ch) for ch in joltage_requirements_raw[1:-1].split(",")]
        )
        return cls(
            indicator_lights=indicator_lights,
            button_wirings=button_wirings,
            button_wirings_original=button_wirings_original,
            joltage_requirements=joltage_requirements,
        )


class Y2025Day10(Solution):
    def parse_data(self, contents: str) -> Any:
        machines = []
        for line in contents.strip().split("\n"):
            machine = Machine.from_str(line)
            machines.append(machine)
        return machines

    def solve_one(self, data: List[Machine]) -> Any:
        ans = 0
        for machine in data:
            ans += machine.find_total_presses_for_indicator_lights()
        return ans

    def solve_two(self, data: List[Machine]) -> Any:
        ans = 0
        for machine in data:
            ans += machine.find_total_presses_for_joltage_requirements()
        return ans
