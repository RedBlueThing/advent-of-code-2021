import functools
import math
from enum import Enum
import random
import copy
from itertools import groupby
import heapq

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
part_two_real_data = real_data[:3] + part_two_insert + real_data[3:]
part_two_test_data = test_data[:3] + part_two_insert + test_data[3:]

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
part_one_real_no_constraints_cost = cost(7, 'D') + cost(8, 'D') + cost(9, 'A') + cost(5, 'A') + cost(5, 'B') + cost(
    4, 'B') + cost(6, 'C') + cost(7, 'C')
#
# The no constraints cost could be the "admissible" (never overestimates the cost) heursitic for A* search!!!! So
# I need a function to calculate this automagically!

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

    hall = lines[1].strip()[1:-1]
    side_rooms = []
    for line in lines[2:]:
        split_line = line.strip().strip("#").split("#")
        if (len(split_line) > 1):
            side_rooms.append(none_or_amphipod(split_line))

    return {"cost": 0, "side_rooms": side_rooms, "hall": none_or_amphipod(hall)}


def key_for_game_state(game_state):
    return "".join([x or "." for x in list(flatten(game_state.get('side_rooms'))) + game_state.get("hall")])


y = key_for_game_state(read_game_state(test_data))


def amphipod_for_descriptor(game_state, descriptor):
    key, index = descriptor.split(":")
    if ("side_rooms" in descriptor):
        key, depth_index = key.split("-")
        try:
            return game_state[key][int(depth_index)][int(index)]
        except:
            print(game_state)
            print(descriptor)
            raise

    return game_state[key][int(index)]


def update_descriptor(game_state, descriptor, new_value):
    key, index = descriptor.split(":")

    if ("side_rooms" in descriptor):
        key, depth_index = key.split("-")
        game_state[key][int(depth_index)][int(index)] = new_value
    else:
        game_state[key][int(index)] = new_value


def descriptor_for_key_and_index(key, index):
    return "%s:%d" % (key, index)


def index_for_descriptor(descriptor):
    return int(descriptor.split(":")[1])


def hall_descriptor(descriptor):
    return "hall" in descriptor


def entrance_descriptor(descriptor):
    return "side_rooms-0" in descriptor


def steps_to_side_room_descriptor(descriptor):
    assert "side_rooms" in descriptor
    key, index = descriptor.split(":")
    key, depth_index = key.split("-")
    return int(depth_index) + 1


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


def side_rooms_for_index(game_state, target_room_index):
    return [x[target_room_index] for x in game_state.get('side_rooms')]


def available_target_room(game_state, descriptor, target_room_index):

    free_spots = [x is None for x in side_rooms_for_index(game_state, target_room_index)]
    if all(free_spots):
        return True
    if not any(free_spots):
        return False

    our_amphipod = amphipod_for_descriptor(game_state, descriptor)
    return all([x == our_amphipod for x in side_rooms_for_index(game_state, target_room_index) if x is not None])


def available_to_move(game_state):
    """
    Return a list of amphipods that can move
    """
    room_candidates = []

    # for each of the side rooms (corridors)
    for index in range(0, len(game_state.get("side_rooms")[0])):

        # If any one in this list doesn't belong here, then we need to move the top one
        side_rooms_for_this_index = side_rooms_for_index(game_state, index)
        if (any([target_room_index_for_amphipod(x) != index for x in side_rooms_for_this_index if x is not None])):
            first_ampipod_index = len([x for x in side_rooms_for_this_index if x is None])
            room_candidates.append(descriptor_for_key_and_index("side_rooms-%d" % first_ampipod_index, index))

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
    "room_candidates": ['side_rooms-0:0', 'side_rooms-0:1', 'side_rooms-0:2', 'side_rooms-0:3'],
    "hall_candidates": []
}
assert available_to_move(
    read_game_state(["#############\n", "#..........A#\n", "###.#C#B#D###\n", "  #A#D#C#A#\n", "  #########\n"])) == {
        "room_candidates": ['side_rooms-0:1', 'side_rooms-0:2', 'side_rooms-0:3'],
        "hall_candidates": ['hall:10']
    }
assert available_to_move(
    read_game_state(["#############\n", "#..........A#\n", "###.#C#B#D###\n", "  #D#A#C#A#\n", "  #########\n"])) == {
        "room_candidates": ['side_rooms-1:0', 'side_rooms-0:1', 'side_rooms-0:2', 'side_rooms-0:3'],
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
        side_rooms_for_this_index = side_rooms_for_index(game_state, target_room_index)
        free_depth_index = len([x for x in side_rooms_for_this_index if x is None]) - 1
        return [descriptor_for_key_and_index("side_rooms-%d" % free_depth_index, target_room_index)]

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
                     "  #########\n"]))['side_rooms-0:1'] == ['hall:3', 'hall:5', 'hall:7', 'hall:9', 'hall:10']
assert available_destinations(
    read_game_state(["#############\n", "#.A.........#\n", "###.#C#.#B###\n", "  #A#D#.#A#\n",
                     "  #########\n"]))['side_rooms-0:1'] == ['side_rooms-1:2']
