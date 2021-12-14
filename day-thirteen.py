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



def process_lines(lines):
    # have to account for the end of line in this data
    width = len(lines[0]) - 1
    height = len(lines)
    heightmap = list(flatten([[int(c) for c in line if c != '\n'] for line in lines]))
    return (heightmap, width, height)

test_data = [
    "6,10\n",
    "0,14\n",
    "9,10\n",
    "0,3\n",
    "10,4\n",
    "4,11\n",
    "6,0\n",
    "6,12\n",
    "4,1\n",
    "0,13\n",
    "10,12\n",
    "3,4\n",
    "3,0\n",
    "8,4\n",
    "1,10\n",
    "2,14\n",
    "8,10\n",
    "9,0\n",
    "\n",
    "fold along y=7\n",
    "fold along x=5\n"
]

f = open('day-thirteen-input.txt')
real_data = f.readlines()
f.close()

def create_dotmap(width, height):
    return [[None for x in range(0, width)] for y in range(0, height)]

def process_lines(data):

    fold_data = [(fold_type, int(value)) for fold_type, value in [tuple(line.strip().split(" ")[2].split("=")) for line in data if "fold" in line]]
    dot_data = [line.strip() for line in data if line != "\n" and "fold" not in line]
    dot_data = [(int(x),int(y)) for x,y in [tuple(line.split(",")) for line in dot_data] ]
    x_values = [x for x,y in dot_data]
    y_values = [y for x,y in dot_data]

    def get_first_fold(fold_data, fold_type):
        return list(filter(lambda x: x[0]==fold_type, fold_data))[0]

    first_x_fold = get_first_fold(fold_data, 'x')[1]
    first_y_fold = get_first_fold(fold_data, 'y')[1]

    # Asserting some of my assumptions about how this works
    width = max(x_values) + 1
    height = max(y_values) + 1
    assert max(x_values) == first_x_fold * 2, "First x fold %d, max x value %d" % (first_x_fold, max(x_values))
    assert max(y_values) == first_y_fold * 2

    dotmap = create_dotmap(width, height)
    for x,y in dot_data:
        dotmap[y][x] = '#'

    return fold_data, dotmap, width, height

def visible_dots(dotmap):
    return len(list(filter(lambda pixel: pixel == '#', flatten(dotmap))))


def fold_dimensions(width, height, fold_instruction):
    fold_type, value = fold_instruction
    width_modifier, width_offset = ( 2, 1 ) if fold_type == 'x' else ( 1, 0 )
    height_modifier, height_offset = ( 2, 1 ) if fold_type == 'y' else ( 1, 0 )
    return int((width - width_offset) / width_modifier), int((height - height_offset) / height_modifier)


def fold(dotmap, width, height, fold_instruction):
    fold_type, value = fold_instruction
    new_width, new_height = fold_dimensions(width, height, fold_instruction)
    new_dotmap = create_dotmap(new_width, new_height)
    flipped_dotmap = [list(reversed(line)) for line in dotmap] if fold_type == 'x' else list(reversed(dotmap))
    # then just merge the dotmap and the flipped dotmap in the dimensions of the new page
    for y in range(0, new_height):
        for x in range(0, new_width):
            new_dotmap[y][x] = dotmap[y][x] or flipped_dotmap[y][x]
    return new_dotmap, new_width, new_height

def show_dotmap(dotmap, width, height):
    for row in dotmap:
        for x in range(0, width):
            print("%s" %  row[x] if row[x] is not None else ".", end="")
        print("")
    for x in range(0, width):
        print("-", end="")
    print("")

fold_data, dotmap, width, height = process_lines(test_data)
show_dotmap(dotmap, width, height)
folded_dotmap, width, height = fold(dotmap, width, height, fold_data[0])
show_dotmap(folded_dotmap, width, height)
expected_visible_dots_after_first_fold = 17
test_data_visible_dots_after_first_fold = visible_dots(folded_dotmap)
assert test_data_visible_dots_after_first_fold == expected_visible_dots_after_first_fold, "Visible dots %d" % test_data_visible_dots_after_first_fold

# Now for the real data
fold_data, dotmap, width, height = process_lines(real_data)
folded_dotmap, width, height = fold(dotmap, width, height, fold_data[0])
print(visible_dots(folded_dotmap))

# Part two
fold_data, folded_dotmap, width, height = process_lines(real_data)
for fold_instruction in fold_data:
    folded_dotmap, width, height = fold(folded_dotmap, width, height, fold_instruction)
show_dotmap(folded_dotmap, width, height)

