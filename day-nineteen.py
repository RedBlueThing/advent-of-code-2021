import functools
import math
from enum import Enum
import numpy as np


def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, list) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


f = open('day-nineteen-input.txt')
real_data = [line.strip() for line in f.readlines()]
f.close()

f = open('test-day-nineteen-input.txt')
test_data = [line.strip() for line in f.readlines()]
f.close()

test_expected_beacons_relative_to_first_scanner = [(-892, 524, 684), (-876, 649, 763), (-838, 591, 734),
                                                   (-789, 900, -551), (-739, -1745, 668), (-706, -3180, -659),
                                                   (-697, -3072, -689), (-689, 845, -530), (-687, -1600, 576),
                                                   (-661, -816, -575), (-654, -3158, -753), (-635, -1737, 486),
                                                   (-631, -672, 1502), (-624, -1620, 1868), (-620, -3212, 371),
                                                   (-618, -824, -621), (-612, -1695, 1788), (-601, -1648, -643),
                                                   (-584, 868, -557), (-537, -823, -458), (-532, -1715, 1894),
                                                   (-518, -1681, -600), (-499, -1607, -770), (-485, -357, 347),
                                                   (-470, -3283, 303), (-456, -621, 1527), (-447, -329, 318),
                                                   (-430, -3130, 366), (-413, -627, 1469), (-345, -311, 381),
                                                   (-36, -1284, 1171), (-27, -1108, -65), (7, -33, -71),
                                                   (12, -2351, -103), (26, -1119, 1091), (346, -2985, 342),
                                                   (366, -3059, 397), (377, -2827, 367), (390, -675, -793),
                                                   (396, -1931, -563), (404, -588, -901), (408, -1815, 803),
                                                   (423, -701, 434), (432, -2009, 850), (443, 580, 662),
                                                   (455, 729, 728), (456, -540, 1869), (459, -707, 401),
                                                   (465, -695, 1988), (474, 580, 667), (496, -1584, 1900),
                                                   (497, -1838, -617), (527, -524, 1933), (528, -643, 409),
                                                   (534, -1912, 768), (544, -627, -890), (553, 345, -567),
                                                   (564, 392, -477), (568, -2007, -577), (605, -1665, 1952),
                                                   (612, -1593, 1893), (630, 319, -379), (686, -3108, -505),
                                                   (776, -3184, -501), (846, -3110, -434), (1135, -1161, 1235),
                                                   (1243, -1093, 1063), (1660, -552, 429), (1693, -557, 386),
                                                   (1735, -437, 1738), (1749, -1800, 1813), (1772, -405, 1572),
                                                   (1776, -675, 371), (1779, -442, 1789), (1780, -1548, 337),
                                                   (1786, -1538, 337), (1847, -1591, 415), (1889, -1729, 1762),
                                                   (1994, -1805, 1792)]


def process_lines(lines):

    current_index = 0
    scanners = []

    for line in lines:
        if ("---" in line):
            current_index = int(line.split(" ")[2])
            scanners.append([])
            continue
        if (line):
            scanners[current_index].append(tuple([int(x) for x in line.split(',')]))

    return scanners


# Distance between two points in 3D space
# ((x2 - x1)2 + (y2 - y1)2 + (z2 - z1)2)1/2


def distance(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return math.sqrt((math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) + math.pow(z2 - z1, 2)))


def distance_map(scanner_data):
    return [[distance(p1, p2) for p1 in scanner_data] for p2 in scanner_data]


def isclose(value1, value2):
    return math.isclose(value1, value2, rel_tol=0, abs_tol=0.001)


def compare_scanner_distance_data(distance_maps):

    matching_points = set()

    # Compare every scanner to every other scanner
    for first_scanner_index, first_scanner_distance_map in enumerate(distance_maps):
        for second_scanner_index, second_scanner_distance_map in enumerate(distance_maps):
            if (first_scanner_index == second_scanner_index):
                continue

            for first_scanner_point_index, first_scanner_point_distance_map in enumerate(first_scanner_distance_map):
                for second_scanner_point_index, second_scanner_point_distance_map in enumerate(
                        second_scanner_distance_map):
                    if (len([
                            isclose for isclose in (flatten([[
                                isclose(first_scanner_distance, second_scanner_distance)
                                for first_scanner_distance in first_scanner_point_distance_map
                            ] for second_scanner_distance in second_scanner_point_distance_map])) if isclose
                    ]) >= 12):
                        # test_scanner_data[first_scanner_index][first_scanner_points_index] ===
                        # test_scanner_data[second_scanner_index][second_scanner_points_index]
                        matching_points.add(
                            tuple(
                                sorted(((first_scanner_index, first_scanner_point_index),
                                        (second_scanner_index, second_scanner_point_index)))))

    return sorted(matching_points)


def filter_matching_points(matching_points, from_scanner, to_scanner):
    return [
        point for point in matching_points
        if point[0][0] in [from_scanner, to_scanner] and point[1][0] in [from_scanner, to_scanner]
    ]


