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
    "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe\n",
    "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc\n",
    "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg\n",
    "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb\n",
    "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea\n",
    "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb\n",
    "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe\n",
    "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef\n",
    "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb\n",
    "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce\n",
]

expected_digits_with_unique_number_of_segments = 26
expected_sum_of_decoded_digits = 61229

f = open('day-eight-input.txt')
real_data = f.readlines()
f.close()

segments_for_digits = {0: 6, 1: 2, 2: 5, 3: 5, 4: 4, 5: 5, 6: 6, 7: 3, 8: 7, 9: 6}

digits_for_segments = {
    segments: [digit for digit in segments_for_digits.keys() if segments_for_digits.get(digit) == segments]
    for segments in segments_for_digits.values()
}

unique_segment_digits = [v[0] for k, v in digits_for_segments.items() if len(v) == 1]
segments_for_unique_segment_digits = [k for k, v in digits_for_segments.items() if len(v) == 1]


def process_data(data):

    return [{
        "signals": signals.strip().split(" "),
        "four_digit_output": output.strip().split(" ")
    } for signals, output in [x.strip().split("|") for x in data]]


def is_unique(signal):
    return len(signal) in segments_for_unique_segment_digits


def count_digits_with_unique_segments(data):
    all_output = flatten([entry['four_digit_output'] for entry in data])
    return len([x for x in flatten([entry['four_digit_output'] for entry in data]) if is_unique(x)])


class DigitPositions(Enum):
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"
    TOP_RIGHT = "top_right"
    TOP_LEFT = "top_left"
    BOTTOM_RIGHT = "top_right"
    BOTTOM_LEFT = "top_left"


def key_for_positions(positions):
    return "-".join(sorted([position.value for position in positions]))


# Didn't end up needing this thing
positions_for_digit = {
    0: [
        DigitPositions.TOP, DigitPositions.BOTTOM, DigitPositions.TOP_RIGHT, DigitPositions.TOP_LEFT,
        DigitPositions.BOTTOM_LEFT, DigitPositions.BOTTOM_RIGHT
    ],
    1: [DigitPositions.TOP_RIGHT, DigitPositions.BOTTOM_RIGHT],
    2: [
        DigitPositions.TOP, DigitPositions.BOTTOM, DigitPositions.MIDDLE, DigitPositions.TOP_RIGHT,
        DigitPositions.BOTTOM_LEFT
    ],
    3: [
        DigitPositions.TOP, DigitPositions.BOTTOM, DigitPositions.MIDDLE, DigitPositions.TOP_RIGHT,
        DigitPositions.BOTTOM_RIGHT
    ],
    4: [DigitPositions.MIDDLE, DigitPositions.TOP_RIGHT, DigitPositions.TOP_LEFT, DigitPositions.BOTTOM_RIGHT],
    5: [
        DigitPositions.TOP, DigitPositions.MIDDLE, DigitPositions.BOTTOM, DigitPositions.TOP_LEFT,
        DigitPositions.BOTTOM_RIGHT
    ],
    6: [
        DigitPositions.TOP, DigitPositions.MIDDLE, DigitPositions.BOTTOM, DigitPositions.TOP_LEFT,
        DigitPositions.BOTTOM_RIGHT, DigitPositions.BOTTOM_LEFT
    ],
    7: [DigitPositions.TOP, DigitPositions.BOTTOM_RIGHT, DigitPositions.TOP_RIGHT],
    8: [
        DigitPositions.TOP, DigitPositions.MIDDLE, DigitPositions.BOTTOM, DigitPositions.TOP_RIGHT,
        DigitPositions.TOP_LEFT, DigitPositions.BOTTOM_LEFT, DigitPositions.BOTTOM_RIGHT
    ],
    9: [
        DigitPositions.TOP, DigitPositions.MIDDLE, DigitPositions.BOTTOM, DigitPositions.TOP_RIGHT,
        DigitPositions.TOP_LEFT, DigitPositions.BOTTOM_RIGHT
    ]
}

digit_for_positions = {key_for_positions(v): k for k, v in positions_for_digit.items()}


def digit_for_known_signal(signal):
    return digits_for_segments.get(len(signal))[0]


def key_for_signal(signal):
    return "".join(sorted(signal))


def digit_for_signal(signal, positions_for_signals):
    return digit_for_positions.get(key_for_positions(positions_for_signals.get(key_for_signal(signal))))


def signal_to_set(signal):
    return {c for c in signal}


def digits_for_known_and_unknown_signals(known_signals, unknown_signals):

    # signal_character_For_middle_position
    one, seven, four, eight = sorted(known_signals, key=lambda signal: len(signal))

    signal_character_for_top = signal_to_set(seven).difference(signal_to_set(one)).pop()
    sorted_unknown_signals = sorted(unknown_signals, key=lambda signal: len(signal))
    two_three_five = sorted_unknown_signals[:3]
    three = list(filter(lambda signal: all([signal_character in signal for signal_character in one]),
                        two_three_five))[0]
    two_five = list(filter(lambda signal: signal != three, two_three_five))
    signal_character_set_for_top_middle_and_bottom = signal_to_set(two_five[0]).intersection(two_five[1])
    signal_character_set_for_middle_and_bottom = signal_character_set_for_top_middle_and_bottom
    signal_character_set_for_middle_and_bottom.remove(signal_character_for_top)
    zero_six_nine = sorted_unknown_signals[3:]
    zero = list(
        filter(lambda signal: len(signal_to_set(signal).intersection(signal_character_set_for_middle_and_bottom)) == 1,
               zero_six_nine))[0]
    six_nine = list(filter(lambda signal: signal != zero, zero_six_nine))
    # six shares one character with 7, but nine shares two
    six = list(filter(lambda signal: len(signal_to_set(signal).intersection(signal_to_set(seven))) == 2, six_nine))[0]
    nine = list(filter(lambda signal: signal != six, six_nine))[0]
    five = list(filter(lambda signal: len(signal_to_set(signal).intersection(signal_to_set(nine))) == 5, two_five))[0]
    two = list(filter(lambda signal: signal != five, two_five))[0]

    return {
        **{
            zero: 0,
            two: 2,
            three: 3,
            five: 5,
            six: 6,
            nine: 9
        },
        **{signal: digit_for_known_signal(signal)
           for signal in known_signals}
    }


def order_signals(signals):
    return ["".join(sorted(signal)) for signal in signals]


def decode_entry(entry):

    unknown_signals = order_signals(filter(lambda signal: not is_unique(signal), entry['signals']))
    known_signals = order_signals(filter(is_unique, entry['signals']))
    digits_for_signals = digits_for_known_and_unknown_signals(known_signals, unknown_signals)
    four_digits = int("".join(
        [str(x) for x in [digits_for_signals.get(signal) for signal in order_signals(entry['four_digit_output'])]]))
    print("%s %d" % (order_signals(entry['four_digit_output']), four_digits))
    return four_digits


def decode_data(data):
    return sum([decode_entry(entry) for entry in data])


# Part One
print(str(count_digits_with_unique_segments(process_data(test_data)) == expected_digits_with_unique_number_of_segments))
print(count_digits_with_unique_segments(process_data(real_data)))

# Part Two
print(str(decode_data(process_data(test_data)) == expected_sum_of_decoded_digits))
print(decode_data(process_data(real_data)))
