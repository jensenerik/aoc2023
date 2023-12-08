import math
from typing import Dict, List, Tuple

from . import read_input

EXAMPLE = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

EXAMPLE_2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

GHOST_EXAMPLE = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


def make_tuple(tuple_looking_string: str) -> Tuple[str, ...]:
    return tuple([item.strip().strip("()") for item in tuple_looking_string.split(",")])


def parse_input(input: str) -> Tuple[List[str], Dict[str, Tuple[str, ...]]]:
    input_rows = input.splitlines()
    instructions = list(input_rows[0])
    pointers = {row.split("=")[0].strip(): make_tuple(row.split("=")[1]) for row in input_rows[2:]}
    return instructions, pointers


def run_rules(instructions: List[str], pointers: Dict[str, Tuple[str, ...]]) -> int:
    location = "AAA"
    steps = 0
    while location != "ZZZ":
        for direction in instructions:
            choices = pointers[location]
            location = choices[0] if direction == "L" else choices[1]
            steps += 1
    return steps


def run_ghosts(instructions: List[str], pointers: Dict[str, Tuple[str, ...]]) -> int:
    locations = [key for key in pointers.keys() if key[-1] == "A"]
    steps = 0
    counts = [0] * len(locations)

    while not all(counts):
        for direction in instructions:
            new_locations = []
            steps += 1
            for i, location in enumerate(locations):
                choices = pointers[location]
                new_loc = choices[0] if direction == "L" else choices[1]
                new_locations.append(new_loc)
                if new_loc[-1] == "Z" and counts[i] == 0:
                    counts[i] = steps
            locations = new_locations
    return math.lcm(*counts)


assert run_rules(*parse_input(EXAMPLE)) == 2
assert run_rules(*parse_input(EXAMPLE_2)) == 6
assert run_ghosts(*parse_input(GHOST_EXAMPLE)) == 6

puzzle_input = read_input("08")

print(run_rules(*parse_input(puzzle_input)))
print(run_ghosts(*parse_input(puzzle_input)))
