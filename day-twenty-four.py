import functools
import math
from enum import Enum

f = open('day-twenty-four-input.txt')
real_data = [line.strip() for line in f.readlines()]
f.close()

# For example, here is an ALU program which takes an input number, negates it,
# and stores it in x:
test_data_one = ["inp x\n", "mul x -1\n"]

# Here is an ALU program which takes two input numbers, then sets z to 1 if the
# second input number is three times larger than the first input number, or sets
# z to 0 otherwise:
test_data_two = ["inp z\n", "inp x\n", "mul z 3\n", "eql z x\n"]

# Here is an ALU program which takes a non-negative integer as input, converts it
# into binary, and stores the lowest (1's) bit in z, the second-lowest (2's) bit
# in y, the third-lowest (4's) bit in x, and the fourth-lowest (8's) bit in w:
test_data_three = [
    "inp w\n", "add z w\n", "mod z 2\n", "div w 2\n", "add y w\n", "mod y 2\n", "div w 2\n", "add x w\n", "mod x 2\n",
    "div w 2\n", "mod w 2\n"
]

# To enable as many submarine features as possible, find the largest valid
# fourteen-digit model number that contains no 0 digits.

part_one_highest = 99999999999999


def parse_line(line):
    return line.strip().split(" ")


def parse_lines(lines):
    return [parse_line(line) for line in lines]


def add(line, memory, a, b):
    """
    add a b - Add the value of a to the value of b, then store the result in
    variable a.
    """
    memory[a] = memory[a] + (memory[b] if memory.get(b) else int(b))


def mul(line, memory, a, b):
    """
    mul a b - Multiply the value of a by the value of b, then store the result in
    variable a.
    """
    memory[a] = memory[a] * (memory[b] if memory.get(b) else int(b))


def div(line, memory, a, b):
    """
    div a b - Divide the value of a by the value of b, truncate the result to an
    integer, then store the result in variable a. (Here, "truncate" means to
    round the value toward zero.)
    """
    memory[a] = math.floor(memory[a] / (memory[b] if memory.get(b) else int(b)))


def mod(line, memory, a, b):
    """
    mod a b - Divide the value of a by the value of b, then store the remainder
    in variable a. (This is also called the modulo operation.)
    """
    memory[a] = memory[a] % (memory[b] if memory.get(b) else int(b))


def eql(line, memory, a, b):
    """
    eql a b - If the value of a and b are equal, then store the value 1 in
    variable a. Otherwise, store the value 0 in variable a.
    """
    memory[a] = 1 if memory[a] == (memory[b] if memory.get(b) else int(b)) else 0


def run_program(program, input_data):
    memory = {"x": 0, "y": 0, "w": 0, "z": 0}
    instruction_set = {"add": add, "mul": mul, "div": div, "mod": mod, "eql": eql}
    remaining_input = input_data
    for line in program:
        instruction = line[0]

        if instruction == "inp":
            memory[line[1]] = int(remaining_input[0])
            remaining_input = remaining_input[1:]
            continue

        a, b = line[1:]
        instruction_set.get(instruction)(line, memory, a, b)
        # print(line)
        # print(memory)

    return (memory.get('x'), memory.get('y'), memory.get('w'), memory.get('z'))


x, y, w, z = run_program(parse_lines(test_data_one), "1")
assert x == -1
x, y, w, z = run_program(parse_lines(test_data_two), "13")
assert z == 1
x, y, w, z = run_program(parse_lines(test_data_two), "14")
assert z == 0
x, y, w, z = run_program(parse_lines(test_data_three), "9")
assert w == 1
assert x == 0
assert y == 0
assert z == 1
