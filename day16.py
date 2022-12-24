import re
import sys


def parse_input(puzzle: str):
    cave = {}
    pattern = re.compile(
        r"Valve ([A-Z]{2}) has flow rate=(\d+); "
        r"tunnels? leads? to valves? ((([A-Z]{2}), )*([A-Z]{2}))"
    )

    for line in puzzle.splitlines():
        matcher = pattern.match(line)
        if matcher:
            name = matcher.group(1)
            flow_rate = int(matcher.group(2))
            tunnels = set(matcher.group(3).split(", "))
            valve = Valve(name, flow_rate, tunnels)
            cave[name] = valve

    floyd_warshall = {
        x: {y: 1 if y in cave[x].tunnels else float("inf") for y in cave} for x in cave
    }
    for k in floyd_warshall:
        for i in floyd_warshall:
            for j in floyd_warshall:
                floyd_warshall[i][j] = min(
                    floyd_warshall[i][j], floyd_warshall[i][k] + floyd_warshall[k][j]
                )

    return cave, floyd_warshall


class Valve:
    def __init__(self, name, rate: int, tunnels: set[str]):
        self.name = name
        self.rate = rate
        self.tunnels = tunnels


def solve(
    valves,
    floyd_warshall,
    last_valve,
    time_left,
    state_machine,
    crt_state,
    flow_so_far,
    cache,
):
    cache[crt_state] = max(cache.get(crt_state, 0), flow_so_far)
    for valve in valves:
        minutes = time_left - floyd_warshall[last_valve][valve] - 1
        if (state_machine[valve] & crt_state) or (minutes <= 0):
            continue
        solve(
            valves,
            floyd_warshall,
            valve,
            minutes,
            state_machine,
            crt_state | state_machine[valve],
            flow_so_far + (minutes * valves[valve].rate),
            cache,
        )
    return cache


# part 1 & 2
fname = sys.argv[1] if len(sys.argv) == 2 else "input/day16.txt"
with open(fname) as infile:
    puzzle = infile.read()
    cave, floyd_warshall = parse_input(puzzle)

    non_jammed_valves = {
        name: valve for (name, valve) in cave.items() if valve.rate > 0
    }
    state_machine = {v: 1 << i for i, v in enumerate(non_jammed_valves)}
    last_valve, initial_state, initial_flow = "AA", 0, 0
    max_flow = max(
        solve(
            non_jammed_valves,
            floyd_warshall,
            last_valve,
            30,
            state_machine,
            initial_state,
            initial_flow,
            {},
        ).values()
    )
    print(max_flow)

    cave, floyd_warshall = parse_input(puzzle)
    non_jammed_valves = {
        name: valve for (name, valve) in cave.items() if valve.rate > 0
    }
    state_machine = {v: 1 << i for i, v in enumerate(non_jammed_valves)}
    last_valve, initial_state, initial_flow = "AA", 0, 0
    paths = solve(
        non_jammed_valves,
        floyd_warshall,
        last_valve,
        26,
        state_machine,
        initial_state,
        initial_flow,
        {},
    )
    max_flow = max(
        v1 + v2 for k1, v1 in paths.items() for k2, v2 in paths.items() if not k1 & k2
    )
    print(max_flow)
