from collections import namedtuple
from math import sqrt

Offset = namedtuple("Offset", ["dx", "dy"])
Point = namedtuple("Point", ["x", "y"])
Move = namedtuple("Move", ["direction", "steps"])

DIRECTIONS = {
    "U": Offset(0, 1),
    "D": Offset(0, -1),
    "R": Offset(1, 0),
    "L": Offset(-1, 0),
}


def distance(p1: Point, p2: Point) -> int:
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    return round(sqrt(dx * dx + dy * dy))


def unit_direction(p1: Point, p2: Point) -> Offset:
    x = p1.x - p2.x
    y = p1.y - p2.y
    dx = x // abs(x) if x != 0 else 0
    dy = y // abs(y) if y != 0 else 0
    return Offset(dx, dy)


def move_point(p: Point, d: str) -> Point:
    o = DIRECTIONS[d]
    return Point(p.x + o.dx, p.y + o.dy)


def offset_point(p: Point, o: Offset) -> Point:
    return Point(p.x + o.dx, p.y + o.dy)


class Rope:
    def __init__(self, num_knots: int = 2) -> None:
        self.knots = [Point(0, 0) for _ in range(num_knots)]
        self.visited = set([self.knots[-1]])

    def move(self, m: Move) -> None:
        for _ in range(m.steps):
            head = self.knots[0]
            head = move_point(head, m.direction)
            self.knots[0] = head
            i = 1
            while i < len(self.knots):
                head = self.knots[i - 1]
                tail = self.knots[i]
                dist = distance(head, tail)
                if dist > 1:
                    unit = unit_direction(head, tail)
                    tail = offset_point(tail, unit)
                    self.knots[i] = tail
                    if i == len(self.knots) - 1:
                        self.visited.add(tail)
                i += 1


import sys


def parse_move(s: str) -> Move:
    direction, steps = s.split(" ")
    return Move(direction, int(steps))


fname = sys.argv[1] if len(sys.argv) == 2 else "input/day9.txt"
with open(fname) as infile:
    rope_moves = [parse_move(line) for line in infile.read().splitlines() if line]

# part 1 & 2
for n in (2, 10):
    rope = Rope(num_knots=n)
    for m in rope_moves:
        rope.move(m)
    print(len(rope.visited))
