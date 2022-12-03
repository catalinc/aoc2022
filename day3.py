from string import ascii_letters
from typing import Iterator

# part 1
def find_duplicate(rucksack: str) -> str:
    mid = len(rucksack) // 2
    first, second = rucksack[:mid], rucksack[mid:]
    for item in first:
        if item in second:
            return item

def priority(item: str) -> int:
    return ascii_letters.index(item) + 1

import sys

fname = sys.argv[1] if len(sys.argv) == 2 else "input/day3.txt"
with open(fname) as infile:
    rucksacks = [line.strip() for line in infile.readlines()]

total_priorities = 0
for r in rucksacks:
    total_priorities += priority(find_duplicate(r))
print(total_priorities)

# part 2
def find_badge(rucksack1: str, rucksack2: str, rucksack3: str) -> str:
    for item in rucksack1:
        if item in rucksack2 and item in rucksack3:
            return item

def chunk(l: list, n: int) -> Iterator:
    for i in range(0, len(l), n):
        yield l[i:i+n]

total_priorities = 0
for group in chunk(rucksacks, 3):
    total_priorities += priority(find_badge(group[0], group[1], group[2]))
print(total_priorities)
