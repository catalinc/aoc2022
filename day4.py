import re
from collections import namedtuple

Range = namedtuple("Range", ["start", "end"])

def range_fully_contains(r1: Range, r2: Range) -> bool:
    return (r1.start >= r2.start and r1.end <= r2.end) or (
        r2.start >= r1.start and r2.end <= r1.end
    )

def parse_range_pair(s: str) -> tuple[Range, Range]:
    s1, e1, s2, e2 = map(int, re.findall(r"\d+", s))
    return Range(s1, e1), Range(s2, e2)

def range_overlap(r1: Range, r2: Range) -> bool:
    if r1.start > r2.end or r2.start > r1.end:
        return False
    return True

import sys
fname = sys.argv[1] if len(sys.argv) == 2 else "input/day4.txt"
with open(fname) as infile:
    range_pairs = list(map(parse_range_pair, infile.readlines()))

# part 1 & 2
fully_contains = 0
overlaps = 0
for rp in range_pairs:
    if range_fully_contains(rp[0], rp[1]):
        fully_contains += 1
    if range_overlap(rp[0], rp[1]):
        overlaps += 1
print(f"{fully_contains}\n{overlaps}")
