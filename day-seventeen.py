import functools
from enum import Enum
from itertools import groupby


def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, list) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


# The probe's x position increases by its x velocity.
# The probe's y position increases by its y velocity.
# Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
# Due to gravity, the probe's y velocity decreases by 1


def simulate_step(position, velocity):
    x, y = position
    x_velocity, y_velocity = velocity

    new_position = (x + x_velocity, y + y_velocity)
    x_velocity_change = -1 if x_velocity > 0 else 1
    new_x_velocity = (x_velocity + x_velocity_change) if x_velocity != 0 else 0
    new_y_velocity = y_velocity - 1
    return new_position, (new_x_velocity, new_y_velocity)


def position_in_target(position, target):
    x, y = position
    min_x, max_x, min_y, max_y = target
    return (x >= min_x and x <= max_x) and (y >= min_y and y <= max_y)


def position_past_target(position, target):
    x, y = position
    min_x, max_x, min_y, max_y = target
    return x > max_x or y < min_y


def parse_input(line):

    x_values, y_values = line[15:].split(", y=")
    min_x, max_x = x_values.split("..")
    min_y, max_y = y_values.split("..")

    return tuple(int(value) for value in (min_x, max_x, min_y, max_y))


def try_starting_velocity(target, velocity):
    position = (0, 0)
    max_y = 0
    while (True):
        position, velocity = simulate_step(position, velocity)
        max_y = max(max_y, position[1])
        if (position_in_target(position, target)):
            return max_y, True
        if (position_past_target(position, target)):
            return -1, False


brute_force_range = range(-200, 200)

def calculated_maximum_y(target):
    # attempt a range of starting velocities
    attempts = flatten(
        [[try_starting_velocity(target, (test_x_velocity, test_y_velocity)) for test_x_velocity in brute_force_range]
         for test_y_velocity in brute_force_range])
    return max([attempt[0] for attempt in attempts]) if attempts else 0


def calculate_firing_solutions(target):
    attempts = flatten([[(try_starting_velocity(target,
                                                (test_x_velocity, test_y_velocity)), test_x_velocity, test_y_velocity)
                         for test_x_velocity in brute_force_range] for test_y_velocity in brute_force_range])
    return {(test_x_velocity, test_y_velocity) for result, test_x_velocity, test_y_velocity in attempts if result[1]}


assert parse_input("target area: x=20..30, y=-10..-5") == (20, 30, -10, -5)

target = parse_input("target area: x=139..187, y=-148..-89")

# Part One
expected_maximum_y = 45
test_maximum_y = calculated_maximum_y(parse_input("target area: x=20..30, y=-10..-5"))
assert test_maximum_y == expected_maximum_y

# Real target
maximum_y = calculated_maximum_y(target)
# 1225 too low with a 50 range
# next attempt with 200 range -> 10878 ... confirmed this is the max with a 400 range.

# Part Two
expected_firing_solutions_count = 112
firing_solutions = calculate_firing_solutions(parse_input("target area: x=20..30, y=-10..-5"))
assert len(firing_solutions) == expected_firing_solutions_count

# Again with the real target
firing_solutions = calculate_firing_solutions(target)
