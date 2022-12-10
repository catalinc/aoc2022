from math import floor
from typing import Optional, Union


class Noop:
    def __init__(self) -> None:
        self.cycles = 1

    def execute(self, _: "CPU") -> None:
        self.cycles -= 1
        pass

    def done(self) -> bool:
        return self.cycles == 0


class AddX:
    def __init__(self, v: int) -> None:
        self.v = v
        self.cycles = 2

    def execute(self, cpu: "CPU") -> None:
        self.cycles -= 1
        if self.cycles == 0:
            cpu.x += self.v

    def done(self) -> bool:
        return self.cycles == 0


class SignalStrengthCalc:
    def __init__(self) -> None:
        self.signal_strengths = []

    def on_cycle(self, cpu: "CPU"):
        if cpu.cycle in (20, 60, 100, 140, 180, 220):
            self.signal_strengths.append(cpu.cycle * cpu.x)


class CPU:
    def __init__(self) -> None:
        self.x = 1
        self.cycle = 0

    def run_program(
        self, prog: str, obs: Optional[Union[SignalStrengthCalc, "CRT"]] = None
    ) -> None:
        lines = [l for l in prog.splitlines() if l]
        for l in lines:
            instr = self.decode(l)
            while not instr.done():
                self.cycle += 1
                if obs:
                    obs.on_cycle(self)
                instr.execute(self)

    def decode(self, line: str) -> Union[Noop, AddX]:
        if line.startswith("noop"):
            return Noop()
        if line.startswith("addx"):
            return AddX(int(line.split(" ")[1]))


import sys

fname = sys.argv[1] if len(sys.argv) == 2 else "input/day10.txt"
with open(fname) as infile:
    program = infile.read()

# part 1
ssc = SignalStrengthCalc()
cpu = CPU()
cpu.run_program(program, ssc)
print(sum(ssc.signal_strengths))

# part 2
class CRT:
    def __init__(self) -> None:
        self.beam = 0
        self.pixels = [["." for _ in range(40)] for _ in range(6)]

    def on_cycle(self, cpu: CPU) -> None:
        sprite = (cpu.x - 1, cpu.x, cpu.x + 1)
        row = floor(self.beam / 40)
        col = self.beam % 40
        self.pixels[row][col] = "#" if col in sprite else "."
        self.beam = (self.beam + 1) % 240

    def __repr__(self) -> str:
        return "\n".join(("".join(line) for line in self.pixels))


crt = CRT()
cpu = CPU()
cpu.run_program(program, crt)
print(crt)
