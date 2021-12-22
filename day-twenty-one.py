import functools
import math
from enum import Enum
import numpy as np
import random
from itertools import permutations
from itertools import groupby

test_data = [4, 8]
real_data = [3, 7]

def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, list) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


class Dice:
    def __init__(self, sides=100, deterministic=True):
        self.last_roll = 0
        self.roll_count = 0
        self.sides = sides
        self.deterministic = deterministic

    def update_last_roll(self, last_roll):
        self.roll_count += 1
        self.last_roll = last_roll
        return last_roll

    def __str__(self):
        return "Rolls:%d" % self.roll_count

    def roll(self):

        if (self.deterministic):
            return self.update_last_roll(self.last_roll + 1 if self.last_roll < self.sides else 1)

        return self.update_last_roll(random.randint(1, self.sides))


def new_position_for_board(board_len, current_position, steps):
    offset_position = current_position + (steps % board_len)
    return offset_position if offset_position <= board_len else offset_position - board_len


def simulate_game(starting_positions, winning_score=1000):
    board_len = 10
    scores = [0, 0]
    current_player_index = 0
    current_positions = starting_positions
    dice = Dice()

    while not any([score >= winning_score for score in scores]):
        steps = sum([dice.roll() for i in range(0, 3)])
        current_positions[current_player_index] = new_position_for_board(board_len,
                                                                         current_positions[current_player_index], steps)
        scores[current_player_index] += current_positions[current_player_index]
        current_player_index = 0 if current_player_index else 1

    return dice.roll_count * min(scores)


def group_by_roll_value(data):
    return {k: len(list(g)) for k, g in groupby(sorted(data))}


def simulate_universes(starting_positions, winning_score=21):

    # distribution of 27 roll results for each round
    single_round_roll_universes = group_by_roll_value([
        sum(thing)
        for thing in list(flatten([[[(i, j, k) for i in range(1, 4)] for j in range(1, 4)] for k in range(1, 4)]))
    ])

    universes = defaultdict()

    # key is position for player one, position for player two, and their respective scores
    # value is the number of universes that match that key. We start with just one universe.
    universes[(starting_positions[0], starting_positions[1], 0, 0)] = 1

    def finished(universe):
        key, value = universe
        return key[2] >= winning_score or key[3] >= winning_score

    def universes_with_unfinished_games(universes):
        return defaultdict(None,{key: value for key, value in universes.items() if not finished((key, value))})

    round = 0

    while (universes_with_unfinished_games(universes)):

        next_universes = defaultdict(int)

        # While there exist any universes without both players having won
        for key in universes:

            player_one_position, player_two_position, player_one_score, player_two_score = key
            if (finished((key, 0))):
                next_universes[key] += universes[key]
            else:
                # active player this round
                position = player_one_position if round == 0 else player_two_position
                score = player_one_score if round == 0 else player_two_score

                # This universe will generate a bunch of extra universes when we roll the dice
                for steps, count in single_round_roll_universes.items():

                    new_position = new_position_for_board(10, position, steps)
                    new_score = score + new_position

                    updated_key = (new_position, player_two_position, new_score,
                        player_two_score) if round == 0 else (player_one_position, new_position, player_one_score,
                                                                new_score)

                    next_universes[updated_key] += count * universes[key]

        round = 1 if round == 0 else 0
        universes = next_universes

    return max(sum([count for key, count in universes.items() if key[2] >= winning_score]),
    sum([count for key, count in universes.items() if key[3] >= winning_score]))