assert available_destinations(
    read_game_state(["#############\n", "#.A...D.....#\n", "###.#C#.#B###\n", "  #A#D#.#A#\n",
                     "  #########\n"]))['side_rooms-0:1'] == ['hall:3']
assert available_destinations(
    read_game_state(["#############\n", "#C....D....C#\n", "###A#B#.#.###\n", "  #A#B#.#D#\n",
                     "  #########\n"]))['hall:5'] == ['side_rooms-0:3']


def cost_for_move(game_state, source, target):

    # first, which amphipod is moving?
    steps = 0
    amphipod = amphipod_for_descriptor(game_state, source)

    # print("%s -> %s" % (source, target))

    # If they are moving from the hall?
    if (hall_descriptor(source)):
        target_hall_index = hall_index_for_room_index(index_for_descriptor(target))
        steps += abs(target_hall_index - index_for_descriptor(source))
        steps += steps_to_side_room_descriptor(target)
    elif hall_descriptor(target):
        # Just move into the side room
        steps += steps_to_side_room_descriptor(source)
        # move from the side room to the spot in the hall
        target_hall_index = index_for_descriptor(target)
        source_hall_index = hall_index_for_room_index(index_for_descriptor(source))
        steps += abs(target_hall_index - source_hall_index)
    else:
        # move from and to the side room
        steps += steps_to_side_room_descriptor(source)
        steps += steps_to_side_room_descriptor(target)
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


def finished_game_state(game_state):

    try:
        return all(["".join(filter_for_none(x)) == "ABCD" for x in game_state.get("side_rooms")])
    except:
        print(game_state)
        raise


assert finished_game_state({
    'cost':
    0,
    'side_rooms': [['B', 'C', 'B', 'D'], ['D', 'C', 'B', 'A'], ['D', 'B', 'A', 'C'], ['A', 'D', 'C', 'A']],
    'hall': [None, None, None, None, None, None, None, None, None, None, None]
}) == False
assert finished_game_state({
    'cost':
    999,
    'side_rooms': [['A', 'B', 'C', 'D'], ['A', 'B', 'C', 'D'], ['A', 'B', 'C', 'D'], ['A', 'B', 'C', 'D']],
    'hall': [None, None, None, None, None, None, None, None, None, None, None]
}) == True


def brute_force(game_state):

    if (finished_game_state(game_state)):
        return game_state.get('cost')

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


def heuristic_solution_cost(game_state):
    """
    This function uses the "no constraints cost" to get to the completed game
    state for this game state. Because this will always be less than the actual
    cost, we can use this for the A* search heuristic.
    """
    heuristic_cost = 0
    # Just move to the same row in the right room index. So The cost is less
    # than the "no constraints" cost I created manually.
    for row_index, side_room_row in enumerate(game_state.get("side_rooms")):
        for index, amphipod in enumerate(side_room_row):
            if (amphipod is None):
                continue
            target_room_index = target_room_index_for_amphipod(amphipod)
            if target_room_index != index:
                heuristic_cost += cost_for_move(
                    game_state, descriptor_for_key_and_index("side_rooms-%d" % row_index, index),
                    descriptor_for_key_and_index("side_rooms-%d" % row_index, target_room_index))

    # Don't want to keep track of the free spots in the side rooms, so our
    # heuristic will just calculate the move from the hall to the first room
    # spot. Stays admissible because that cost will always be less than or
    # equal the actual cost to move these guys from the hall to their target
    # rooms.
    for hall_index, amphipod in enumerate(game_state.get('hall')):
        if (amphipod is None):
            continue
        target_room_index = target_room_index_for_amphipod(amphipod)
        heuristic_cost += cost_for_move(game_state, descriptor_for_key_and_index("hall", hall_index),
                                        descriptor_for_key_and_index("side_rooms-0", target_room_index))

    return heuristic_cost


class PriorityElem:
    def __init__(self, elem_to_wrap, priority):
        self.wrapped_elem = elem_to_wrap
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority


def a_star(game_state):
    def push_game_state(open_set, game_state):
        try:
            heapq.heappush(open_set,
                           PriorityElem(game_state,
                                        game_state.get("cost") + heuristic_solution_cost(game_state)))
        except:
            print(game_state)
            raise

    def pop_game_state(open_set):
        return heapq.heappop(open_set).wrapped_elem

    open_set = []

    # start with the initial node
    push_game_state(open_set, game_state)

    g_scores = {key_for_game_state(game_state): 0}

    while (open_set):

        current = pop_game_state(open_set)

        if (finished_game_state(current)):
            return current

        all_moves = flatten_and_cost(current, available_destinations(current))

        for move in all_moves:
            neighbour_game_state = apply_move(current, move)

            current_g_score = g_scores.get(key_for_game_state(neighbour_game_state))
            if current_g_score is None or neighbour_game_state.get("cost") < current_g_score:
                g_scores[key_for_game_state(neighbour_game_state)] = neighbour_game_state.get("cost")
                push_game_state(open_set, neighbour_game_state)


# part two
# test_game_state = read_game_state(part_two_test_data)
# results = a_star(test_game_state)
# test_game_state = read_game_state(test_data)
# results = a_star(test_game_state)
real_game_state = read_game_state(part_two_real_data)
results = a_star(real_game_state)
