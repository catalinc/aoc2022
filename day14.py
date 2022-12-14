import sys
import re
from collections import namedtuple
from typing import Iterable, Iterator


Point = namedtuple("Point", ["x", "y"])
Wall = namedtuple("Wall", ["start", "end"])
Bounds = namedtuple("Bounds", ["top", "bottom"])


class Cave:
    def __init__(self, walls: Iterable[Wall]) -> None:
        self.rocks: set[Point] = set()
        for w in walls:
            start, end = w
            if start.x == end.x:
                x = start.x
                start_y = start.y if start.y < end.y else end.y
                end_y = start.y if start.y > end.y else end.y
                for y in range(start_y, end_y + 1):
                    self.rocks.add(Point(x, y))
            elif start.y == end.y:
                y = start.y
                start_x = start.x if start.x < end.x else end.x
                end_x = start.x if start.x > end.x else end.x
                for x in range(start_x, end_x + 1):
                    self.rocks.add(Point(x, y))
        min_x = min(r.x for r in self.rocks)
        min_y = min(r.y for r in self.rocks)
        max_x = max(r.x for r in self.rocks)
        max_y = max(r.y for r in self.rocks)
        top = Point(min_x, min_y)
        bottom = Point(max_x, max_y)
        self.bounds: Bounds = Bounds(top, bottom)
        self.floor = Point(0, self.bounds.bottom.y + 2)

    def is_rock(self, p: Point) -> bool:
        return p in self.rocks

    def is_endless_void(self, p: Point) -> bool:
        return (
            p.x < self.bounds.top.x
            or p.x > self.bounds.bottom.x
            or p.y > self.bounds.bottom.y
        )

    def is_on_floor(self, p: Point) -> bool:
        return (p.y + 1) == self.floor.y


class SandSimulator:
    def __init__(self, emiter: Point, cave: Cave) -> None:
        self.emiter = emiter
        self.cave = cave

    def run(self):
        cnt = 0
        sand = Point(self.emiter.x, self.emiter.y)
        while True:
            if self.cave.is_endless_void(sand):
                return cnt
            down = Point(sand.x, sand.y + 1)
            if self.cave.is_rock(down):
                left = Point(sand.x - 1, sand.y + 1)
                if self.cave.is_rock(left):
                    right = Point(sand.x + 1, sand.y + 1)
                    if self.cave.is_rock(right):
                        self.cave.rocks.add(sand)
                        sand = Point(self.emiter.x, self.emiter.y)
                        cnt += 1
                    else:
                        sand = right
                else:
                    sand = left
            else:
                sand = down


def chunk(l: list, n: int) -> Iterator:
    for i in range(0, len(l), n):
        yield l[i : i + n]


fname = sys.argv[1] if len(sys.argv) == 2 else "input/day14.txt"
with open(fname) as infile:
    walls = []
    for l in infile.read().splitlines():
        coords = [int(x) for x in re.findall(r"\d+", l)]
        points = []
        for x, y in chunk(coords, 2):
            points.append(Point(x, y))
        for i in range(len(points) - 1):
            start, end = points[i], points[i + 1]
            wall = Wall(start, end)
            walls.append(wall)

# part 1
cave = Cave(walls)
sim = SandSimulator(Point(500, 0), cave)
print(sim.run())

# part 2
class SandSimulatorWithFloor:
    def __init__(self, emiter: Point, cave: Cave) -> None:
        self.emiter = emiter
        self.cave = cave

    def run(self):
        cnt = 0
        sand = Point(self.emiter.x, self.emiter.y)
        while True:
            if self.cave.is_on_floor(sand):
                self.cave.rocks.add(sand)
                sand = Point(self.emiter.x, self.emiter.y)
                cnt += 1
            else:
                down = Point(sand.x, sand.y + 1)
                if self.cave.is_rock(down):
                    left = Point(sand.x - 1, sand.y + 1)
                    if self.cave.is_rock(left):
                        right = Point(sand.x + 1, sand.y + 1)
                        if self.cave.is_rock(right):
                            if sand == self.emiter:
                                cnt += 1
                                return cnt
                            self.cave.rocks.add(sand)
                            sand = Point(self.emiter.x, self.emiter.y)
                            cnt += 1
                        else:
                            sand = right
                    else:
                        sand = left
                else:
                    sand = down

cave = Cave(walls)
sim = SandSimulatorWithFloor(Point(500, 0), cave)
print(sim.run())

