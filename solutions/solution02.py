import math
from typing import Dict

from . import read_input

EXAMPLE = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

CUBE_MAXES = {"red": 12, "green": 13, "blue": 14}


def parse_game(game_data: str) -> Dict[str, int]:
    pulls = game_data.split(";")
    color_max: Dict[str, int] = dict()
    for pull in pulls:
        color_counts = pull.split(",")
        for color_count in color_counts:
            count = int(color_count.strip().split()[0])
            color = color_count.strip().split()[1]
            if color_max.get(color, 0) < count:
                color_max[color] = count
    return color_max


def compare_games(games: str, cube_max: Dict[str, int]) -> int:
    running_sum = 0
    for game in games.split("\n"):
        game_num = int(game.split(":")[0][5:])
        game_max = parse_game(game.split(":")[1])
        game_test = True
        for k, v in cube_max.items():
            if game_max[k] > v:
                game_test = False
        if game_test:
            running_sum += game_num
    return running_sum


def game_powers(games: str) -> int:
    running_sum = 0
    for game in games.split("\n"):
        game_max = parse_game(game.split(":")[1])
        running_sum += math.prod(game_max.values())
    return running_sum


assert compare_games(EXAMPLE, CUBE_MAXES) == 8
assert game_powers(EXAMPLE) == 2286

puzzle_input = read_input("02")

print(compare_games(puzzle_input, CUBE_MAXES))
print(game_powers(puzzle_input))
