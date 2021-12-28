import functools
import math
from enum import Enum
import numpy as np
import random
import copy
from itertools import groupby


def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, list) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


real_data = ["#############\n", "#...........#\n", "###D#D#B#A###\n", "  #C#A#B#C#\n", "  #########\n"]
test_data = ["#############\n", "#...........#\n", "###B#C#B#D###\n", "  #A#D#C#A#\n", "  #########\n"]
part_two_insert = ["  #D#C#B#A#\n", "  #D#B#A#C#\n"]

energy_cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


def cost(steps, amphipod):
    return energy_cost.get(amphipod) * steps


#############
#...........#
###D#D#B#A###
#C#A#B#C#
#########

#############
#..........A#
###.#.#C#D###
#A#B#C#D#
#########

# 16404 -- Too low (no constraints cost)
# cost(7,'D') + cost(8, 'D') + cost(9, 'A') + cost(5, 'A') + cost(5, 'B') + cost(4, 'B') +  cost(6,'C') + cost(7, 'C')

test_cost = cost(7, 'D') + cost(8, 'D') + cost(3, 'A') + cost(7, 'A') + cost(5, 'B') + cost(5, 'B') + cost(
    7, 'B') + cost(7, 'B') + cost(6, 'C') + cost(7, 'C') + cost(9, 'A') + cost(9, 'A')

# calculated ->
# {'cost': 16558, 'side_room_rear': ['A', 'B', 'C', 'D'], 'side_room_entrance': ['A', 'B', 'C', 'D'], 'hall': [None, None, None, None, None, None, None, None, None, None, None]}
# {'cost': 16556, 'side_room_rear': ['A', 'B', 'C', 'D'], 'side_room_entrance': ['A', 'B', 'C', 'D'], 'hall': [None, None, None, None, None, None, None, None, None, None, None]}
# {'cost': 16528, 'side_room_rear': ['A', 'B', 'C', 'D'], 'side_room_entrance': ['A', 'B', 'C', 'D'], 'hall': [None, None, None, None, None, None, None, None, None, None, None]}
# {'cost': 16526, 'side_room_rear': ['A', 'B', 'C', 'D'], 'side_room_entrance': ['A', 'B', 'C', 'D'], 'hall': [None, None, None, None, None, None, None, None, None, None, None]}
# {'cost': 16508, 'side_room_rear': ['A', 'B', 'C', 'D'], 'side_room_entrance': ['A', 'B', 'C', 'D'], 'hall': [None, None, None, None, None, None, None, None, None, None, None]}

test_data = ["#############\n", "#...........#\n", "###B#C#B#D###\n", "  #A#D#C#A#\n", "  #########\n"]


def read_game_state(lines):
    """
    Just interested in lines 3 and 4 to get the starting positions
    """
    def none_or_amphipod(characters):
        return [None if x == "." else x for x in characters]

    side_room_entrance = lines[2][3:].split("#")[:4]
    side_room_rear = (lines[3]).strip()[1:].split("#")[:4]
    hall = lines[1].strip()[1:-1]
    return {
        "cost": 0,
        "side_room_rear": none_or_amphipod(side_room_rear),
        "side_room_entrance": none_or_amphipod(side_room_entrance),
        "hall": none_or_amphipod(hall)
    }


def amphipod_for_descriptor(game_state, descriptor):
    key, index = descriptor.split(":")
    return game_state[key][int(index)]


def update_descriptor(game_state, descriptor, new_value):
    key, index = descriptor.split(":")
    game_state[key][int(index)] = new_value


def descriptor_for_key_and_index(key, index):
    return "%s:%d" % (key, index)


def index_for_descriptor(descriptor):
    return int(descriptor.split(":")[1])


def hall_descriptor(descriptor):
    return "hall" in descriptor


def entrance_descriptor(descriptor):
    return "side_room_entrance" in descriptor


def target_room_index_for_amphipod(amphipod):
    return {'A': 0, 'B': 1, 'C': 2, 'D': 3}.get(amphipod)


def hall_index_for_room_index(room_index):
    """
    Mapping the room indexes to the indexes in the hall array.

    #...........#
    ###.#.#.#.###

    """
    return {0: 2, 1: 4, 2: 6, 3: 8}.get(room_index)


