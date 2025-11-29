import multiprocessing
import os
from typing import Any, List, Tuple

from ..solution import Solution


class Computer:
    def __init__(
        self, instructions: List[int], register_a: int, register_b: int, register_c: int
    ):
        self.instructions = instructions
        self.instruction_ptr = 0
        self.A = register_a
        self.B = register_b
        self.C = register_c
        self.outputs: List[int] = []

    def run(self):
        while self.instruction_ptr < len(self.instructions):
            instruction = self.instructions[self.instruction_ptr]
            match instruction:
                case 0:
                    self.adv()
                case 1:
                    self.bxl()
                case 2:
                    self.bst()
                case 3:
                    self.jnz()
                case 4:
                    self.bxc()
                case 5:
                    self.out()
                case 6:
                    self.bdv()
                case 7:
                    self.cdv()
        return ",".join([str(o) for o in self.outputs])

    def get_combo_operand(self) -> int:
        operand = self.instructions[self.instruction_ptr + 1]
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
        return 0

    def get_literal_operand(self) -> int:
        return self.instructions[self.instruction_ptr + 1]

    def adv(self):
        numerator = self.A
        denominator = 2 ** self.get_combo_operand()
        self.A = int(numerator / denominator)
        self.instruction_ptr += 2

    def bxl(self):
        self.B = self.B ^ self.get_literal_operand()
        self.instruction_ptr += 2

    def bst(self):
        self.B = self.get_combo_operand() % 8
        self.instruction_ptr += 2

    def jnz(self):
        if self.A == 0:
            self.instruction_ptr += 2
            return
        self.instruction_ptr = self.get_literal_operand()

    def bxc(self):
        self.B = self.B ^ self.C
        self.instruction_ptr += 2

    def out(self):
        output = self.get_combo_operand() % 8
        self.outputs.append(output)
        self.instruction_ptr += 2

    def bdv(self):
        numerator = self.A
        denominator = 2 ** self.get_combo_operand()
        self.B = int(numerator / denominator)
        self.instruction_ptr += 2

    def cdv(self):
        numerator = self.A
        denominator = 2 ** self.get_combo_operand()
        self.C = int(numerator / denominator)
        self.instruction_ptr += 2

    @staticmethod
    def from_computer(other: "Computer", new_A: int):
        return Computer(other.instructions[:], new_A, other.B, other.C)


def process_chunk(args):
    chunk_start, chunk_size, expected, data = args
    chunk_end = chunk_start + chunk_size
    for new_A in range(chunk_start, chunk_end + 1):
        if new_A % 1_000_000 == 0:
            pid = os.getpid()
            print(f"Processor [{pid}] {new_A}")
        new_computer = Computer.from_computer(data, new_A)
        if new_computer.run() == expected:
            return new_A
    return None


class Y2024Day17(Solution):
    def parse_data(self, contents: str) -> Any:
        [registers_raw, program_raw] = contents.strip().split("\n\n")
        [register_a, register_b, register_c] = [
            int(register.split(" ")[2]) for register in registers_raw.split("\n")
        ]
        program_instructions = [int(v) for v in program_raw.split(" ")[1].split(",")]

        return Computer(program_instructions, register_a, register_b, register_c)

    def solve_one(self, data: Computer) -> Any:
        return data.run()

    def solve_two(self, data: Computer) -> Any:
        A = 0
        for i in reversed(range(len(data.instructions))):
            A <<= 3
            new_computer = Computer.from_computer(data, A)
            while [int(v) for v in new_computer.run().split(",")] != data.instructions[
                i:
            ]:
                A += 1
                new_computer = Computer.from_computer(data, A)
        return A
