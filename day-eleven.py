import functools
from enum import Enum

test_data = [
'5483143223',
'2745854711',
'5264556173',
'6141336146',
'6357385478',
'4167524645',
'2176841721',
'6882881134',
'4846848554',
'5283751526'
]

real_data = [ '7222221271',
'6463754232',
'3373484684',
'4674461265',
'1187834788',
'1175316351',
'8211411846',
'4657828333',
'5286325337',
'5771324832' ]

expected_flashes_after_one_hundred_steps = 1656

def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, list) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x

def process_data(raw_data):
    # have to account for the end of line in this data
    width = len(raw_data[0]) - 1
    height = len(raw_data)
    powermap = list(flatten([[int(c) for c in line if c != '\n'] for line in raw_data]))
    return (powermap, width, height)

def increment_power(powermap, width, height):
    return [octopus_power + 1 for octopus_power in powermap ]

def count_flashes(powermap, width, height, remaining_steps, current_flashes):

    if (remaining_steps == 0):
        return current_flashes

    # Otherwise we have at least one more step to calculate
    powermap = increment_power(powermap, width, height)

    return count_flashes(powermap, width, height, remaining_steps-1, current_flashes)

# Part One
flashes = count_flashes(*(process_data(test_data) + (100,0)))
assert flashes == expected_flashes_after_one_hundred_steps, "Flashes was %d" % flashes
