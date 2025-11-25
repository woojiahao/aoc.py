from collections import deque
from typing import Any, Deque, List, Optional, Tuple

from ..solution import Solution


class FragmentNode:
    def __init__(self, start: int, length: int) -> None:
        self.start = start
        self.length = length
        self.prev: Optional["FragmentNode"] = None
        self.next: Optional["FragmentNode"] = None

    def __repr__(self) -> str:
        return f"[{self.start}/{self.length}]"


class FragmentList:
    def __init__(self) -> None:
        self.head = FragmentNode(-1, -1)
        self.tail = FragmentNode(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head

    def insert_end(self, node: FragmentNode) -> None:
        tail_prev = self.tail.prev
        assert tail_prev is not None
        tail_prev.next = node
        node.prev = tail_prev
        self.tail.prev = node
        node.next = self.tail

    def pop_node(self, node: FragmentNode) -> FragmentNode:
        node_prev = node.prev
        node_next = node.next
        assert node_prev is not None
        assert node_next is not None
        node_prev.next = node_next
        node_next.prev = node_prev
        node.next = None
        node.prev = None
        return node_prev

    def insert_ahead(self, target: FragmentNode, node: FragmentNode) -> None:
        target_next = target.next
        assert target_next is not None
        target.next = node
        node.next = target_next
        target_next.prev = node
        node.prev = target

    def __repr__(self) -> str:
        cur = self.head.next
        ll = []
        while cur != self.tail:
            assert cur is not None
            ll.append(repr(cur))
            cur = cur.next
        return " -> ".join(ll)


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
        empty: FragmentList = FragmentList()

        # Behaves as a stack for end most available slots
        filled: List[Tuple[int, int, int]] = []

        is_file = True
        i = 0
        id = 0
        for d in data:
            if is_file:
                if d != 0:
                    filled.append((id, i, d))
                id += 1
            else:
                if d != 0:
                    empty.insert_end(FragmentNode(i, d))
            i += d
            is_file = not is_file

        compacted_positions = []
        j = len(filled) - 1
        while j >= 0 and empty:
            last_block_id, last_block_start, last_block_length = filled.pop()
            cur = empty.head.next
            while cur != empty.tail:
                assert cur is not None
                cur_next = cur.next
                if cur.start < last_block_start and cur.length >= last_block_length:
                    remaining = cur.length - last_block_length
                    compacted_positions.append(
                        (last_block_id, cur.start, last_block_length)
                    )
                    if remaining == 0:
                        empty.pop_node(cur)
                    else:
                        cur.start += last_block_length
                        cur.length = remaining
                    break
                cur = cur_next
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
