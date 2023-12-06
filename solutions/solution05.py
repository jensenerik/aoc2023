from typing import List, Optional, Tuple

from . import read_input

EXAMPLE = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def dest_from_row(lookup_num: int, dest_start: int, source_start: int, length: int) -> Optional[int]:
    diff_from_start = lookup_num - source_start
    if diff_from_start >= 0 and diff_from_start <= length:
        return dest_start + diff_from_start
    else:
        return None


def destination_from_group(lookup_num: int, row_group: str) -> int:
    destination = None
    for row in row_group.splitlines()[1:]:
        destination = dest_from_row(lookup_num, *[int(item) for item in row.split()])
        if destination is not None:
            return destination
    return lookup_num


def seed_to_location(input: str) -> int:
    groups = input.split("\n\n")
    seeds = [int(item) for item in groups[0].split()[1:]]
    seed_locations = []
    for seed in seeds:
        running_value = seed
        for group in groups[1:]:
            running_value = destination_from_group(running_value, group)
        seed_locations.append(running_value)
    return min(seed_locations)


def range_destination(lookup_ranges: List[Tuple[int, int]], row_group: str) -> List[Tuple[int, int]]:
    ranges_to_process = lookup_ranges.copy()
    destination_ranges: List[Tuple[int, int]] = []
    for row in row_group.splitlines()[1:]:
        loose_ends: List[Tuple[int, int]] = []
        dest_start, source_start, length = tuple([int(item) for item in row.split()])
        source_end = source_start + length
        for lookup_range in ranges_to_process:
            if lookup_range[0] < source_start:
                loose_ends.append((lookup_range[0], min(lookup_range[1], source_start)))
            if lookup_range[1] > source_end:
                loose_ends.append((max(lookup_range[0], source_end), lookup_range[1]))
            if (lookup_range[0] < source_end) and (lookup_range[1] > source_start):
                offset = dest_start - source_start
                destination_ranges.append(
                    (max(lookup_range[0], source_start) + offset, min(lookup_range[1], source_end) + offset)
                )
        ranges_to_process = loose_ends
    return destination_ranges + ranges_to_process


def ranges_to_location(input: str) -> int:
    groups = input.split("\n\n")
    seed_ranges = groups[0].split()[1:]
    running_ranges = [
        (int(seed_ranges[i]), int(seed_ranges[i]) + int(seed_ranges[i + 1])) for i in range(0, len(seed_ranges), 2)
    ]
    for group in groups[1:]:
        running_ranges = range_destination(running_ranges, group)
    return min([item[0] for item in running_ranges])


assert seed_to_location(EXAMPLE) == 35
assert ranges_to_location(EXAMPLE) == 46

puzzle_input = read_input("05")

print(seed_to_location(puzzle_input))
print(ranges_to_location(puzzle_input))
