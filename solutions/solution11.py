from typing import List, Set, Tuple

from . import read_input

EXAMPLE = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


def find_galaxies(input: str) -> List[Tuple[int, int]]:
    galaxy_list: List[Tuple[int, int]] = []
    for row_num, row in enumerate(input.splitlines()):
        for col_num, char in enumerate(row):
            if char == "#":
                galaxy_list.append((row_num, col_num))
    return galaxy_list


def expand_universe(galaxy_list: List[Tuple[int, int]], expansion_factor: int) -> List[Tuple[int, int]]:
    empty_row_col: List[Set] = [set(), set()]
    for i in range(2):
        filled_row_col = {galaxy[i] for galaxy in galaxy_list}
        empty_row_col[i] = {row_col for row_col in range(max(filled_row_col)) if row_col not in filled_row_col}
    return [
        (
            galaxy[0] + (expansion_factor - 1) * len({item for item in empty_row_col[0] if item < galaxy[0]}),
            galaxy[1] + (expansion_factor - 1) * len({item for item in empty_row_col[1] if item < galaxy[1]}),
        )
        for galaxy in galaxy_list
    ]


def total_distance(input: str, expansion_factor: int) -> int:
    galaxies = expand_universe(find_galaxies(input), expansion_factor)
    distance_sum = 0
    for gal_num, galaxy in enumerate(galaxies[:-1]):
        for target in galaxies[gal_num + 1 :]:
            distance_sum += abs(galaxy[0] - target[0]) + abs(galaxy[1] - target[1])
    return distance_sum


assert total_distance(EXAMPLE, 2) == 374
assert total_distance(EXAMPLE, 10) == 1030
assert total_distance(EXAMPLE, 100) == 8410

puzzle_input = read_input("11")

print(total_distance(puzzle_input, 2))
print(total_distance(puzzle_input, 1_000_000))
