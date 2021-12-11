import functools
from enum import Enum
from itertools import groupby

test_data = [
    '5483143223', '2745854711', '5264556173', '6141336146', '6357385478', '4167524645', '2176841721', '6882881134',
    '4846848554', '5283751526'
]

real_data = [
    '7222221271', '6463754232', '3373484684', '4674461265', '1187834788', '1175316351', '8211411846', '4657828333',
    '5286325337', '5771324832'
]

expected_flashes_after_one_hundred_steps = 1656
first_step_all_flash = 195


def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, list) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


def process_data(raw_data):
    width = len(raw_data[0]) 
    height = len(raw_data)
    powermap = list(flatten([[int(c) for c in line if c != '\n'] for line in raw_data]))
    return (powermap, width, height)


def group_by_index(data):
    return {k: len(list(g)) for k, g in groupby(sorted(data))}


assert group_by_index([1, 2, 1, 2, 3, 3, 3, 3]) == {1: 2, 2: 2, 3: 4}


def increment_power(powermap, indicies):

    increment_dict = group_by_index(indicies)

    def new_value(index, power):
        return power + increment_dict.get(index) if increment_dict.get(index) is not None else power

    return [new_value(index, octopus_power) for index, octopus_power in enumerate(powermap)]


def flash(powermap, indicies):

    increment_dict = group_by_index(indicies)

    def flashed_value(index, power):
        return 0 if increment_dict.get(index) is not None else power

    return [flashed_value(index, octopus_power) for index, octopus_power in enumerate(powermap)]


def get_flashing_indicies(powermap):

    return {i for i, value in enumerate(powermap) if value > 9}


def in_range(powermap, cell_index):
    return cell_index >= 0 and cell_index < len(powermap)


def is_first_cell_in_row(width, cell_index):
    return cell_index % width == 0


def top(powermap, width, height, cell_index):
    offset_index = cell_index - width
    return offset_index if in_range(powermap, offset_index) else None


def bottom(powermap, width, height, cell_index):
    offset_index = cell_index + width
    return offset_index if in_range(powermap, offset_index) else None


def left(powermap, width, height, cell_index):
    if cell_index is None:
        return None
    offset_index = cell_index - 1 if not is_first_cell_in_row(width, cell_index) else -1
    return offset_index if in_range(powermap, offset_index) else None


def right(powermap, width, height, cell_index):
    if cell_index is None:
        return None
    offset_index = cell_index + 1 if not is_first_cell_in_row(width, cell_index + 1) else -1
    return offset_index if in_range(powermap, offset_index) else None


def adjacent_cell_indicies(powermap, width, height, cell_index):
    return [
        adjacent_cell_index for adjacent_cell_index in [
            top(powermap, width, height, cell_index),
            # top right and top left
            right(powermap, width, height, top(powermap, width, height, cell_index)),
            left(powermap, width, height, top(powermap, width, height, cell_index)),
            bottom(powermap, width, height, cell_index),
            # then bottom right and bottom left
            right(powermap, width, height, bottom(powermap, width, height, cell_index)),
            left(powermap, width, height, bottom(powermap, width, height, cell_index)),
            left(powermap, width, height, cell_index),
            right(powermap, width, height, cell_index)
        ] if adjacent_cell_index is not None
    ]


def show_powermap(powermap, width, height):
    for y in range(0, height):
        for x in range(0, width):
            index = (width * y) + x
            print("\t%02d:%02d " % (index, powermap[index]), end="")
        print("")


def propagate_flashes(powermap, width, height, newly_flashing_indicies):
    # Get a list of indicies that we will increment
    indicies_to_increment = list(
        flatten([adjacent_cell_indicies(powermap, width, height, index) for index in newly_flashing_indicies]))
    pre_flashing_indicies = get_flashing_indicies(powermap)
    powermap = increment_power(powermap, indicies_to_increment)
    post_flashing_indicies = get_flashing_indicies(powermap)
    # now compare our current flashing cells to what we had before the increment
    next_lot_of_flashing_indicies = post_flashing_indicies.difference(pre_flashing_indicies)
    # if we don't have any more flashing cells, time to unroll
    if (len(next_lot_of_flashing_indicies) == 0):
        if (len(post_flashing_indicies) == width * height):
            assert False
        powermap = flash(powermap, list(post_flashing_indicies))
        return (len(post_flashing_indicies), powermap)

    return propagate_flashes(powermap, width, height, next_lot_of_flashing_indicies)


def count_flashes(powermap, width, height, remaining_steps, current_flashes):

    if (remaining_steps == 0):
        return current_flashes

    # Otherwise we have at least one more step to calculate
    powermap = increment_power(powermap, list(range(0, len(powermap))))

    # propagate flashes
    new_flashes, powermap = propagate_flashes(powermap, width, height, get_flashing_indicies(powermap))
    print (remaining_steps - 1)

    return count_flashes(powermap, width, height, remaining_steps - 1, current_flashes + new_flashes)


# Part One
# flashes = count_flashes(*(process_data(test_data) + (100, 0)))
# assert flashes == expected_flashes_after_one_hundred_steps, "Flashes was %d" % flashes
# flashes = count_flashes(*(process_data(real_data) + (100, 0)))
# print(flashes)
# Party Two
flashes = count_flashes(*(process_data(real_data) + (500, 0)))

(500 - 167) + 1