def target_room_index_for_position(game_state, descriptor):
    return target_room_index_for_amphipod(amphipod_for_descriptor(game_state, descriptor))


def available_target_room(game_state, descriptor, target_room_index):
    if (game_state.get("side_room_entrance")[target_room_index] is not None):
        return False
    if (game_state.get("side_room_rear")[target_room_index] is not None
            and game_state.get("side_room_rear")[target_room_index] != amphipod_for_descriptor(game_state, descriptor)):
        return False
    return True


def available_to_move(game_state):
    """
    Return a list of amphipods that can move
    """
    room_candidates = []
    for index, side_room_amphipod in enumerate(game_state.get("side_room_entrance")):

        # If there is a amphipod in the entrance room (and they don't belong
        # there already or the rear room doesn't belong there either)
        if side_room_amphipod is not None and (
                target_room_index_for_amphipod(side_room_amphipod) != index
                or target_room_index_for_amphipod(game_state.get("side_room_rear")[index]) != index):
            room_candidates.append(descriptor_for_key_and_index("side_room_entrance", index))
        elif game_state.get("side_room_rear")[index] is not None and target_room_index_for_amphipod(
                game_state.get("side_room_rear")[index]) != index:
            room_candidates.append(descriptor_for_key_and_index("side_room_rear", index))

    # Check the hall guys
    hall_candidates = []
    for index, maybe_amphipod_in_the_hall in enumerate(game_state.get('hall')):
        if maybe_amphipod_in_the_hall is None:
            continue
        target_room_index = target_room_index_for_amphipod(maybe_amphipod_in_the_hall)
        hall_candidate = descriptor_for_key_and_index("hall", index)

        if (available_target_room(game_state, hall_candidate, target_room_index)):
            hall_candidates.append(hall_candidate)

    return {"room_candidates": room_candidates, "hall_candidates": hall_candidates}


assert available_to_move(read_game_state(test_data)) == {
    "room_candidates": ['side_room_entrance:0', 'side_room_entrance:1', 'side_room_entrance:2', 'side_room_entrance:3'],
    "hall_candidates": []
}
assert available_to_move(
    read_game_state(["#############\n", "#..........A#\n", "###.#C#B#D###\n", "  #A#D#C#A#\n", "  #########\n"])) == {
        "room_candidates": ['side_room_entrance:1', 'side_room_entrance:2', 'side_room_entrance:3'],
        "hall_candidates": ['hall:10']
    }
assert available_to_move(
    read_game_state(["#############\n", "#..........A#\n", "###.#C#B#D###\n", "  #D#A#C#A#\n", "  #########\n"])) == {
        "room_candidates": ['side_room_rear:0', 'side_room_entrance:1', 'side_room_entrance:2', 'side_room_entrance:3'],
        "hall_candidates": []
    }


def destinations_around_hall_index(game_state, hall_index):

    left_ampipods = [index for index, x in enumerate(game_state.get('hall')) if x is not None and index < hall_index]
    min_destination_index_in_hall = 0 if not left_ampipods else max(0, max(left_ampipods) + 1)

    right_ampipods = [index for index, x in enumerate(game_state.get('hall')) if x is not None and index > hall_index]
    max_destination_index_in_hall = 10 if not right_ampipods else min(10, min(right_ampipods) - 1)

    return min_destination_index_in_hall, max_destination_index_in_hall


def within_bounds(index, min_d, max_d):
    return index >= min_d and index <= max_d


def hall_destinations_for_index(game_state, index):
    legal_destinations_in_hall = [0, 1, 3, 5, 7, 9, 10]

    min_destination_index_in_hall, max_destination_index_in_hall = destinations_around_hall_index(
        game_state, hall_index_for_room_index(index))

    return list(
        filter(lambda index: within_bounds(index, min_destination_index_in_hall, max_destination_index_in_hall),
               legal_destinations_in_hall))


assert hall_destinations_for_index(
    read_game_state(["#############\n", "#..........A#\n", "###.#C#B#D###\n", "  #D#A#C#A#\n", "  #########\n"]),
    0) == [0, 1, 3, 5, 7, 9]
