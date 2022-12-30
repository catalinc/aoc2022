from collections import deque, namedtuple
from typing import Iterable

Cube = namedtuple("Cube", ["x", "y", "z"])


def adjacent(a: Cube, b: Cube) -> bool:
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z) == 1


def total_exposed_surface(cubes: list[Cube]) -> int:
    area = {c: 6 for c in cubes}
    for i, c1 in enumerate(cubes):
        if area[c1] > 0:  # has sides exposed
            for c2 in cubes[i + 1 :]:
                if adjacent(c1, c2):
                    area[c1] -= 1
                    area[c2] -= 1
                    if area[c1] == 0:  # no sides exposed
                        break
    return sum(area.values())


def parse_input(filename: str) -> list[Cube]:
    with open(filename) as infile:
        return [eval(f"Cube({line})") for line in infile.read().splitlines()]


# part 1
droplet = parse_input("input/day18.txt")
print(total_exposed_surface(droplet))

# part 2
droplet = set(droplet)


def neighbours(cube: Cube) -> Iterable[Cube]:
    for dx in (-1, 1):
        yield Cube(cube.x + dx, cube.y, cube.z)
    for dy in (-1, 1):
        yield Cube(cube.x, cube.y + dy, cube.z)
    for dz in (-1, 1):
        yield Cube(cube.x, cube.y, cube.z + dz)


def bounding_box(droplet: Iterable[Cube]) -> tuple[Cube, Cube]:
    min_x = min_y = min_z = float("inf")
    max_x = max_y = max_z = float("-inf")
    for c in droplet:
        min_x = min(min_x, c.x)
        min_y = min(min_y, c.y)
        min_z = min(min_z, c.z)
        max_x = max(max_x, c.x)
        max_y = max(max_y, c.y)
        max_z = max(max_z, c.z)
    return Cube(min_x - 1, min_y - 1, min_z - 1), Cube(max_x + 1, max_y + 1, max_z + 1)


def lava_exposed_surface(droplet: set[Cube]):
    lava_surface = 0
    min_cube, max_cube = bounding_box(droplet)
    visited, queue = set(), deque()
    queue.append(min_cube)
    while queue:
        cube = queue.popleft()
        for c in neighbours(cube):
            if c in visited:
                continue
            if c.x < min_cube.x or c.y < min_cube.y or c.z < min_cube.z:
                continue
            if c.x > max_cube.x or c.y > max_cube.y or c.z > max_cube.z:
                continue
            if c in droplet:
                lava_surface += 1
            else:
                visited.add(c)
                queue.append(c)
    return lava_surface


print(lava_exposed_surface(droplet))
