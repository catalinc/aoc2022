from collections import deque

import sys
import re


def parse_crate_stacks(lines: list[str]) -> list[deque[str]]:
    nstacks = int(re.findall(r"(.{3})\s?", lines[-1])[-1])
    stacks = [deque() for _ in range(nstacks)]
    for l in lines[:-1]:
        tops = re.findall(r"(.{3})\s?", l)
        for i, t in enumerate(tops):
            if t[0] == "[":
                stacks[i].appendleft(t[1])
    return stacks


def parse_crane_moves(lines: list[str]) -> list[tuple[int, int, int]]:
    moves = []
    for l in lines:
        cnt, src, dst = map(int, re.findall(r"\d+", l))
        moves.append((cnt, src - 1, dst - 1))
    return moves


# part 1
fname = sys.argv[1] if len(sys.argv) == 2 else "input/day5.txt"
with open(fname) as infile:
    content = infile.read()
    first, second = [
        [line for line in section.split("\n") if line]
        for section in re.split(r"\n\n", content)
    ]
    crate_stacks = parse_crate_stacks(first)
    crane_moves = parse_crane_moves(second)


def crate_mover9000_do_move(stacks: list[deque[str]], move: tuple[int, int, int]):
    cnt, src, dst = move
    for _ in range(cnt):
        stacks[dst].append(stacks[src].pop())


def move_crates(
    stacks: list[deque[str]], moves: list[tuple[int, int, int]], move_fn
) -> str:
    for m in moves:
        move_fn(stacks, m)
    return "".join(st[-1] for st in stacks)

import copy
crate_stacks_copy = copy.deepcopy(crate_stacks)
print(move_crates(crate_stacks_copy, crane_moves, crate_mover9000_do_move))

# part 2
def crate_mover9001_do_move(stacks: list[deque[str]], move: tuple[int, int, int]):
    cnt, src, dst = move
    to_move = [stacks[src].pop() for _ in range(cnt)]
    for c in reversed(to_move):
        stacks[dst].append(c)


print(move_crates(crate_stacks, crane_moves, crate_mover9001_do_move))