assert hall_destinations_for_index(
    read_game_state(["#############\n", "#.D........A#\n", "###.#C#B#.###\n", "  #D#A#C#A#\n", "  #########\n"]),
    0) == [3, 5, 7, 9]
assert hall_destinations_for_index(
    read_game_state(["#############\n", "#.D.B......A#\n", "###.#C#.#.###\n", "  #D#A#C#A#\n", "  #########\n"]),
    0) == []
assert hall_destinations_for_index(
    read_game_state(["#############\n", "#.D...B....A#\n", "###.#C#.#.###\n", "  #D#A#C#A#\n", "  #########\n"]),
    0) == [3]
assert hall_destinations_for_index(
    read_game_state(["#############\n", "#.D.........#\n", "###.#C#A#B###\n", "  #D#A#C#A#\n", "  #########\n"]),
    0) == [3, 5, 7, 9, 10]


def available_destinations(game_state):

    # Get a list of candidates to move. For each one we will generate a list of
    # destination descriptors
    candidates = available_to_move(game_state)

    destinations_for_candidates = {}

    # First do the side room candidates (moving into the legal_destinations_in_hall)
    for room_candidate in candidates.get("room_candidates"):
        destinations_for_candidates[room_candidate] = [
            descriptor_for_key_and_index("hall", index)
            for index in hall_destinations_for_index(game_state, index_for_descriptor(room_candidate))
        ]

    def destination_for_target_room_index(game_state, target_room_index):
        return [descriptor_for_key_and_index("side_room_entrance", target_room_index)
                ] if game_state.get("side_room_rear")[target_room_index] else [
                    descriptor_for_key_and_index("side_room_rear", target_room_index)
                ]

    # Then overwrite those side room candidates if they can move directly into
    # their target room (because that will always be cheaper than a move to the
    # hall with a subsequent move to the room so we may as well restrict
    # available destinations if this is possible).
    for room_candidate in candidates.get("room_candidates"):
        target_room_index = target_room_index_for_position(game_state, room_candidate)
        if (not available_target_room(game_state, room_candidate, target_room_index)):
            continue

        hall_destinations = hall_destinations_for_index(game_state, index_for_descriptor(room_candidate))
        target_hall_index = hall_index_for_room_index(target_room_index)
        source_hall_index = hall_index_for_room_index(index_for_descriptor(room_candidate))

        # If the hall source/target is within the hall destinations then there
        # is a clear path from source to target
        if (hall_destinations and min([target_hall_index, source_hall_index]) >= min(hall_destinations)
                and max([target_hall_index, source_hall_index]) <= max(hall_destinations)):

            # The destination for the room candidate is the single side room they can move too.
            destinations_for_candidates[room_candidate] = destination_for_target_room_index(
                game_state, target_room_index)

    # Then do hall candiates (moving into rooms)
    for hall_candidate in candidates.get("hall_candidates"):
        target_room_index = target_room_index_for_position(game_state, hall_candidate)
        target_hall_index = hall_index_for_room_index(target_room_index)
        source_hall_index = index_for_descriptor(hall_candidate)
        min_destination_index_in_hall, max_destination_index_in_hall = destinations_around_hall_index(
            game_state, source_hall_index)
        # If the target hall index is within the min and max destinations then the amphipod can just move there.
        if (within_bounds(target_hall_index, min_destination_index_in_hall, max_destination_index_in_hall)):
            destinations_for_candidates[hall_candidate] = destination_for_target_room_index(
                game_state, target_room_index)

    return destinations_for_candidates


assert available_destinations(
    read_game_state(["#############\n", "#.A.........#\n", "###.#C#A#B###\n", "  #A#D#C#A#\n",
                     "  #########\n"]))['side_room_entrance:1'] == ['hall:3', 'hall:5', 'hall:7', 'hall:9', 'hall:10']
assert available_destinations(
    read_game_state(["#############\n", "#.A.........#\n", "###.#C#.#B###\n", "  #A#D#.#A#\n",
                     "  #########\n"]))['side_room_entrance:1'] == ['side_room_rear:2']
