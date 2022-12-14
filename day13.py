def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return left - right
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]
    for l, r in zip(left, right):
        if (c := compare(l, r)) != 0:
            return c
    if len(left) < len(right):
        return -1
    if len(left) > len(right):
        return 1
    return 0


from functools import cmp_to_key
from itertools import chain
import sys

packets = []
fname = sys.argv[1] if len(sys.argv) == 2 else "input/day13.txt"
with open(fname) as infile:
    sections = infile.read().split("\n\n")
    for s in sections:
        lines = s.splitlines()
        packets.append((eval(lines[0]), eval(lines[1])))

# part 1
ordered = []
for i, pair in enumerate(packets, 1):
    left, right = pair
    if compare(left, right) < 0:
        ordered.append(i)
print(sum(ordered))

# part 2
packets = list(chain(*packets))
packets.append([[2]])
packets.append([[6]])
packets.sort(key=cmp_to_key(compare))
key = 1
for i, p in enumerate(packets, 1):
    if p in ([[2]], [[6]]):
        key *= i
print(key)
