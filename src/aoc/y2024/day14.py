import re
import os
import time
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from ..solution import Solution

ROBOT_REGEX = re.compile("p=(\\d+),(\\d+) v=([-\\d]+),([-\\d]+)")


@dataclass
class Robot:
    start_x: int
    start_y: int

    cur_x: int
    cur_y: int

    move_x: int
    move_y: int

    @staticmethod
    def from_line(line: str) -> "Robot":
        matches = ROBOT_REGEX.match(line)
        assert matches is not None
        start_x = int(matches.group(1))
        start_y = int(matches.group(2))
        move_x = int(matches.group(3))
        move_y = int(matches.group(4))
        return Robot(
            start_x=start_x,
            start_y=start_y,
            cur_x=start_x,
            cur_y=start_y,
            move_x=move_x,
            move_y=move_y,
        )

    def move(self, width: int, height: int) -> None:
        self.cur_x = (self.cur_x + self.move_x) % width
        self.cur_y = (self.cur_y + self.move_y) % height


class Y2024Day14(Solution):
    TEST_TILES_WIDTH = 11
    TEST_TILES_HEIGHT = 7

    LIVE_TILES_WIDTH = 101
    LIVE_TILES_HEIGHT = 103

    def parse_data(self, contents: str) -> Any:
        robots = []
        for line in contents.strip().split("\n"):
            robots.append(Robot.from_line(line))
        return robots

    def solve_one(self, data: List[Robot]) -> Any:
        width = self.TEST_TILES_WIDTH if self.is_test_mode() else self.LIVE_TILES_WIDTH
        height = (
            self.TEST_TILES_HEIGHT if self.is_test_mode() else self.LIVE_TILES_HEIGHT
        )
        for _ in range(100):
            for robot in data:
                robot.move(width, height)
        robot_positions: Dict[Tuple[int, int], int] = defaultdict(int)
        for robot in data:
            robot_positions[(robot.cur_x, robot.cur_y)] += 1

        # Quadrant 1
        q1 = []
        for x in range(width // 2):
            for y in range(height // 2):
                if (x, y) in robot_positions:
                    q1.append(robot_positions[(x, y)])

        # Quadrant 2
        q2 = []
        for x in range(width // 2 + 1, width):
            for y in range(height // 2):
                if (x, y) in robot_positions:
                    q2.append(robot_positions[(x, y)])

        # Quadrant 3
        q3 = []
        for x in range(width // 2):
            for y in range(height // 2 + 1, height):
                if (x, y) in robot_positions:
                    q3.append(robot_positions[(x, y)])
        # Quadrant 4
        q4 = []
        for x in range(width // 2 + 1, width):
            for y in range(height // 2 + 1, height):
                if (x, y) in robot_positions:
                    q4.append(robot_positions[(x, y)])

        ans = sum(q1) * sum(q2) * sum(q3) * sum(q4)
        return ans

    def solve_two(self, data: Any) -> Any:
        width = self.TEST_TILES_WIDTH if self.is_test_mode() else self.LIVE_TILES_WIDTH
        height = (
            self.TEST_TILES_HEIGHT if self.is_test_mode() else self.LIVE_TILES_HEIGHT
        )
        for i in range(10_000):
            print(f"Iteration {i}")
            for robot in data:
                robot.move(width, height)
            self.__print_grid__(data)
            print()

    def __print_grid__(self, robots: List[Robot]) -> None:
        width = self.TEST_TILES_WIDTH if self.is_test_mode() else self.LIVE_TILES_WIDTH
        height = (
            self.TEST_TILES_HEIGHT if self.is_test_mode() else self.LIVE_TILES_HEIGHT
        )
        robot_positions: Dict[Tuple[int, int], int] = defaultdict(int)
        for robot in robots:
            robot_positions[(robot.cur_x, robot.cur_y)] += 1
        for x in range(width):
            line = []
            for y in range(height):
                if (x, y) in robot_positions:
                    line.append("*")
                else:
                    line.append(".")
            print("".join(line))
