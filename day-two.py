import functools


def split_command(command):
    instruction, value = command.split(" ")
    return (instruction, int(value))


def apply_command_version_one(command, current_horizontal, current_depth):

    instruction, value = split_command(command)
    if (instruction == "forward"):
        current_horizontal += value
    if (instruction == "up"):
        current_depth -= value
    if (instruction == "down"):
        current_depth += value

    return (current_horizontal, current_depth)


def apply_command_version_two(command, current_horizontal, current_depth, current_aim):

    instruction, value = split_command(command)
    if (instruction == "forward"):
        current_horizontal += value
        current_depth += (current_aim * value)
    if (instruction == "up"):
        current_aim -= value
    if (instruction == "down"):
        current_aim += value

    return (current_horizontal, current_depth, current_aim)


# forward 5
# down 5
# forward 8
# up 3
# down 8
# forward 2


def process_version(apply_command_fn, init):

    f = open('day-two-input.txt')
    results = functools.reduce(lambda current_value, next_value: apply_command_fn(*((next_value, ) + current_value)),
                               f.readlines(), init)
    f.close()
    print("%s Results %s" % (str(apply_command_fn), str(results)))
    print("Value %d" % (results[0] * results[1]))


process_version(apply_command_version_one, (0, 0))
process_version(apply_command_version_two, (0, 0, 0))
