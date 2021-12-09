import functools
import pygame
from enum import Enum


def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, list) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


test_data = [
    "2199943210\n",
    "3987894921\n",
    "9856789892\n",
    "8767896789\n",
    "9899965678\n",
]

expected_risk_level_sum = 15
expected_top_three_basin_size_multiple = 1134


def calculate_risk_level(height):
    return height + 1


def show_heightmap(heightmap, width, height):
    for y in range(0, height):
        for x in range(0, width):
            index = (width * y) + x
            print("%d:%d " % (index, heightmap[index]), end="")
        print("")


def in_range(heightmap, cell_index):
    return cell_index >= 0 and cell_index < len(heightmap)


def is_first_cell_in_row(width, cell_index):
    return cell_index % width == 0


def top(heightmap, width, height, cell_index):
    offset_index = cell_index - width
    return offset_index if in_range(heightmap, offset_index) else None


def bottom(heightmap, width, height, cell_index):
    offset_index = cell_index + width
    return offset_index if in_range(heightmap, offset_index) else None


def left(heightmap, width, height, cell_index):
    offset_index = cell_index - 1 if not is_first_cell_in_row(width, cell_index) else -1
    return offset_index if in_range(heightmap, offset_index) else None


def right(heightmap, width, height, cell_index):
    offset_index = cell_index + 1 if not is_first_cell_in_row(width, cell_index + 1) else -1
    return offset_index if in_range(heightmap, offset_index) else None


def adjacent_cell_indicies(heightmap, width, height, cell_index):
    return [
        adjacent_cell_index for adjacent_cell_index in [
            top(heightmap, width, height, cell_index),
            bottom(heightmap, width, height, cell_index),
            left(heightmap, width, height, cell_index),
            right(heightmap, width, height, cell_index)
        ] if adjacent_cell_index is not None
    ]


# 00:2 1:1  2:9  3:9  4:9  5:4  6:3  7:2  8:1  9:0
# 10:3 11:9 12:8 13:7 14:8 15:9 16:4 17:9 18:2 19:1
# 20:9 21:8 22:5 23:6 24:7 25:8 26:9 27:8 28:9 29:2
# 30:8 31:7 32:6 33:7 34:8 35:9 36:6 37:7 38:8 39:9
# 40:9 41:8 42:9 43:9 44:9 45:6 46:5 47:6 48:7 49:8


def is_minimum_cell(heightmap, width, height, cell_index):
    min_adjacent_cell_value = min(
        [heightmap[adjacent_index] for adjacent_index in adjacent_cell_indicies(heightmap, width, height, cell_index)])
    return heightmap[cell_index] < min_adjacent_cell_value


def get_min_cell_indicies(heightmap, width, height):
    return [
        cell_index for cell_index in range(0, len(heightmap)) if is_minimum_cell(heightmap, width, height, cell_index)
    ]


def calculate_risk_sum(heightmap, width, height):
    return sum([
        calculate_risk_level(heightmap[a_min_cell_index])
        for a_min_cell_index in get_min_cell_indicies(heightmap, width, height)
    ])


def process_lines(lines):
    # have to account for the end of line in this data
    width = len(lines[0]) - 1
    height = len(lines)
    heightmap = list(flatten([[int(c) for c in line if c != '\n'] for line in lines]))
    return (heightmap, width, height)


def expand_basin_set(heightmap, width, height, cell_index, current_basin):
    current_value = heightmap[cell_index]
    current_basin_size = len(current_basin)
    # expand the basin set from any adjacent cells that are higher than our current cell (and aren't 9)
    candidate_indicies = {
        adjacent_cell_index
        for adjacent_cell_index in adjacent_cell_indicies(heightmap, width, height, cell_index)
        if heightmap[adjacent_cell_index] > current_value and heightmap[adjacent_cell_index] != 9
    }
    current_basin = current_basin.union(candidate_indicies)
    for candidate_index in candidate_indicies:
        current_basin = current_basin.union(expand_basin_set(heightmap, width, height, candidate_index, current_basin))
    return current_basin


def find_basin_sets(heightmap, width, height):
    return [
        expand_basin_set(heightmap, width, height, min_cell_index, {min_cell_index})
        for min_cell_index in get_min_cell_indicies(heightmap, width, height)
    ]


def multiplied_top_three_basin_set_sizes(heightmap, width, height):
    top_basin_sets = sorted(find_basin_sets(heightmap, width, height),
                            key=lambda current_set: len(current_set),
                            reverse=True)[:3]
    return functools.reduce((lambda x, y: x * y), [len(basin_set) for basin_set in top_basin_sets])


f = open('day-nine-input.txt')
real_data = f.readlines()
f.close()

# Part One
test_risk_sum = calculate_risk_sum(*process_lines(test_data))
print(test_risk_sum)
print(str(test_risk_sum == expected_risk_level_sum))
print(calculate_risk_sum(*process_lines(real_data)))

# Part Two
multiple_top_three_basin_set_sizes = multiplied_top_three_basin_set_sizes(*process_lines(test_data))
print(multiple_top_three_basin_set_sizes)
print(str(multiple_top_three_basin_set_sizes == expected_top_three_basin_size_multiple))
print(multiplied_top_three_basin_set_sizes(*process_lines(real_data)))
