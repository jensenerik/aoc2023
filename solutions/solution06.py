import math
from typing import Any, Tuple

from . import read_input

EXAMPLE = """Time:      7  15   30
Distance:  9  40  200"""


def parse_time_distance(races: str) -> zip[Tuple[Any, ...]]:
    time_distance = [[int(item) for item in row.split()[1:]] for row in races.splitlines()]
    return zip(*time_distance)


def solve_quadratic(time: int, dist: int) -> int:
    discriminant = (time**2 - 4 * dist) ** 0.5
    lower_value = time / 2 - discriminant / 2
    upper_value = time / 2 + discriminant / 2
    return math.ceil(upper_value) - math.floor(lower_value) - 1


def mult_solutions(races: str) -> int:
    return math.prod([solve_quadratic(*item) for item in parse_time_distance(races)])


def single_race(races: str) -> int:
    time_distance = [int("".join(row.split()[1:])) for row in races.splitlines()]
    return solve_quadratic(time_distance[0], time_distance[1])


assert mult_solutions(EXAMPLE) == 288
assert single_race(EXAMPLE) == 71503

puzzle_input = read_input("06")

print(mult_solutions(puzzle_input))
print(single_race(puzzle_input))