def get_affine_transformations(matching_points, from_scanner, to_scanner, scanner_data):
    def index_for_point(point, scanner):
        if (point[0][0] == scanner):
            return point[0][1]
        return point[1][1]

    def points_for_matching_points(matching_points, scanner_data, scanner):
        return [list(scanner_data[scanner][index_for_point(point, scanner)]) for point in matching_points][:4]

    ins = points_for_matching_points(matching_points, scanner_data, from_scanner)
    out = points_for_matching_points(matching_points, scanner_data, to_scanner)

    # calculations
    l = len(ins)
    B = np.vstack([np.transpose(ins), np.ones(l)])
    D = 1.0 / np.linalg.det(B)
    entry = lambda r, d: np.linalg.det(np.delete(np.vstack([r, B]), (d + 1), axis=0))
    M = [[(-1)**i * D * entry(R, i) for i in range(l)] for R in np.transpose(out)]
    transformation_matrix, translation_vector = np.hsplit(np.array(M), [l - 1])
    translation_vector = np.transpose(translation_vector)[0]
    return transformation_matrix, translation_vector


def transform(transformation_matrix, translation_vector, point):
    return tuple(int(round(x)) for x in np.dot(transformation_matrix, point) + translation_vector)


test_scanner_data = process_lines(test_data)
distance_maps = [distance_map(scanner_data) for scanner_data in test_scanner_data]
matching_points = compare_scanner_distance_data(distance_maps)
transformation_matrix, translation_vector = get_affine_transformations(filter_matching_points(matching_points, 1, 0), 1,
                                                                       0, test_scanner_data)
# In total, each scanner could be in any of 24 different orientations
x = transform(transformation_matrix, translation_vector, [553, 889, -390])
# Wow .. this totally worked
assert x == (-485, -357, 347)


def available_transforms(matching_points):
    mapping = set()
    for point in matching_points:
        mapping.add((point[0][0], point[1][0]))
    return (mapping)


def transform_all_beacons(scanner_data, maching_points, scanner_order):

    mapped_data = [set() for x in range(0, len(scanner_data))]
    for i, untransformed_data in enumerate(scanner_data):
        for point in untransformed_data:
            mapped_data[i].add(point)

    for from_scanner, to_scanner in scanner_order:
        print("transforming %d -> %d" % (from_scanner, to_scanner))
        transformation_matrix, translation_vector = get_affine_transformations(
            filter_matching_points(matching_points, from_scanner, to_scanner), from_scanner, to_scanner, scanner_data)
        transformed_from_data = [transform(transformation_matrix, translation_vector, list(x)) for x in mapped_data[from_scanner]]
        for point in transformed_from_data:
            mapped_data[to_scanner].add(point)

    return mapped_data


def transform_order(available_transforms, target_scanner, scanner_count, ordered_transforms = []):
    """
    Takes the set of overlapping scanners and returns the order of
    transformations to transform everything to scanner zero

    {(0, 1), (2, 4), (1, 3), (1, 4)} -> [(2, 4), (3, 1), (4, 1), (1, 0)]
    """


    if (target_scanner >= scanner_count):
        return list(reversed(ordered_transforms))

    linked_transforms = [(tuple(reversed(transform)) if transform[1] != target_scanner else transform) for transform in [transform for transform in available_transforms if transform[0] == target_scanner or transform[1] == target_scanner] ]

    new_transforms = ordered_transforms + linked_transforms

    return transform_order(available_transforms, target_scanner + 1, scanner_count, new_transforms)


# assert beacons_relative_to_first_scanner == test_expected_beacons_relative_to_first_scanner
scanner_order = transform_order(available_transforms(matching_points), 0, len(test_scanner_data))
# assert scanner_order == [(2, 4), (3, 1), (4, 1), (1, 0)]
x = transform_all_beacons(test_scanner_data, matching_points, scanner_order)

scanner_data = process_lines(real_data)
distance_maps = [distance_map(scanner_data) for scanner_data in scanner_data]
matching_points = compare_scanner_distance_data(distance_maps)
scanner_order = transform_order(available_transforms(matching_points), 0, len(scanner_data))

# These are the available transforms for the live data
# [ (3, 4), (12, 25), (9, 11), (11, 20), (1, 15), (6, 11), (7, 10), (21, 24), (14, 18), (4, 11), (14, 15), (2, 4), (1, 5), (19, 23), (8, 20), (13, 18), (0, 22), (11, 22), (1, 17), (6, 7), (15, 19), (7, 24), (3, 5), (12, 20), (3, 17), (5, 8), (5, 14), (14, 23), (3, 20), (0, 6), (2, 9), (8, 22), (1, 16) ]

x = transform_all_beacons(scanner_data, matching_points, [ (25, 12), (3, 20), (2, 9), (9, 11), (11, 20), (12, 20), (11, 4), (2, 4), (4, 3), (3, 17), (17, 1), (13, 18), (16, 1), (1, 15), (19, 23), (23, 14), (15, 14), (18, 14), (14, 5), (3, 5), (1, 5), (5, 8), (20, 8), (21, 24), (10, 7), (24, 7), (7, 6), (11, 6), (8, 22), (22, 0), (6, 0) ])

# 182 ... too low
# 313 from the handmade transform list

