from collections import deque
import re
from typing import Iterable


class Monkey:
    def __init__(
        self,
        id: int,
        items: Iterable[int],
        op: str,
        test_div: int,
        test_true: int,
        test_false: int,
    ) -> None:
        self.id = id
        self.items = deque(items)
        self.op = op
        self.test_div = test_div
        self.test_true = test_true
        self.test_false = test_false
        self.inspected = 0

    def play(self, gang: list["Monkey"], stress_mgmt_fn=None):
        while self.items:
            self.inspected += 1
            x = self.items.popleft()
            w = eval(self.op.replace("old", str(x)))
            if stress_mgmt_fn:
                w = stress_mgmt_fn(w)
            else:
                w //= 3
            if w % self.test_div == 0:
                gang[self.test_true].items.append(w)
            else:
                gang[self.test_false].items.append(w)

    def __repr__(self) -> str:
        return f"{self.id} {self.inspected}"


def parse_monkey(s: str) -> Monkey:
    lines = s.splitlines()
    id = int(re.findall(r"\d+", lines[0])[0])
    items = map(int, re.findall(r"\d+", lines[1]))
    op = lines[2].split(" = ")[1]
    test_div = int(lines[3].split(" ")[-1])
    test_true = int(lines[4].split(" ")[-1])
    test_false = int(lines[5].split(" ")[-1])
    return Monkey(id, items, op, test_div, test_true, test_false)


import sys

fname = sys.argv[1] if len(sys.argv) == 2 else "input/day11.txt"
with open(fname) as infile:
    orig_gang = [parse_monkey(s) for s in infile.read().split("\n\n")]

# part 1
import copy

gang = copy.deepcopy(orig_gang)
for _ in range(20):
    for m in gang:
        m.play(gang)
gang.sort(key=lambda m: m.inspected, reverse=True)
print(gang[0].inspected * gang[1].inspected)

# part 2
from math import prod

max_w = prod(m.test_div for m in orig_gang)
for _ in range(10_000):
    for m in orig_gang:
        m.play(orig_gang, lambda w: w % max_w)
orig_gang.sort(key=lambda m: m.inspected, reverse=True)
print(orig_gang[0].inspected * orig_gang[1].inspected)
