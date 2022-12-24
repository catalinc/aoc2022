from collections import namedtuple
from itertools import pairwise

Block = namedtuple("Block", ["x", "y"])


class Rock:
    def __init__(self, start_x: int = 3) -> None:
        self.blocks: list[Block] = []
        self.start_x = start_x

    def bottom(self) -> int:
        return min(b.y for b in self.blocks)

    def top(self) -> int:
        return max(b.y for b in self.blocks)

    def left(self) -> int:
        return min(b.x for b in self.blocks)

    def right(self) -> int:
        return max(b.x for b in self.blocks)

    def move_down(self) -> "Rock":
        rock = Rock()
        for b in self.blocks:
            rock.blocks.append(Block(b.x, b.y - 1))
        return rock

    def move_right(self) -> "Rock":
        rock = Rock()
        for b in self.blocks:
            rock.blocks.append(Block(b.x + 1, b.y))
        return rock

    def move_left(self) -> int:
        rock = Rock()
        for b in self.blocks:
            rock.blocks.append(Block(b.x - 1, b.y))
        return rock


class HBar(Rock):
    def __init__(self, bottom: int) -> None:
        super().__init__()
        for x in range(self.start_x, self.start_x + 4):
            self.blocks.append(Block(x, bottom))


class VBar(Rock):
    def __init__(self, bottom: int) -> None:
        super().__init__()
        for y in range(bottom, bottom + 4):
            self.blocks.append(Block(self.start_x, y))


class ReverseL(Rock):
    def __init__(self, bottom: int) -> None:
        super().__init__()
        for y in range(bottom, bottom + 3):
            self.blocks.append(Block(self.start_x + 2, y))
        self.blocks.append(Block(self.start_x, bottom))
        self.blocks.append(Block(self.start_x + 1, bottom))


class Cross(Rock):
    def __init__(self, bottom: int) -> None:
        super().__init__()
        for y in range(bottom, bottom + 3):
            self.blocks.append(Block(self.start_x + 1, y))
        self.blocks.append(Block(self.start_x, bottom + 1))
        self.blocks.append(Block(self.start_x + 2, bottom + 1))


class Square(Rock):
    def __init__(self, bottom: int) -> None:
        super().__init__()
        self.blocks.append(Block(self.start_x, bottom))
        self.blocks.append(Block(self.start_x + 1, bottom))
        self.blocks.append(Block(self.start_x, bottom + 1))
        self.blocks.append(Block(self.start_x + 1, bottom + 1))


class Chamber:
    def __init__(self, width: int = 7) -> None:
        self.floor: set[Block] = set()
        self.width = width

    def land_shape(self, rock: Rock) -> bool:
        for br in rock.blocks:
            if Block(br.x, br.y - 1) in self.floor:
                for b in rock.blocks:
                    self.floor.add(b)
                return True
        if rock.bottom() == 1:
            for b in rock.blocks:
                self.floor.add(b)
            return True
        return False

    def max_heigh(self) -> int:
        if not self.floor:
            return 0
        return max(b.y for b in self.floor)

    def valid(self, rock: Rock) -> bool:
        if rock.left() < 1 or rock.right() > self.width:
            return False
        if any(b in self.floor for b in rock.blocks):
            return False
        return True


def print_chamber(chamber: Chamber, rock: Rock = None):
    nrows = chamber.max_heigh() + 5
    if rock:
        nrows = max(rock.top() + 1, nrows)
    ncols = chamber.width + 2
    buffer = [["." for _ in range(ncols)] for _ in range(nrows)]
    for i in range(nrows):
        buffer[i][0] = buffer[i][ncols - 1] = "|"
    for i in range(ncols):
        buffer[0][i] = "-"
    buffer[0][0] = buffer[0][ncols - 1] = "+"
    for b in chamber.floor:
        buffer[b.y][b.x] = "#"
    if rock:
        for b in rock.blocks:
            buffer[b.y][b.x] = "@"
    buffer.reverse()
    output = "\n".join(["".join(line) for line in buffer])
    print(output)


class RockGenerator:
    def __init__(self, chamber: Chamber) -> None:
        self.chamber = chamber
        self.seq: tuple[str] = ("HBar", "Cross", "ReverseL", "VBar", "Square")
        self.index = 0

    def next(self) -> Rock:
        bottom = self.chamber.max_heigh() + 4
        rock = eval(f"{self.seq[self.index]}({bottom})")
        self.index = (self.index + 1) % len(self.seq)
        return rock


class GasJet:
    def __init__(self, seq: str) -> None:
        self.seq = seq
        self.index = 0

    def push(self) -> str:
        d = self.seq[self.index]
        self.index = (self.index + 1) % len(self.seq)
        return d


class Simulation:
    def __init__(self, jet_seq: str) -> None:
        self.gas_jet = GasJet(jet_seq)
        self.chamber = Chamber()
        self.rock_gen = RockGenerator(self.chamber)
        self.max_heigh_hist = []

    def run(self, max_rocks: int) -> int:
        for _ in range(max_rocks):
            self.max_heigh_hist.append(self.chamber.max_heigh())
            rock = self.rock_gen.next()
            while True:
                d = self.gas_jet.push()
                if d == ">":
                    new_rock = rock.move_right()
                    if self.chamber.valid(new_rock):
                        rock = new_rock
                if d == "<":
                    new_rock = rock.move_left()
                    if self.chamber.valid(new_rock):
                        rock = new_rock
                if self.chamber.land_shape(rock):
                    break
                rock = rock.move_down()
        max_h = self.chamber.max_heigh()
        self.max_heigh_hist.append(max_h)
        return max_h


def read_input(filename: str) -> str:
    with open(filename) as infile:
        return infile.read().rstrip()


# part 1

jet_seq = read_input("input/day17.txt")
sim = Simulation(jet_seq)
print(sim.run(2022))

# part 2


def find_pattern(data: list[int]) -> tuple[list[int], list[int]]:
    for i in range(len(data)):
        tail = data[i:]
        for j in range(2, len(tail) // 2):
            if tail[0:j] == tail[j : 2 * j]:
                if all(
                    [(tail[0:j] == tail[k : k + j]) for k in range(j, len(tail) - j, j)]
                ):
                    return data[:i], data[i : i + j]
    return [], []


def find_max_heigh(jet_seq: str, num_rocks: int, sample_size: int = 10000) -> int:
    sim = Simulation(jet_seq)
    sim.run(sample_size)

    max_height_deltas = [p[1] - p[0] for p in pairwise(sim.max_heigh_hist)]
    pre, rep = find_pattern(max_height_deltas)
    return (
        sum(pre)
        + sum(rep) * ((num_rocks - len(pre)) // len(rep))
        + sum(rep[: ((num_rocks - len(pre)) % len(rep))])
    )

print(find_max_heigh(jet_seq, 1000000000000))
