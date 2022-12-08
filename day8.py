import sys

fname = sys.argv[1] if len(sys.argv) == 2 else "input/day8.txt"
with open(fname) as infile:
    grid = [[int(x) for x in line] for line in infile.read().splitlines() if line]

# part 1
def is_visible(row: int, col: int, grid: list[list[int]]) -> bool:
    if row == 0 or row == len(grid) - 1:
        return True
    if col == 0 or col == len(grid[0]) - 1:
        return True
    # from top
    vis = True
    for i in range(0, row):
        if grid[i][col] >= grid[row][col]:
            vis = False
            break
    if vis:
        return True
    # from bottom
    vis = True
    for i in range(row + 1, len(grid)):
        if grid[i][col] >= grid[row][col]:
            vis = False
            break
    if vis:
        return True
    # from left
    vis = True
    for i in range(0, col):
        if grid[row][i] >= grid[row][col]:
            vis = False
            break
    if vis:
        return True
    # from right
    vis = True
    for i in range(col + 1, len(grid[0])):
        if grid[row][i] >= grid[row][col]:
            vis = False
            break
    return vis


def count_visible(grid: list[list[int]]) -> int:
    nrows, ncols = len(grid), len(grid[0])
    visible = 0
    for i in range(nrows):
        for j in range(ncols):
            if is_visible(i, j, grid):
                visible += 1
    return visible


print(count_visible(grid))

# part 2
def get_scenic_score(row: int, col: int, grid: list[list[int]]):
    if row == 0 or row == len(grid) - 1:
        return 0
    if col == 0 or col == len(grid[0]) - 1:
        return 0
    up_score = 0
    for i in range(row - 1, -1, -1):
        up_score += 1
        if grid[i][col] >= grid[row][col]:
            break
    down_score = 0
    for i in range(row + 1, len(grid)):
        down_score += 1
        if grid[i][col] >= grid[row][col]:
            break
    left_score = 0
    for i in range(col - 1, -1, -1):
        left_score += 1
        if grid[row][i] >= grid[row][col]:
            break
    right_score = 0
    for i in range(col + 1, len(grid[0])):
        right_score += 1
        if grid[row][i] >= grid[row][col]:
            break
    return up_score * down_score * left_score * right_score


def get_max_scenic_score(grid: list[list[int]]):
    max_score = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            max_score = max(max_score, get_scenic_score(i, j, grid))
    return max_score


print(get_max_scenic_score(grid))
