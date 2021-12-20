import functools
import math
from enum import Enum
import numpy as np
import pygame


def image_pixel_index(x, y, image_width, image_height):
    return (image_width * y) + x

def render_image(image, image_width, image_height):
    pygame.init()
    screen = pygame.display.set_mode((image_width, image_height))
    screenrect = screen.get_rect()
    background = pygame.Surface(screen.get_size())  #create surface for background
    background.fill((255, 255, 255))  #fill the background white (red,green,blue)
    clock = pygame.time.Clock()  #create pygame clock object
    mainloop = True
    FPS = 60  # desired max. framerate in frames per second.

    while mainloop:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0  # seconds passed since last frame (float)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False  # pygame window closed by user
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False  # user pressed ESC

        background.fill((0, 0, 0))

        for y in range(0, image_height):
            for x in range(0, image_width):
                index = image_pixel_index(x, y, image_width, image_height)
                pixel = 255 if image[index] == "#" else 0
                background.set_at((x, y), (pixel,pixel,pixel))

        screen.blit(background, (0, 0))  #draw background on screen (overwriting all)

        pygame.display.flip()  # flip the screen 30 times a second

# f = open('day-nineteen-input.txt')
f = open('day-twenty-input.txt')
real_data = [line.strip() for line in f.readlines()]
f.close()


def process_data(raw_data):
    width = len(raw_data[0])
    height = len(raw_data)
    imagemap = "".join(raw_data)
    return (imagemap, width, height)


def process_lines(lines):

    current_index = 0

    image = []

    for i, line in enumerate(lines):
        if (i == 0):
            algorithm = line.strip()
            continue

        if (line.strip()):
            image.append(line.strip())

    return algorithm, image


test_data = [
    "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#\n",
    "\n", "#..#.\n", "#....\n", "##..#\n", "..#..\n", "..###\n"
]


def show_imagemap(imagemap, width, height):
    for y in range(0, height):
        for x in range(0, width):
            index = (width * y) + x
            print("%s" % (imagemap[index]), end="")
        print("")


def expand_imagemap(imagemap, width, height, padding):
    def populate_padding(count):
        global infinite_pixel
        return "".join([("#" if infinite_pixel else ".") for x in range(0, count)])

    new_blank_row = populate_padding(width + (padding * 2))
    rows = [new_blank_row for i in range(0,padding)]
    for y in range(0, height):
        end_padding = populate_padding(padding)
        current_row = end_padding
        for x in range(0, width):
            index = (width * y) + x
            current_row += imagemap[index]
        current_row += end_padding
        rows.append(current_row)
    rows += [new_blank_row for i in range(0,padding)]

    # Then turn the data back into an imagemap
    return process_data(rows)


def in_range(imagemap, pixel_index):
    return pixel_index >= 0 and pixel_index < len(imagemap)


def is_first_cell_in_row(width, pixel_index):
    return pixel_index % width == 0


def top(imagemap, width, height, pixel_index):
    offset_index = pixel_index - width
    return offset_index if in_range(imagemap, offset_index) else None


def bottom(imagemap, width, height, pixel_index):
    offset_index = pixel_index + width
    return offset_index if in_range(imagemap, offset_index) else None


def left(imagemap, width, height, pixel_index):
    if pixel_index is None:
        return None
    offset_index = pixel_index - 1 if not is_first_cell_in_row(width, pixel_index) else -1
    return offset_index if in_range(imagemap, offset_index) else None


def right(imagemap, width, height, pixel_index):
    if pixel_index is None:
        return None
    offset_index = pixel_index + 1 if not is_first_cell_in_row(width, pixel_index + 1) else -1
    return offset_index if in_range(imagemap, offset_index) else None


def adjacent_cell_indicies(imagemap, width, height, pixel_index):
    return [
            left(imagemap, width, height, top(imagemap, width, height, pixel_index)),
            top(imagemap, width, height, pixel_index),
            right(imagemap, width, height, top(imagemap, width, height, pixel_index)),
            left(imagemap, width, height, pixel_index),
            pixel_index,
            right(imagemap, width, height, pixel_index),
            left(imagemap, width, height, bottom(imagemap, width, height, pixel_index)),
            bottom(imagemap, width, height, pixel_index),
            right(imagemap, width, height, bottom(imagemap, width, height, pixel_index))
        ]

infinite_pixel = False
def get_enhancement_key(imagemap, width, height, pixel_index):
    global infinite_pixel
    return int("".join([{"#":'1',".":"0"}.get(imagemap[i] if i else ("#" if infinite_pixel else ".")) for i in adjacent_cell_indicies(imagemap, width, height, pixel_index)]), 2)

def get_output_image(imagemap, width, height, algorithm, border=1):
    input_image, new_width, new_height = expand_imagemap(imagemap, width, height, border)
    return ([algorithm[get_enhancement_key(input_image, new_width, new_height, i)] for i in range(0,new_width*new_height)],new_width,new_height)


algorithm, image = process_lines(test_data)
imagemap, width, height = process_data(image)
show_imagemap(*process_data(image))
show_imagemap(*expand_imagemap(*process_data(image) + (2,)))
print("---")
assert get_enhancement_key(*process_data(image) + (12,)) == 34

algorithm, image = process_lines(test_data)
imagemap, width, height = process_data(image)
imagemap, width, height = get_output_image(imagemap, width, height, algorithm, 5)
imagemap, width, height = get_output_image(imagemap, width, height, algorithm, 5)
show_imagemap(imagemap, width, height)
assert len(list(filter(lambda c: c == "#", imagemap))) == 35

# Global variables for the WINNNNNN!
# When the infinite void winks at you, don't wink back.
def flip_infite():
    global infinite_pixel
    infinite_pixel = not infinite_pixel

# Part One
algorithm, image = process_lines(real_data)
imagemap, width, height = process_data(image)
for i in range(0, 50):
    imagemap, width, height = get_output_image(imagemap, width, height, algorithm)
    flip_infite()
print(len(list(filter(lambda c: c == "#", imagemap))))
# render_image(*expand_imagemap(imagemap, width, height, 50))
