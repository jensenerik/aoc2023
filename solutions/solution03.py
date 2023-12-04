import math
from typing import List, NamedTuple, Optional, Tuple

from . import read_input

EXAMPLE = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

DIGITS = [str(i) for i in range(10)]


class part_num(NamedTuple):
    number: int
    row_number: int
    start_col: int
    end_col: int


def validate_part_number(part_number: part_num, special_chars: List[Tuple[int, int]]) -> bool:
    for row_num in [part_number.row_number + i for i in [-1, 0, 1]]:
        for col_num in range(part_number.start_col - 1, part_number.end_col + 2):
            if (row_num, col_num) in special_chars:
                return True
    return False


def process_row(row_number: int, row: str, gear: bool) -> Tuple[List[part_num], List[Tuple[int, int]]]:
    part_numbers: List[part_num] = []
    special_chars: List[Tuple[int, int]] = []
    start_col: Optional[int] = None
    current_number: str = ""
    for col_number, symbol in enumerate(row):
        if symbol in DIGITS:
            if start_col is None:
                start_col = col_number
            current_number += symbol
        else:
            if symbol == "*" if gear else symbol != ".":
                special_chars.append((row_number, col_number))
            if start_col is not None:
                part_numbers.append(part_num(int(current_number), row_number, start_col, col_number - 1))
            start_col = None
            current_number = ""
    if start_col is not None:
        part_numbers.append(part_num(int(current_number), row_number, start_col, len(row)))
    return part_numbers, special_chars


def generate_part_nums(text: str) -> List[part_num]:
    part_numbers: List[part_num] = []
    special_chars: List[Tuple[int, int]] = []
    for row_number, row in enumerate(text.splitlines()):
        new_parts, new_specials = process_row(row_number, row, False)
        part_numbers.extend(new_parts)
        special_chars.extend(new_specials)
    return [candidate for candidate in part_numbers if validate_part_number(candidate, special_chars)]


def validate_gear(part_numbers: List[part_num], gear: Tuple[int, int]) -> int:
    touching_parts = [
        part
        for part in part_numbers
        if (part.row_number - gear[0] in [-1, 0, 1])
        and (part.start_col - gear[1] <= 1)
        and (part.end_col - gear[1] >= -1)
    ]
    if len(touching_parts) > 1:
        return math.prod([part.number for part in touching_parts])
    else:
        return 0


def generate_gear_products(text: str) -> int:
    part_numbers: List[part_num] = []
    gears: List[Tuple[int, int]] = []
    for row_number, row in enumerate(text.splitlines()):
        new_parts, new_gears = process_row(row_number, row, True)
        part_numbers.extend(new_parts)
        gears.extend(new_gears)
    return sum([validate_gear(part_numbers, gear) for gear in gears])


assert sum([part.number for part in generate_part_nums(EXAMPLE)]) == 4361
assert generate_gear_products(EXAMPLE) == 467835

puzzle_input = read_input("03")

print(sum([part.number for part in generate_part_nums(puzzle_input)]))
print(generate_gear_products(puzzle_input))
