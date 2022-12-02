def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, list) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x

f = open('day-twenty-five-input.txt')
real_data = f.readlines()
f.close()

test_data = [
"v...>>.vv>\n",
".vv>>.vv..\n",
">>.>v>...v\n",
">>v>>.>.v.\n",
"v>v.vv.v..\n",
">.>>..v...\n",
".vv..>.>v.\n",
"v.v..>>v.v\n",
"....v..v.>\n"
]

def process_lines(lines):
    # have to account for the end of line in this data
    width = len(lines[0]) - 1
    height = len(lines)
    seafloor = list(flatten([[c for c in line if c != '\n'] for line in lines]))
    return (seafloor, width, height)

def in_range(seafloor, cell_index):
    return cell_index >= 0 and cell_index < len(seafloor)

def is_last_cell_in_row(width, cell_index):
    return (cell_index + 1) % width == 0

def south(seafloor, width, height, cell_index):
    offset_index = cell_index + width
    return offset_index if in_range(seafloor, offset_index) else offset_index - len(seafloor)

def east(seafloor, width, height, cell_index):
    return cell_index + 1 if not is_last_cell_in_row(width, cell_index) else (cell_index - (width - 1))

south_east_test_data = [
"...\n",
"...\n",
"...\n"
]
seafloor, width, height = process_lines(south_east_test_data)
assert east(seafloor, width, height, 2) == 0
assert east(seafloor, width, height, 8) == 6
assert east(seafloor, width, height, 0) == 1
assert south(seafloor, width, height, 0) == 3
assert south(seafloor, width, height, 6) == 0
assert south(seafloor, width, height, 7) == 1
assert south(seafloor, width, height, 8) == 2

# Part One
seafloor, width, height = process_lines(test_data)

def get_herd(ch, seafloor, width, height):
    return [i for i,v in enumerate(seafloor) if v == ch]

def show_seafloor(seafloor, width, height):
    for y in range(0, height):
        for x in range(0, width):
            index = (width * y) + x
            print("%c " % (seafloor[index]), end="")
        print("")

def can_move(seafloor, width, height, direction_fn, cell_index):
    new_cell_index = direction_fn(seafloor, width, height, cell_index)
    return (seafloor[new_cell_index] == '.', cell_index, new_cell_index)

def move_herd (seafloor, width, height, herd, fn):
    moves = [(cell_index, new_cell_index) for can_move, cell_index, new_cell_index in map(lambda cell_index: can_move(seafloor, width, height, fn, cell_index), herd) if can_move]
    for cell_index, new_cell_index in moves:
        seafloor[new_cell_index] = seafloor[cell_index]
        seafloor[cell_index] = '.'
    return len(moves)

def simulate_step(seafloor, width, height):

    east_herd = get_herd('>', seafloor, width, height)
    south_herd = get_herd('v', seafloor, width, height)
    east_move_count = move_herd(seafloor, width, height, east_herd, east)
    south_move_count = move_herd(seafloor, width, height, south_herd, south)
    return east_move_count + south_move_count

def steps_while_moving(seafloor, width, height):

    steps = 0
    while (steps < 1000):
        moves = simulate_step(seafloor, width, height)
        steps += 1
        if (moves == 0):
            return steps

    assert False


