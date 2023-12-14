from typing import List, NamedTuple, Optional, Tuple

from solutions import read_input

EXAMPLE = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


def parse_input(input: str) -> List[str]:
    return input.split("\n\n")


class rock_locations(NamedTuple):
    locations: List[Tuple[int, int]]
    rows: int
    columns: int


def rock_locs(block: str) -> rock_locations:
    rocks = []
    split_blocks = block.splitlines()
    for row_num, row in enumerate(split_blocks):
        for col_num, spot in enumerate(row):
            if spot == "#":
                rocks.append((row_num, col_num))
    return rock_locations(rocks, len(split_blocks), len(split_blocks[0]))


def check_split(rock_locs: rock_locations, split: int, vert: bool, error_target: int) -> Optional[int]:
    errors = 0
    for rock in rock_locs.locations:
        trial_rock = (rock[0] if vert else split - rock[0], split - rock[1] if vert else rock[1])
        if (
            (trial_rock[0] >= 0)
            and (trial_rock[0] <= rock_locs.rows - 1)
            and (trial_rock[1] >= 0)
            and (trial_rock[1] <= rock_locs.columns - 1)
            and (trial_rock not in rock_locs.locations)
        ):
            errors += 1
    return errors == error_target


def run_splits(input: str, error_target: int) -> int:
    running_sum = 0
    for block in parse_input(input):
        rocks = rock_locs(block)
        for split in range(1, 2 * rocks.rows - 1, 2):
            if check_split(rocks, split, False, error_target):
                running_sum += 100 * (split + 1) // 2
        for split in range(1, 2 * rocks.columns - 1, 2):
            if check_split(rocks, split, True, error_target):
                running_sum += (split + 1) // 2
    return running_sum


assert run_splits(EXAMPLE, 0) == 405
assert run_splits(EXAMPLE, 1) == 400

puzzle_input = read_input("13")

print(run_splits(puzzle_input, 0))
print(run_splits(puzzle_input, 1))
