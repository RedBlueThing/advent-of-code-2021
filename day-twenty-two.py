import functools
import math
from enum import Enum
import numpy as np
import random
from itertools import groupby

test_data = [
    "on x=-20..26,y=-36..17,z=-47..7\n", "on x=-20..33,y=-21..23,z=-26..28\n", "on x=-22..28,y=-29..23,z=-38..16\n",
    "on x=-46..7,y=-6..46,z=-50..-1\n", "on x=-49..1,y=-3..46,z=-24..28\n", "on x=2..47,y=-22..22,z=-23..27\n",
    "on x=-27..23,y=-28..26,z=-21..29\n", "on x=-39..5,y=-6..47,z=-3..44\n", "on x=-30..21,y=-8..43,z=-13..34\n",
    "on x=-22..26,y=-27..20,z=-29..19\n", "off x=-48..-32,y=26..41,z=-47..-37\n", "on x=-12..35,y=6..50,z=-50..-2\n",
    "off x=-48..-32,y=-32..-16,z=-15..-5\n", "on x=-18..26,y=-33..15,z=-7..46\n",
    "off x=-40..-22,y=-38..-28,z=23..41\n", "on x=-16..35,y=-41..10,z=-47..6\n", "off x=-32..-23,y=11..30,z=-14..3\n",
    "on x=-49..-5,y=-3..45,z=-29..18\n", "off x=18..30,y=-20..-8,z=-3..13\n", "on x=-41..9,y=-7..43,z=-33..15\n",
    "on x=-54112..-39298,y=-85059..-49293,z=-27449..7877\n", "on x=967..23432,y=45373..81175,z=27513..53682\n"
]


def process_lines(lines):
    def data_for_line(line):
        on_or_off, data = line.strip().split(" ")
        ranges = [[[int(value) for value in axis[2:].split("..")] for axis in data.split(",")]][0]
        return (1 if on_or_off == "on" else 0, ranges)

    return [data_for_line(line) for line in lines]

def inside_bounds(cube_range):
    return all([value <= 50 and value >= -50 for value in flatten(cube_range)])

def filter_bounds(ranges):
    return [cube_range for cube_range in ranges if inside_bounds(cube_range[1])]

f = open('day-twenty-two-input.txt')
real_data = f.readlines()
f.close()

def apply_range_naive(core_state, cube_range):

    print(cube_range)
    on_or_off, data = cube_range
    x_range, y_range, z_range = data

    for x in range(x_range[0],x_range[1] + 1):
        for y in range(y_range[0],y_range[1] + 1):
            for z in range(z_range[0],z_range[1] + 1):
                core_state["%d:%d:%d" % (x,y,z)] = on_or_off

    return core_state

def apply_range_giant_brain(core_state, cube_range):

    print(cube_range)
    on_or_off, data = cube_range
    x_range, y_range, z_range = data

    for x in range(x_range[0],x_range[1] + 1):
        for y in range(y_range[0],y_range[1] + 1):
            for z in range(z_range[0],z_range[1] + 1):
                core_state["%d:%d:%d" % (x,y,z)] = on_or_off

    return core_state


def apply_ranges(ranges, fn):
    core_state = {}
    for cube_range in ranges:
        core_state = fn(core_state, cube_range)
    return core_state

expected_on_cubes = 590784
test_ranges = filter_bounds(process_lines(test_data))
real_ranges = filter_bounds(process_lines(real_data))
assert sum(apply_ranges(test_ranges, apply_range_naive).values()) == expected_on_cubes
print(sum(apply_ranges(real_ranges, apply_range_naive).values()))

expected_on_cubes_part_two = 2758514936282235
test_ranges = process_lines(test_data)
real_ranges = process_lines(real_data)
# assert sum(apply_ranges(test_ranges, apply_range_giant_brain).values()) == expected_on_cubes_part_two
# print(sum(apply_ranges(real_ranges, apply_range_giant_brain).values()))
