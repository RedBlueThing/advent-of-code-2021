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

def source_pair_to_matching_pair(source_pair):
    return source_pair[0] + '0' + source_pair[1]

def source_pair_to_replace_pair(source_pair, insert):
    return source_pair[0] + insert+ source_pair[1]


def process_insertion_rules_version_one(lines):
    return {source_pair_to_matching_pair(source_pair): source_pair_to_replace_pair(source_pair, insert) for source_pair, insert in [tuple(line.strip().split(" -> ")) for line in lines]}


test_data = [
    "NNCB\n", "\n", "CH -> B\n", "HH -> N\n", "CB -> H\n", "NH -> C\n", "HB -> C\n", "HC -> B\n", "HN -> C\n",
    "NN -> C\n", "BH -> H\n", "NC -> B\n", "NB -> B\n", "BN -> B\n", "BB -> N\n", "BC -> B\n", "CC -> N\n", "CN -> C\n"
]

expected_polymers = [
    "NNCB", "NCNBCHB", "NBCCNBBBCBHCB", "NBBBCNCCNBBNBNBBCHBHHBCHB", "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"
]

# taking the quantity of the most common element (B, 1749) and subtracting the
# quantity of the least common element (H, 161) produces 1749 - 161 = 1588.
part_one_steps = 10
part_one_expected_most_common_minus_least_common = 1588
part_two_steps = 40
part_two_expected_most_common_minus_least_common = 2188189693529

def apply_rules_version_one(polymer, insertion_rules, remaining_steps):
    if (remaining_steps == 0):
        return polymer

    # spread out our polymer
    spread_polymer = "".join(flatten([[c, '0'] for c in polymer]))

    for key,value in insertion_rules.items():
        while (spread_polymer.find(key) >= 0):
            spread_polymer = spread_polymer.replace(key, value)


    return apply_rules_version_one("".join(list(filter(lambda a: a != '0', spread_polymer))), insertion_rules, remaining_steps - 1)

def quantity_answer(polymer):
    grouped_element_counts = {k: len(list(g)) for k, g in groupby(sorted(polymer))}
    counts = sorted([value for value in grouped_element_counts.values()])
    return counts[-1] - counts[0]


f = open('day-fourteen-input.txt')
real_data = f.readlines()
f.close()

starting_polymer = test_data[0].strip()
insertion_rules = process_insertion_rules_version_one(test_data[2:])
print(starting_polymer)

for i, polymer in enumerate(expected_polymers):
    assert polymer == apply_rules_version_one(starting_polymer, insertion_rules, i), "for %d" % i

assert part_one_expected_most_common_minus_least_common == quantity_answer(apply_rules_version_one(starting_polymer, insertion_rules, part_one_steps))

def count_pairs(polymer):
    return { first + second: 1 for first, second in zip(polymer, polymer[1:]) }

def count_characters(polymer):
    return {k: len(list(g)) for k, g in groupby(sorted(polymer))}

def process_insertion_rules_version_two(lines):
    return {source_pair: insert for source_pair, insert in [tuple(line.strip().split(" -> ")) for line in lines]}

def apply_rules_version_two(pair_count, character_count, insertion_rules, remaining_steps):

    print(pair_count)
    print(character_count)

    if (remaining_steps == 0):
        return pair_count, character_count

    new_pair_counts = {}
    reset_pair_counts = {}

    # update the pair count for the insertion rules
    for key,value in insertion_rules.items():
        matching_pairs = pair_count.get(key)
        if (matching_pairs):
            character_count[value] = (character_count.get(value) or 0) + matching_pairs
            new_pair_counts[key[0] + value] = (new_pair_counts.get(key[0] + value) or 0) + matching_pairs
            new_pair_counts[value + key[1]] = (new_pair_counts.get(value + key[1]) or 0) + matching_pairs
            reset_pair_counts[key] = 0

    def merge_pair_counts(current, new):
        for key, value in new.items():
            current[key] = (current.get(key) or 0) + value
        return current

    updated_pair_counts = merge_pair_counts({**pair_count,**reset_pair_counts},new_pair_counts)

    return apply_rules_version_two(updated_pair_counts, character_count, insertion_rules, remaining_steps - 1)

starting_polymer = test_data[0].strip()
insertion_rules = process_insertion_rules_version_two(test_data[2:])

def quantity_answer_version_two(pair_count, character_counts):
    counts = sorted([value for value in character_counts.values()])
    return counts[-1] - counts[0]

# print(quantity_answer_version_two(*apply_rules_version_two(count_pairs(starting_polymer), count_characters(starting_polymer), insertion_rules, 2)))
# assert part_one_expected_most_common_minus_least_common == quantity_answer_version_two(*apply_rules_version_two(count_pairs (starting_polymer), count_characters(starting_polymer), insertion_rules, part_one_steps))

starting_polymer = real_data[0].strip()
print(starting_polymer)
insertion_rules = process_insertion_rules_version_two(real_data[2:])
print (quantity_answer_version_two(*apply_rules_version_two(count_pairs (starting_polymer), count_characters(starting_polymer), insertion_rules, part_two_steps)))
