import re
from collections import namedtuple
import sys
from typing import Iterable

Point = namedtuple("Point", ["x", "y"])
Sensor = namedtuple("Sensor", ["sensor", "beacon", "radius"])
Rect = namedtuple("Rect", ["min_x", "min_y", "max_x", "max_y"])


def distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def parse_sensor(s: str) -> Sensor:
    sx, sy, bx, by = [int(x) for x in re.findall(r"(\-?\d+)", s)]
    sensor = Point(sx, sy)
    beacon = Point(bx, by)
    radius = distance(sensor, beacon)
    return Sensor(sensor, beacon, radius)


def grid_bounds(grid: Iterable[Sensor]) -> Rect:
    min_x, min_y = float("inf"), float("inf")
    max_x, max_y = float("-inf"), float("-inf")
    for s in grid:
        min_x = min(min_x, s.sensor.x - s.radius, s.beacon.x)
        min_y = min(min_y, s.sensor.y - s.radius, s.beacon.y)
        max_x = max(max_x, s.sensor.x + s.radius, s.beacon.x)
        max_y = max(max_y, s.sensor.y + s.radius, s.beacon.y)
    return Rect(min_x, min_y, max_x, max_y)


fname = sys.argv[1] if len(sys.argv) == 2 else "input/day15.txt"
with open(fname) as infile:
    lines = infile.read().splitlines()
    row = int(lines[0])
    ymax = int(lines[1])
    grid = [parse_sensor(l) for l in lines[2:]]
    bounds = grid_bounds(grid)
    all_sensors = set(s.sensor for s in grid)
    all_beacons = set(s.beacon for s in grid)
    sensor_and_beacons = all_beacons | all_sensors


def is_detectable(p: Point) -> bool:
    if p in sensor_and_beacons:
        return False
    for s in grid:
        if distance(p, s.sensor) <= s.radius:
            return True
    return False


def count_pos_beacon_cannot_exist() -> int:
    cnt = 0
    for x in range(bounds.min_x, bounds.max_x + 1):
        b = Point(x, row)
        if is_detectable(b):
            cnt += 1
    return cnt


# part 1
print(count_pos_beacon_cannot_exist())

# part 2
DIR = [(-1, -1), (-1, 1), (1, 1), (1, -1)]


def perimeter(sensor: Sensor) -> Iterable[Point]:
    x, y = sensor.sensor.x + sensor.radius + 1, sensor.sensor.y
    for dx, dy in DIR:
        for step in range(0, sensor.radius + 1):
            yield Point(x, y)
            if step != sensor.radius:
                x += dx
                y += dy


def find_distress_beacon() -> Point:
    for s in grid:
        for p in perimeter(s):
            if not is_detectable(p):
                if 0 <= p.x <= ymax and 0 <= p.y <= ymax and p not in sensor_and_beacons:
                    return p


db = find_distress_beacon()
print(db.x * 4000000 + db.y)
