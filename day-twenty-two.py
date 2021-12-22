import functools
import math
from enum import Enum
import numpy as np
import random
from itertools import groupby

def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, list) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x

my_test_data = ["on x=-100..100,y=-100..100,z=-100..100\n", "on x=-50..50,y=-50..50,z=-50..50\n"]

test_data_part_one = [
    "on x=-20..26,y=-36..17,z=-47..7\n", "on x=-20..33,y=-21..23,z=-26..28\n", "on x=-22..28,y=-29..23,z=-38..16\n",
    "on x=-46..7,y=-6..46,z=-50..-1\n", "on x=-49..1,y=-3..46,z=-24..28\n", "on x=2..47,y=-22..22,z=-23..27\n",
    "on x=-27..23,y=-28..26,z=-21..29\n", "on x=-39..5,y=-6..47,z=-3..44\n", "on x=-30..21,y=-8..43,z=-13..34\n",
    "on x=-22..26,y=-27..20,z=-29..19\n", "off x=-48..-32,y=26..41,z=-47..-37\n", "on x=-12..35,y=6..50,z=-50..-2\n",
    "off x=-48..-32,y=-32..-16,z=-15..-5\n", "on x=-18..26,y=-33..15,z=-7..46\n",
    "off x=-40..-22,y=-38..-28,z=23..41\n", "on x=-16..35,y=-41..10,z=-47..6\n", "off x=-32..-23,y=11..30,z=-14..3\n",
    "on x=-49..-5,y=-3..45,z=-29..18\n", "off x=18..30,y=-20..-8,z=-3..13\n", "on x=-41..9,y=-7..43,z=-33..15\n",
    "on x=-54112..-39298,y=-85059..-49293,z=-27449..7877\n", "on x=967..23432,y=45373..81175,z=27513..53682\n"
]

