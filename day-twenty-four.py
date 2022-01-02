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
    "# A comment\n", "inp w\n", "add z w\n", "mod z 2\n", "div w 2\n", "add y w\n", "mod y 2\n", "div w 2\n",
    "add x w\n", "mod x 2\n", "div w 2\n", "mod w 2\n"
]

# To enable as many submarine features as possible, find the largest valid
# fourteen-digit model number that contains no 0 digits.


def parse_line(line):
    return line.strip().split(" ")


def parse_lines(lines):
    return [parse_line(line) for line in lines if line[0] != "#"]


def add(memory, a, b):
    """
    add a b - Add the value of a to the value of b, then store the result in
    variable a.
    """
    memory[a] = memory[a] + (memory[b] if memory.get(b) is not None else int(b))


def mul(memory, a, b):
    """
    mul a b - Multiply the value of a by the value of b, then store the result in
    variable a.
    """
    memory[a] = memory[a] * (memory[b] if memory.get(b) is not None else int(b))


def div(memory, a, b):
    """
    div a b - Divide the value of a by the value of b, truncate the result to an
    integer, then store the result in variable a. (Here, "truncate" means to
    round the value toward zero.)
    """
    memory[a] = math.floor(memory[a] / (memory[b] if memory.get(b) is not None else int(b)))


def mod(memory, a, b):
    """
    mod a b - Divide the value of a by the value of b, then store the remainder
    in variable a. (This is also called the modulo operation.)
    """
    memory[a] = memory[a] % (memory[b] if memory.get(b) is not None else int(b))


def eql(memory, a, b):
    """
    eql a b - If the value of a and b are equal, then store the value 1 in
    variable a. Otherwise, store the value 0 in variable a.
    """
    memory[a] = 1 if memory[a] == (memory[b] if memory.get(b) is not None else int(b)) else 0


def run_program(program, input_data, memory=None):
    if (memory is None):
        memory = {"x": 0, "y": 0, "w": 0, "z": 0}
    instruction_set = {"add": add, "mul": mul, "div": div, "mod": mod, "eql": eql}
    remaining_input = input_data
    for index, line in enumerate(program):
        instruction = line[0]

        if instruction == "inp":
            memory[line[1]] = int(remaining_input[0])
            remaining_input = remaining_input[1:]
            continue

        a, b = line[1:]
        try:
            instruction_set.get(instruction)(memory, a, b)

            if (b == "add_x"):
                print("memory %s" % input_data)
                print(memory)


        except:
            print("Error at line %d" % (index + 1))
            print(memory)
            raise

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

x, y, w, z = run_program(parse_lines(real_data), "12345678901234")

x, y, w, z = run_program(
    parse_lines([
        "inp w\n", "mul x 0\n", "add x z\n", "mod x 26\n", "div z 1\n", "add x 11\n", "eql x w\n", "eql x 0\n",
        "mul y 0\n", "add y 25\n", "mul y x\n", "add y 1\n", "mul z y\n", "mul y 0\n", "add y w\n", "add y 10\n",
        "mul y x\n", "add z y\n"
    ]), "1")

real_data_monad_params = [(1, 12, 4), (1, 11, 10), (1, 14, 12), (26, -6, 14), (1, 15, 6), (1, 12, 16), (26, -9, 1), (1, 14, 7),
                          (1, 14, 8), (26, -5, 11), (26, -9, 8), (26, -5, 3), (26, -2, 1), (26, -7, 8)]

# inp w
# mul x 0
# add x z
# mod x 26
# div z div_z
# add x add_x
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y add_y
# mul y x
# add z y


def monad_digit(div_z, add_x, add_y, memory, digit):

    memory = {**memory, **{"div_z": div_z, "add_x": add_x, "add_y": add_y}}
    x, y, w, z = run_program(
        parse_lines([
            "inp w\n", "mul x 0\n", "add x z\n", "mod x 26\n", "div z div_z\n", "add x add_x\n", "eql x w\n",
            "eql x 0\n", "mul y 0\n", "add y 25\n", "mul y x\n", "add y 1\n", "mul z y\n", "mul y 0\n", "add y w\n",
            "add y add_y\n", "mul y x\n", "add z y\n"
        ]), str(digit), memory)
    return {"x": x, "y": y, "w": w, "z": z}


def monad(input):

    memory = {"x": 0, "y": 0, "w": 0, "z": 0}
    for index, params in enumerate(real_data_monad_params):
        div_z, add_x, add_y = params
        print(params)
        memory = monad_digit(div_z, add_x, add_y, memory, input[index:])
        print(memory)

    return (memory.get('x'), memory.get('y'), memory.get('w'), memory.get('z'))

# Zero in the z variable means a valid number

assert run_program(parse_lines(real_data), "12345678901234") == monad("12345678901234")

# real_data_monad_params = [(1, 12, 4), (1, 11, 10), (1, 14, 12), (26, -6, 14), (1, 15, 6), (1, 12, 16), (26, -9, 1), (1, 14, 7),
#                           (1, 14, 8), (26, -5, 11), (26, -9, 8), (26, -5, 3), (26, -2, 1), (26, -7, 8)]
# div_z, add_x, add_y
#
# x gets the previous z
# x = (x % 26) + add_x (-7)
# z = z / div_z (26)
#
# if x == input:
#   x = 0
# else:
#   x = 1
#
# y = 25
#
# y = 1 or 26 (if x == input)
# z = z * y
# y = input + add_y
# y = 0 or input + add_y (8) (if x == input)
#
# So by digit 14 we want z to be zero and y to be zero
# z = z + y


