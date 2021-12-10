import functools
import pygame
from enum import Enum

test_data = [
    "[({(<(())[]>[[{[]{<()<>>\n",
    "[(()[<>])]({[<{<<[]>>(\n",
    "{([(<{}[<>[]}>{[]{[(<()>\n",
    "(((({<>}<{<{<>}{[]{[]{}\n",
    "[[<[([]))<([[{}[[()]]]\n",
    "[{[{({}]{}}([{[{{{}}([]\n",
    "{<[[]]>}<{[{[{[]{()[[[]\n",
    "[<(<(<(<{}))><([]([]()\n",
    "<{([([[(<>()){}]>(<<{{\n",
    "<{([{{}}[<[[[<>{}]]]>[]]\n",
]

expected_illegal_characters = ['}', ')', ']', ')', '>']
expected_syntax_checker_score = 26397
expected_middle_autocomplete_score = 288957

expected_autocomplete_dictionary = {
    '}}]])})]': 288957,
    ')}>]})': 5566,
    '}}>}>))))': 1480781,
    ']]}}]}]}>': 995444,
    '])}>': 294
}


def calculate_syntax_checker_score(characters):
    score_lookup = {')': 3, ']': 57, '}': 1197, '>': 25137}
    return sum([score_lookup.get(character) for character in characters])


def calculate_autocomplete_score(characters):
    score_lookup = {')': 1, ']': 2, '}': 3, '>': 4}
    return sum([score_lookup.get(character) for character in characters])


def process_lines(lines):
    return [line.strip() for line in lines]


def is_closing(character):
    return character in '}>)]'


def is_pair(character, test_character):
    return {'(': ')', '[': ']', '{': '}', '<': '>'}.get(character) == test_character


def syntax_check_line(line):
    character_stack = []
    for character in line:
        if not is_closing(character):
            character_stack.append(character)
        else:
            opening_character = character_stack.pop()
            if not is_pair(opening_character, character):
                return character

    return character_stack


def syntax_check(data):
    return list(filter(lambda char: type(char) is not list, [syntax_check_line(line) for line in data]))

def autocomplete_check(data):
    return list(filter(lambda char: type(char) is list, [syntax_check_line(line) for line in data]))

f = open('day-ten-input.txt')
real_data = f.readlines()
f.close()

# Part One
test_calculate_syntax_checker_score = calculate_syntax_checker_score(expected_illegal_characters)
assert test_calculate_syntax_checker_score == expected_syntax_checker_score
illegal_characters = syntax_check(process_lines(test_data))
assert expected_illegal_characters == illegal_characters, "%s" % str(illegal_characters)
# print(calculate_syntax_checker_score(syntax_check(process_lines(real_data))))
autocomplete_lines = ["".join(x) for x in autocomplete_check(process_lines(test_data)) ]
print(autocomplete_lines)
