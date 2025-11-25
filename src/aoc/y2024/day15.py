import os
from typing import Any, Dict, List, Set, Tuple

from aoc.utils.spatial import Col, RCCoord, Row

from ..solution import Solution

from dataclasses import dataclass, field

DIRECTION_MAP = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}


@dataclass
class Map:
    robot_r: Row
    robot_c: Col

    width: int
    height: int

    directions: List[str]
    boxes: Set[RCCoord]
    walls: Set[RCCoord]

    def move(self, direction: str) -> None:
        # Check if pushing against wall, if so, ignore direction
        dr, dc = DIRECTION_MAP[direction]
        nr, nc = self.robot_r + dr, self.robot_c + dc
        if (nr, nc) in self.walls:
            return

        # Check if next spot is open, move in that direction and be done
        if (nr, nc) not in self.boxes:
            self.robot_r = nr
            self.robot_c = nc
            return

        # Pushing against box, if so, push box(es) in direction till wall is found
        # 1. Check for the box in the given direction
        # 2. Keep searching for boxes in the same direction till (a) hit a wall or
        # (b) find empty space
        # 3. If (a), skip
        # 4. If (b), move all boxes and robot in direction
        space_r, space_c = nr, nc
        boxes_to_move = []
        while True:
            if (space_r, space_c) in self.boxes:
                boxes_to_move.append((space_r, space_c))
                space_r += dr
                space_c += dc
            elif (space_r, space_c) in self.walls:
                # Hit a wall
                return
            else:
                break

        new_boxes = {box: 1 for box in self.boxes}
        for box in boxes_to_move:
            new_box_coord = (box[0] + dr, box[1] + dc)
            new_boxes[new_box_coord] = new_boxes.get(new_box_coord, 0) + 1
            new_boxes[box] -= 1
        self.boxes = set([k for k in new_boxes.keys() if new_boxes[k] > 0])
        self.robot_r = nr
        self.robot_c = nc

    def print(self) -> None:
        for i in range(self.height):
            line = []
            for j in range(self.width):
                if (i, j) in self.walls:
                    line.append("#")
                elif (i, j) in self.boxes:
                    line.append("O")
                elif (i, j) == (self.robot_r, self.robot_c):
                    line.append("@")
                else:
                    line.append(".")
            print("".join(line))

    def print_steps(self) -> None:
        os.system("clear")
        print("[Initial] Starting out")
        self.print()
        input("Press ENTER")
        for i, direction in enumerate(self.directions):
            os.system("clear")
            print(f"[{i + 1}] Going in {direction}")
            self.move(direction)
            self.print()
            input("Press ENTER")


class Y2024Day15(Solution):
    def parse_data(self, contents: str) -> Any:
        [map_raw, directions_raw] = contents.strip().split("\n\n")
        map_parsed = [list(line) for line in map_raw.split("\n")]
        height = len(map_parsed)
        width = len(map_parsed[0])
        robot_r, robot_c = -1, -1
        boxes = set()
        walls = set()
        for i in range(height):
            for j in range(width):
                if map_parsed[i][j] == "@":
                    robot_r, robot_c = i, j
                elif map_parsed[i][j] == "O":
                    boxes.add((i, j))
                elif map_parsed[i][j] == "#":
                    walls.add((i, j))
        directions = list(c for r in directions_raw.split("\n") for c in r)
        return Map(
            robot_r=robot_r,
            robot_c=robot_c,
            width=width,
            height=height,
            boxes=boxes,
            walls=walls,
            directions=directions,
        )

    def solve_one(self, data: Map) -> Any:
        for direction in data.directions:
            data.move(direction)
        ans = 0
        for box in data.boxes:
            ans += box[0] * 100 + box[1]
        return ans

    def solve_two(self, data: Any) -> Any:
        pass
