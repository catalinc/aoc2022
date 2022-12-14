from collections import deque


def parse_terrain(grid):
    hmap, start, end = {}, None, None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            ch = grid[i][j]
            if ch == "S":
                start = (i, j)
                hmap[start] = ord("a")
            elif ch == "E":
                end = (i, j)
                hmap[end] = ord("z")
            else:
                hmap[(i, j)] = ord(ch)
    return hmap, start, end


def backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


DIR = ((-1, 0), (1, 0), (0, -1), (0, 1))


def neighbours(node, hmap):
    i, j = node
    for oi, oj in DIR:
        n = (i + oj, j + oi)
        if n in hmap and (hmap[node] >= hmap[n] or hmap[n] - hmap[node] == 1):
            yield n


def find_min_path(hmap, start, end):
    parent = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == end:
            return backtrace(parent, start, end)
        else:
            for adjacent in neighbours(node, hmap):
                if adjacent not in parent:
                    parent[adjacent] = node
                    queue.append(adjacent)


import sys

fname = sys.argv[1] if len(sys.argv) == 2 else "input/day12.txt"
with open(fname) as infile:
    grid = [list(l) for l in infile.read().splitlines()]
    hmap, start, end = parse_terrain(grid)

# part 1
print(len(find_min_path(hmap, start, end)) - 1)

# part 2
min_path_len = float("inf")
min_elevation = ord("a")
# top
for i in range(0, len(grid[0])):
    if hmap[(0, i)] == min_elevation:
        min_path = find_min_path(hmap, (0, i), end)
        if min_path:
            min_path_len = min(len(min_path) - 1, min_path_len)
# left
for i in range(0, len(grid)):
    if hmap[(i, 0)] == min_elevation:
        min_path = find_min_path(hmap, (i, 0), end)
        if min_path:
            min_path_len = min(len(min_path) - 1, min_path_len)
# bottom
for i in range(0, len(grid[0])):
    m = len(grid) - 1
    if hmap[(m, i)] == min_elevation:
        min_path = find_min_path(hmap, (m, i), end)
        if min_path:
            min_path_len = min(len(min_path) - 1, min_path_len)
# right
for i in range(0, len(grid)):
    n = len(grid[0]) - 1
    if hmap[(i, n)] == min_elevation:
        min_path = find_min_path(hmap, (i, n), end)
        if min_path:
            min_path_len = min(len(min_path) - 1, min_path_len)


print(min_path_len)