test_data_part_two = [
    "on x=-5..47,y=-31..22,z=-19..33\n", "on x=-44..5,y=-27..21,z=-14..35\n", "on x=-49..-1,y=-11..42,z=-10..38\n",
    "on x=-20..34,y=-40..6,z=-44..1\n", "off x=26..39,y=40..50,z=-2..11\n", "on x=-41..5,y=-41..6,z=-36..8\n",
    "off x=-43..-33,y=-45..-28,z=7..25\n", "on x=-33..15,y=-32..19,z=-34..11\n", "off x=35..47,y=-46..-34,z=-11..5\n",
    "on x=-14..36,y=-6..44,z=-16..29\n", "on x=-57795..-6158,y=29564..72030,z=20435..90618\n",
    "on x=36731..105352,y=-21140..28532,z=16094..90401\n", "on x=30999..107136,y=-53464..15513,z=8553..71215\n",
    "on x=13528..83982,y=-99403..-27377,z=-24141..23996\n", "on x=-72682..-12347,y=18159..111354,z=7391..80950\n",
    "on x=-1060..80757,y=-65301..-20884,z=-103788..-16709\n", "on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856\n",
    "on x=-52752..22273,y=-49450..9096,z=54442..119054\n", "on x=-29982..40483,y=-108474..-28371,z=-24328..38471\n",
    "on x=-4958..62750,y=40422..118853,z=-7672..65583\n", "on x=55694..108686,y=-43367..46958,z=-26781..48729\n",
    "on x=-98497..-18186,y=-63569..3412,z=1232..88485\n", "on x=-726..56291,y=-62629..13224,z=18033..85226\n",
    "on x=-110886..-34664,y=-81338..-8658,z=8914..63723\n", "on x=-55829..24974,y=-16897..54165,z=-121762..-28058\n",
    "on x=-65152..-11147,y=22489..91432,z=-58782..1780\n", "on x=-120100..-32970,y=-46592..27473,z=-11695..61039\n",
    "on x=-18631..37533,y=-124565..-50804,z=-35667..28308\n", "on x=-57817..18248,y=49321..117703,z=5745..55881\n",
    "on x=14781..98692,y=-1341..70827,z=15753..70151\n", "on x=-34419..55919,y=-19626..40991,z=39015..114138\n",
    "on x=-60785..11593,y=-56135..2999,z=-95368..-26915\n", "on x=-32178..58085,y=17647..101866,z=-91405..-8878\n",
    "on x=-53655..12091,y=50097..105568,z=-75335..-4862\n", "on x=-111166..-40997,y=-71714..2688,z=5609..50954\n",
    "on x=-16602..70118,y=-98693..-44401,z=5197..76897\n", "on x=16383..101554,y=4615..83635,z=-44907..18747\n",
    "off x=-95822..-15171,y=-19987..48940,z=10804..104439\n", "on x=-89813..-14614,y=16069..88491,z=-3297..45228\n",
    "on x=41075..99376,y=-20427..49978,z=-52012..13762\n", "on x=-21330..50085,y=-17944..62733,z=-112280..-30197\n",
    "on x=-16478..35915,y=36008..118594,z=-7885..47086\n", "off x=-98156..-27851,y=-49952..43171,z=-99005..-8456\n",
    "off x=2032..69770,y=-71013..4824,z=7471..94418\n", "on x=43670..120875,y=-42068..12382,z=-24787..38892\n",
    "off x=37514..111226,y=-45862..25743,z=-16714..54663\n", "off x=25699..97951,y=-30668..59918,z=-15349..69697\n",
    "off x=-44271..17935,y=-9516..60759,z=49131..112598\n", "on x=-61695..-5813,y=40978..94975,z=8655..80240\n",
    "off x=-101086..-9439,y=-7088..67543,z=33935..83858\n", "off x=18020..114017,y=-48931..32606,z=21474..89843\n",
    "off x=-77139..10506,y=-89994..-18797,z=-80..59318\n", "off x=8476..79288,y=-75520..11602,z=-96624..-24783\n",
    "on x=-47488..-1262,y=24338..100707,z=16292..72967\n", "off x=-84341..13987,y=2429..92914,z=-90671..-1318\n",
    "off x=-37810..49457,y=-71013..-7894,z=-105357..-13188\n", "off x=-27365..46395,y=31009..98017,z=15428..76570\n",
    "off x=-70369..-16548,y=22648..78696,z=-1892..86821\n", "on x=-53470..21291,y=-120233..-33476,z=-44150..38147\n",
    "off x=-93533..-4276,y=-16170..68771,z=-104985..-24507\n"
]


def process_lines(lines):
    def data_for_line(line):
        on, data = line.strip().split(" ")
        ranges = [[[int(value) for value in axis[2:].split("..")] for axis in data.split(",")]][0]
        return (1 if on == "on" else 0, ranges)

    return [data_for_line(line) for line in lines]


def inside_bounds(cube_range):
    return all([value <= 50 and value >= -50 for value in flatten(cube_range)])


def filter_bounds(ranges):
    return [cube_range for cube_range in ranges if inside_bounds(cube_range[1])]


f = open('day-twenty-two-input.txt')
real_data = f.readlines()
f.close()


def apply_range_naive(core_state, cube_range):

    on, cube_range_data = cube_range
    x_range, y_range, z_range = cube_range_data

    for x in range(x_range[0], x_range[1] + 1):
        for y in range(y_range[0], y_range[1] + 1):
            for z in range(z_range[0], z_range[1] + 1):
                core_state["%d:%d:%d" % (x, y, z)] = on

    return core_state


def intersection_range(axis_range, intersecting_axis_range):

    min_value, max_value = axis_range
    min_value_intersecting, max_value_intersecting = intersecting_axis_range

    if (max_value < min_value_intersecting or min_value > max_value_intersecting):
        return None

    # They overlap
    # [......(....].....)
    # (......[....).....]
    return [max(min_value, min_value_intersecting), min(max_value, max_value_intersecting)]


assert intersection_range([-100, 200], [100, 300]) == [100, 200]
assert intersection_range([-100, 100], [50, 50]) == [50, 50]
assert intersection_range([50, 50], [-100, 100]) == [50, 50]
assert intersection_range([-100, 100], [-100, 100]) == [-100, 100]


