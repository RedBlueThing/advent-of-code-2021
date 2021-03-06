import functools
import pygame
from itertools import groupby

test_data = "3,4,3,1,2"

expected_fish_after_18_days = 26
expected_fish_after_80_days = 5934
expected_fish_after_256_days = 26984457539

f = open('day-six-input.txt')
real_data = f.readlines()[0]
f.close()


def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, list) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


def group_by_timer(data):
    data = sorted(data)
    grouped_data = {k: len(list(g)) for k, g in groupby(data)}
    # This version groups by the fish we have, but actually we want to just have zero counts up to the 8 slot
    # return [0 if grouped_data.get(x) is None else grouped_data.get(x) for x in range(0, max(data) + 1)]
    return [0 if grouped_data.get(x) is None else grouped_data.get(x) for x in range(0, 9)]


def timers_for_fish(data):
    return [int(x) for x in data.split(",")]


def breed_version_one(fish):
    return list(flatten([current_fish - 1 if current_fish > 0 else [6, 8] for current_fish in fish]))


def breed_version_two(fish):
    breeding_fish = fish[0]
    # add the offspring
    shifted_fish = fish[1:] + [breeding_fish]
    # Then stick the breeding fish back in slot 6
    shifted_fish[6] += breeding_fish
    return shifted_fish


def simulate_version_one(fish, days_remaining):
    if (days_remaining == 0):
        return len(fish)
    return simulate_version_one(breed_version_one(fish), days_remaining - 1)


def simulate_version_two(fish, days_remaining):
    if (days_remaining == 0):
        return sum(fish)
    return simulate_version_two(breed_version_two(fish), days_remaining - 1)


print(simulate_version_one(timers_for_fish(test_data), 18) == expected_fish_after_18_days)
print(simulate_version_one(timers_for_fish(test_data), 80) == expected_fish_after_80_days)
print(simulate_version_two(group_by_timer(timers_for_fish(test_data)), 18) == expected_fish_after_18_days)
print(simulate_version_two(group_by_timer(timers_for_fish(test_data)), 256) == expected_fish_after_256_days)
print(simulate_version_two(group_by_timer(timers_for_fish(real_data)), 256))
