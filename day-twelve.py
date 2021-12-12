import functools
from enum import Enum
from itertools import groupby

def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, list) and (len(x) == 0 or isinstance(x[0], list)):
            yield from flatten(x)
        else:
            yield x


test_data_one = ["start-A", "start-b", "A-c", "A-b", "b-d", "A-end", "b-end"]

expected_paths_one = [
    "start,A,b,A,c,A,end", "start,A,b,A,end", "start,A,b,end", "start,A,c,A,b,A,end", "start,A,c,A,b,end",
    "start,A,c,A,end", "start,A,end", "start,b,A,c,A,end", "start,b,A,end", "start,b,end"
]

test_data_two = ["dc-end", "HN-start", "start-kj", "dc-start", "dc-HN", "LN-dc", "HN-end", "kj-sa", "kj-HN", "kj-dc"]

expected_paths_two = [
    "start,HN,dc,HN,end", "start,HN,dc,HN,kj,HN,end", "start,HN,dc,end", "start,HN,dc,kj,HN,end", "start,HN,end",
    "start,HN,kj,HN,dc,HN,end", "start,HN,kj,HN,dc,end", "start,HN,kj,HN,end", "start,HN,kj,dc,HN,end",
    "start,HN,kj,dc,end", "start,dc,HN,end", "start,dc,HN,kj,HN,end", "start,dc,end", "start,dc,kj,HN,end",
    "start,kj,HN,dc,HN,end", "start,kj,HN,dc,end", "start,kj,HN,end", "start,kj,dc,HN,end", "start,kj,dc,end"
]

test_data_three = [
    "fs-end", "he-DX", "fs-he", "start-DX", "pj-DX", "end-zg", "zg-sl", "zg-pj", "pj-he", "RW-he", "fs-DX", "pj-RW",
    "zg-RW", "start-pj", "he-WI", "zg-he", "pj-fs", "start-RW"
]

expected_paths_three_count = 226

real_data = [
    "dr-of", "start-KT", "yj-sk", "start-gb", "of-start", "IJ-end", "VT-sk", "end-sk", "VT-km", "KT-end", "IJ-of",
    "dr-IJ", "yj-IJ", "KT-yj", "gb-VT", "dr-yj", "VT-of", "PZ-dr", "KT-of", "KT-gb", "of-gb", "dr-sk", "dr-VT"
]

# Graph structure
{"name": {"large": False, "connections": ["name", "name"]}}

# Part One - How many paths through this cave system are there that visit small caves at most once?


def is_small(cave_name):
    return cave_name[0].islower() and cave_name not in ['start', 'end']


def process_data(data):
    graph = {}
    for source, dest in [x.split("-") for x in data]:
        if (dest != "start" and source != 'end'):
            graph.setdefault(source, []).append(dest)
        if (source != "start" and dest != 'end'):
            graph.setdefault(dest, []).append(source)
    return {k: {"connections": v } for k, v in graph.items()}


def filter_connections_part_one(current_path, source_cave_name, destination_cave_name):
    """
    If the current path already contains a particular small cave (from any
    cave), then we don't want to include that small cave.
    """
    if (is_small(destination_cave_name)):
        return destination_cave_name not in current_path

    return True

def can_repeat(current_path, cave_name):
    filtered = list(filter(is_small, current_path))
    grouped_data = {k: filtered.count(k) for k, g in groupby(filtered)}
    return all(v < 2 for v in grouped_data.values())

def filter_connections_part_two(current_path, source_cave_name, destination_cave_name):
    """
    Specifically, big caves can be visited any number of times, a single small
    cave can be visited at most twice, and the remaining small caves can be
    visited at most once.
    """
    if (is_small(destination_cave_name)):
        if (can_repeat(current_path, destination_cave_name)):
            return True

        return destination_cave_name not in current_path

    return True


def explore_cave(caves, cave_name, filter_fn, current_path=[], loop_dictionary={}):

    if (cave_name == "end"):
        return current_path

    cave = caves.get(cave_name)
    assert cave is not None, "Cave Name was %s" % cave_name

    # If our data contains large caves that link to large caves and therefore
    # can loop we catch it here. If so we would need to update our filter
    # connections fn to handle that case.
    if (len(current_path) > 100):
        print(current_path)
        assert False

    return list(flatten([
        explore_cave(caves, connection_cave_name, filter_fn, current_path + [connection_cave_name], {})
        for connection_cave_name in filter(lambda destination_cave_name: filter_fn(current_path, cave_name, destination_cave_name), cave.get("connections"))
    ]))


paths_test_data_one = explore_cave(process_data(test_data_one), "start", filter_connections_part_one, ["start"])
assert len(paths_test_data_one) == len(expected_paths_one)
print(process_data(test_data_two))
paths_test_data_two = explore_cave(process_data(test_data_two), "start", filter_connections_part_one, ["start"])
assert len(paths_test_data_two) == len(expected_paths_two)
paths_test_data_three = explore_cave(process_data(test_data_three), "start", filter_connections_part_one, ["start"])
assert len(paths_test_data_three) == expected_paths_three_count
print(len(explore_cave(process_data(real_data), "start", filter_connections_part_one, ["start"])))
# Part two .. new relaxed filter function

part_two_expected_one = 36
part_two_expected_two = 103
part_two_expected_three = 3509

paths_test_data_one = explore_cave(process_data(test_data_one), "start", filter_connections_part_two, ["start"])
assert len(paths_test_data_one) == part_two_expected_one
paths_test_data_two = explore_cave(process_data(test_data_two), "start", filter_connections_part_two, ["start"])
assert len(paths_test_data_two) == part_two_expected_two
print(len(explore_cave(process_data(real_data), "start", filter_connections_part_two, ["start"])))