assert available_destinations(
    read_game_state(["#############\n", "#.A...D.....#\n", "###.#C#.#B###\n", "  #A#D#.#A#\n",
                     "  #########\n"]))['side_room_entrance:1'] == ['hall:3']
assert available_destinations(
    read_game_state(["#############\n", "#C....D....C#\n", "###A#B#.#.###\n", "  #A#B#.#D#\n",
                     "  #########\n"]))['hall:5'] == ['side_room_entrance:3']


def cost_for_move(game_state, source, target):

    # first, which amphipod is moving?
    steps = 0
    amphipod = amphipod_for_descriptor(game_state, source)
    assert amphipod_for_descriptor(game_state, target) == None

    # If they are moving from the hall?
    if (hall_descriptor(source)):
        target_hall_index = hall_index_for_room_index(index_for_descriptor(target))
        steps += abs(target_hall_index - index_for_descriptor(source))
        steps += 1 if entrance_descriptor(target) else 2
    elif hall_descriptor(target):
        # Just move into the side room
        steps += 1 if entrance_descriptor(source) else 2
        # move from the side room to the spot in the hall
        target_hall_index = index_for_descriptor(target)
        source_hall_index = hall_index_for_room_index(index_for_descriptor(source))
        steps += abs(target_hall_index - source_hall_index)
    else:
        # move from and to the side room
        steps += 1 if entrance_descriptor(source) else 2
        steps += 1 if entrance_descriptor(target) else 2
        # move from the side room to the other side room via the hall
        target_hall_index = hall_index_for_room_index(index_for_descriptor(target))
        source_hall_index = hall_index_for_room_index(index_for_descriptor(source))
        steps += abs(target_hall_index - source_hall_index)

    return cost(steps, amphipod)


def flatten_and_cost(game_state, destinations_for_candidates):

    possible_moves = []
    for key, value in destinations_for_candidates.items():
        for target in value:
            possible_moves.append((key, target, cost_for_move(game_state, key, target)))
    return possible_moves


def apply_move(game_state, move):
    source, target, cost = move
    new_game_state = copy.deepcopy(game_state)
    update_descriptor(new_game_state, target, amphipod_for_descriptor(new_game_state, source))
    update_descriptor(new_game_state, source, None)
    new_game_state['cost'] = game_state.get('cost') + cost
    return new_game_state


def filter_for_none(spots):
    return [spot for spot in spots if spot is not None]


def verify_game_state(game_state):
    assert "".join(
        sorted(
            filter_for_none(
                game_state.get("hall") + game_state.get("side_room_entrance") +
                game_state.get("side_room_rear")))) == "AABBCCDD"


def finished_game_state(game_state):

    try:
        verify_game_state(game_state)
        return "".join(filter_for_none(game_state.get('side_room_rear'))) == "ABCD" and "".join(
            filter_for_none(game_state.get('side_room_entrance'))) == "ABCD"
    except:
        print(game_state)
        raise


assert finished_game_state({
    'cost': 0,
    'side_room_rear': ['A', 'D', 'C', 'A'],
    'side_room_entrance': ['B', 'C', 'B', 'D'],
    'hall': [None, None, None, None, None, None, None, None, None, None, None]
}) == False
assert finished_game_state({
    'cost': 999,
    'side_room_rear': ['A', 'B', 'C', 'D'],
    'side_room_entrance': ['A', 'B', 'C', 'D'],
    'hall': [None, None, None, None, None, None, None, None, None, None, None]
}) == True

min_cost = 50000
min_state = {}


def brute_force(game_state):
    global min_cost
    global min_state

    if (finished_game_state(game_state)):
        if (game_state.get('cost') < min_cost):
            min_cost = game_state.get('cost')
            min_state = game_state
            print(min_state)
        return game_state.get('cost')

    # Abandon this path
    if (game_state.get('cost') > 20000):
        return None

    try:
        all_moves = flatten_and_cost(game_state, available_destinations(game_state))
    except:
        print(game_state)
        raise

    if (not all_moves):
        return None

    return [
        game_state_result
        for game_state_result in flatten([brute_force(apply_move(game_state, move)) for move in all_moves])
        if game_state_result is not None
    ]


real_game_state = read_game_state(real_data)
results = brute_force(real_game_state)
