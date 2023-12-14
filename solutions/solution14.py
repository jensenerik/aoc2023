from typing import Dict, Tuple

from solutions import read_input

EXAMPLE = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


def parse_input(input: str) -> Dict[Tuple[int, int], str]:
    rock_map: Dict[Tuple[int, int], str] = {}
    for row_num, row in enumerate(input.splitlines()):
        for col_num, symbol in enumerate(row):
            rock_map[(row_num, col_num)] = symbol
    return rock_map


def rolled_rocks(input: str):
    rock_map = parse_input(input)
    max_row = max([loc[0] for loc in rock_map.keys()])
    max_col = max([loc[1] for loc in rock_map.keys()])
    rock_values = 0
    for col_num in range(max_col + 1):
        offset = 0
        for row_num in range(max_row + 1):
            symbol = rock_map[(row_num, col_num)]
            if symbol == ".":
                offset += 1
            elif symbol == "#":
                offset = 0
            elif symbol == "O":
                rock_values += max_row - row_num + 1 + offset
    return rock_values


def move_rocks(rock_map: Dict[Tuple[int, int], str], direction: str) -> Dict[Tuple[int, int], str]:
    max_row = max([loc[0] for loc in rock_map.keys()])
    max_col = max([loc[1] for loc in rock_map.keys()])
    running_rocks = rock_map.copy()
    for col_num in range(max_col, -1, -1) if direction == "east" else range(max_col + 1):
        for row_num in range(max_row, -1, -1) if direction == "south" else range(max_row + 1):
            if running_rocks[(row_num, col_num)] == ".":
                possible_check_rows = (
                    range(row_num + 1, max_row + 1)
                    if direction == "north"
                    else (range(row_num - 1, -1, -1) if direction == "south" else range(row_num, row_num + 1))
                )
                possible_check_cols = (
                    range(col_num + 1, max_col + 1)
                    if direction == "west"
                    else (range(col_num - 1, -1, -1) if direction == "east" else range(col_num, col_num + 1))
                )
                check_spots = []
                for check_row in possible_check_rows:
                    for check_col in possible_check_cols:
                        check_spots.append((check_row, check_col))
                for spot in check_spots:
                    if running_rocks[spot[0], spot[1]] == "#":
                        break
                    elif running_rocks[spot[0], spot[1]] == "O":
                        running_rocks[row_num, col_num] = "O"
                        running_rocks[spot[0], spot[1]] = "."
                        break
    return running_rocks


def cycle_rocks(rock_map: Dict[Tuple[int, int], str]) -> Dict[Tuple[int, int], str]:
    return move_rocks(move_rocks(move_rocks(move_rocks(rock_map, "north"), "west"), "south"), "east")


def calculate_score(rock_map: Dict[Tuple[int, int], str]) -> int:
    running_sum = 0
    max_row = max([loc[0] for loc in rock_map.keys()])
    for rock_loc, symbol in rock_map.items():
        if symbol == "O":
            running_sum += max_row - rock_loc[0] + 1
    return running_sum


def find_pattern(input: str, endpoint: int) -> int:
    patterns = [parse_input(input)]
    steps = 0
    while True:
        new_pattern = cycle_rocks(patterns[-1])
        steps += 1
        if new_pattern in patterns:
            found_spot = patterns.index(new_pattern)
            end_pattern = patterns[((endpoint - found_spot) % (len(patterns) - found_spot)) + found_spot]
            return calculate_score(end_pattern)
        else:
            patterns.append(new_pattern)


assert rolled_rocks(EXAMPLE) == 136
assert calculate_score(move_rocks(parse_input(EXAMPLE), "north")) == 136
assert find_pattern(EXAMPLE, 1_000_000_000) == 64

puzzle_input = read_input("14")

print(rolled_rocks(puzzle_input))
print(find_pattern(puzzle_input, 1_000_000_000))
