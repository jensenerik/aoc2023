from typing import Dict, List, NamedTuple, Set, Tuple

from . import read_input

EXAMPLE = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

EXAMPLE_2 = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

INSIDE_EXAMPLE = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

LARGE_INSIDE_EXAMPLE = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

JUNK_INSIDE_EXAMPLE = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""


KEY: Dict[str, List[Tuple[int, int]]] = {
    "|": [(-1, 0), (+1, 0)],
    "-": [(0, -1), (0, +1)],
    "L": [(0, 1), (-1, 0)],
    "J": [(0, -1), (-1, 0)],
    "7": [(0, -1), (1, 0)],
    "F": [(0, 1), (1, 0)],
    ".": [],
    "S": [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
    ],
}


def parse_pattern(input: str) -> Dict[Tuple[int, int], str]:
    coord_map: Dict[Tuple[int, int], str] = {}
    for row_num, row in enumerate(input.splitlines()):
        for col_num, symbol in enumerate(row):
            coord_map[(row_num, col_num)] = symbol
    return coord_map


class path_location(NamedTuple):
    location: Tuple[int, int]
    way_back: Tuple[int, int]


def coord_addition(item_1: Tuple[int, int], item_2: Tuple[int, int]) -> Tuple[int, int]:
    return (item_1[0] + item_2[0], item_1[1] + item_2[1])


def coord_reverse(coord: Tuple[int, int]) -> Tuple[int, int]:
    return (-coord[0], -coord[1])


def track_paths(
    coord_map: Dict[Tuple[int, int], str], symbol_key: Dict[str, List[Tuple[int, int]]]
) -> List[path_location]:
    s_location = [key for key, value in coord_map.items() if value == "S"][0]
    running_locations = [path_location(s_location, (0, 0))]
    histories: List[List[path_location]] = [[]]
    finished = False
    while not finished:
        new_locations: List[path_location] = []
        new_histories: List[List[path_location]] = []
        for loc_num, path_loc in enumerate(running_locations):
            possible_paths = symbol_key[coord_map.get(path_loc.location, ".")]
            if path_loc.way_back in possible_paths or path_loc.way_back == (0, 0):
                for path in possible_paths:
                    if path != path_loc.way_back:
                        new_locations.append(
                            path_location(coord_addition(path_loc.location, path), coord_reverse(path))
                        )
                        new_histories.append(histories[loc_num] + [path_loc])
        running_locations = new_locations
        histories = new_histories
        if s_location in [loc.location for loc in running_locations] or len(running_locations) == 0:
            finished = True
    return histories[0]


def left_side(path_loc: path_location) -> List[Tuple[int, int]]:
    return [
        (
            path_loc.location[0] - path_loc.way_back[1] + lag * path_loc.way_back[0],
            path_loc.location[1] + path_loc.way_back[0] + lag * path_loc.way_back[1],
        )
        for lag in [0, 1]
    ]


def right_side(path_loc: path_location) -> List[Tuple[int, int]]:
    return [
        (
            path_loc.location[0] + path_loc.way_back[1] + lag * path_loc.way_back[0],
            path_loc.location[1] - path_loc.way_back[0] + lag * path_loc.way_back[1],
        )
        for lag in [0, 1]
    ]


def find_more_coords(
    check_sided_coords: Set[Tuple[int, int]],
    all_sided_coords: Set[Tuple[int, int]],
    path_coords: List[Tuple[int, int]],
    coord_map: Dict[Tuple[int, int], str],
) -> Set[Tuple[int, int]]:
    new_sided_coords = set()
    for coord in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        for sided_coord in check_sided_coords:
            trial_new_coord = coord_addition(sided_coord, coord)
            if (
                trial_new_coord not in path_coords
                and trial_new_coord in coord_map
                and trial_new_coord not in all_sided_coords
            ):
                new_sided_coords.add(trial_new_coord)
    return new_sided_coords


def calculate_interior(input: str, symbol_key: Dict[str, List[Tuple[int, int]]]) -> int:
    coord_map = parse_pattern(input)
    total_coords = len(coord_map)
    path_history = track_paths(coord_map, symbol_key)
    path_coords = [path_loc.location for path_loc in path_history]
    left_coords = set()
    right_coords = set()
    for path_loc in path_history:
        left_coords.update([item for item in left_side(path_loc) if item not in path_coords and item in coord_map])
        right_coords.update([item for item in right_side(path_loc) if item not in path_coords and item in coord_map])
    new_left_coords = left_coords.copy()
    new_right_coords = right_coords.copy()
    while len(path_coords) + len(left_coords) + len(right_coords) < total_coords:
        new_left_coords = find_more_coords(new_left_coords, left_coords, path_coords, coord_map)
        new_right_coords = find_more_coords(new_right_coords, right_coords, path_coords, coord_map)
        left_coords.update(new_left_coords)
        right_coords.update(new_right_coords)
    if len([coord for coord in left_coords if ((coord[0] == 0) or (coord[1] == 0))]) > 0:
        return len(right_coords)
    else:
        return len(left_coords)


assert len(track_paths(parse_pattern(EXAMPLE), KEY)) // 2 == 4
assert len(track_paths(parse_pattern(EXAMPLE_2), KEY)) // 2 == 8
assert calculate_interior(INSIDE_EXAMPLE, KEY) == 4
assert calculate_interior(LARGE_INSIDE_EXAMPLE, KEY) == 8
assert calculate_interior(JUNK_INSIDE_EXAMPLE, KEY) == 10


puzzle_input = read_input("10")

print(len(track_paths(parse_pattern(puzzle_input), KEY)) // 2)
print(calculate_interior(puzzle_input, KEY))