def add_intersection(cube, cube_range_data):
    # If this cube is on or off, it "takes" away volume from the existing cube where it intersects.

    overlaps = [intersection_range(cube.get("cube_range_data")[i], cube_range_data[i]) for i in range(0, 3)]
    if not all(overlaps):
        return

    cube.get("intersections").append(overlaps)


def apply_range_scale(core_state, cube_range):
    """
    Maybe state is a list of on cubes. Each cube has dimensions and a set of intersections.
    """
    on, new_cube_range_data = cube_range
    for cube in core_state:
        add_intersection(cube, new_cube_range_data)

    # If the cube is on, we will need to add intersections with later off and
    # on cubes (so we can remove their volume from this cube)
    #
    # If the cube is off we have already applied its intersections with all the
    # existing on cubes. so we can throw it away.
    new_cube = {"cube_range_data": new_cube_range_data, "intersections": []}
    if (on):
        core_state.append(new_cube)

    return core_state


def calculate_lit_cubes_for_scale(core_state):

    def size_of_edge(min_x, max_x):
        return ( max_x - min_x ) + 1

    def size_of_cube_or_intersection(cube_range_data):
        return functools.reduce(lambda current_size, edge_length: current_size * edge_length,
                                [size_of_edge(*axis_range) for axis_range in cube_range_data])

    def lit_for_cube_borken(cube):
        """
        This doesn't work because intersections intersect with each other
        """
        return size_of_cube_or_intersection(cube.get("cube_range_data")) - sum(
            [size_of_cube_or_intersection(intersection_data) for intersection_data in cube.get("intersections")])

    def lit_for_cube_naive(cube):
        """
        Nope. Ok of course, there are some big cubes here, so naive just wont fly
        """
        intersection_ranges = [[1, intersection] for intersection in cube.get("intersections")]
        intersection_volume = sum(apply_ranges(intersection_ranges, apply_range_naive, {}).values())
        this_cube_volume = size_of_cube_or_intersection(cube.get("cube_range_data"))
        assert this_cube_volume >= intersection_volume, "This cube volume %d, intersection %d" % (this_cube_volume, intersection_volume)
        return this_cube_volume - intersection_volume

    def lit_for_cube_intersection_inception(cube):
        """
        Ok ... what about ... not naive?
        """
        intersection_ranges = [[1, intersection] for intersection in cube.get("intersections")]
        intersection_volume = calculate_lit_cubes_for_scale(apply_ranges(intersection_ranges, apply_range_scale, []))
        this_cube_volume = size_of_cube_or_intersection(cube.get("cube_range_data"))
        assert this_cube_volume >= intersection_volume, "This cube volume %d, intersection %d" % (this_cube_volume, intersection_volume)
        return this_cube_volume - intersection_volume

    return sum([lit_for_cube_intersection_inception(cube) for i, cube in enumerate(core_state)])
    # return sum([lit_for_cube_naive(cube) for i, cube in enumerate(core_state)])


def apply_ranges(ranges, fn, core_state):
    for cube_range in ranges:
        core_state = fn(core_state, cube_range)
    return core_state


expected_on_cubes = 590784
test_ranges = filter_bounds(process_lines(test_data_part_one))
real_ranges = filter_bounds(process_lines(real_data))
assert sum(apply_ranges(test_ranges, apply_range_naive, {}).values()) == expected_on_cubes
assert calculate_lit_cubes_for_scale(apply_ranges(test_ranges, apply_range_scale, [])) == expected_on_cubes
# print(sum(apply_ranges(real_ranges, apply_range_naive, {}).values()))

expected_on_cubes_part_two = 2758514936282235
test_ranges = process_lines(test_data_part_two)
real_ranges = process_lines(real_data)

assert calculate_lit_cubes_for_scale(apply_ranges(test_ranges, apply_range_scale, [])) == expected_on_cubes_part_two
print(calculate_lit_cubes_for_scale(apply_ranges(real_ranges, apply_range_scale, [])))

