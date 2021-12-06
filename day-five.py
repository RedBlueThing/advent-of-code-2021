import functools
import pygame

test_data = [
    "0,9 -> 5,9", "8,0 -> 0,8", "9,4 -> 3,4", "2,2 -> 2,1", "7,0 -> 7,4", "6,4 -> 2,0", "0,9 -> 2,9", "3,4 -> 1,4",
    "0,0 -> 8,8", "5,5 -> 8,2"
]

expected_overlaps_part_one = 5
expected_overlaps_part_two = 12


def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, list) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


expected_seafloor_with_rows = [[0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                               [0, 1, 1, 2, 1, 1, 1, 2, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 2, 1, 1, 1, 0, 0, 0, 0]]

# actually .. just treat this like a screen buffer
expected_seafloor = flatten(expected_seafloor_with_rows)


def seafloor_pixel_index(x, y, seafloor_width, seafloor_height):
    return (seafloor_width * y) + x


def draw_seafloor(seafloor, seafloor_width, seafloor_height):
    for y in range(0, seafloor_height):
        for x in range(0, seafloor_width):
            index = seafloor_pixel_index(x, y, seafloor_width, seafloor_height)
            pixel = seafloor[index]
            print(pixel if pixel > 0 else ".", end="")
        print("")


def render_seafloor(seafloor, seafloor_width, seafloor_height):
    pygame.init()
    screen = pygame.display.set_mode((seafloor_width, seafloor_height))
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

        for y in range(0, seafloor_height):
            for x in range(0, seafloor_width):
                index = seafloor_pixel_index(x, y, seafloor_width, seafloor_height)
                pixel = seafloor[index] * 40
                background.set_at((x, y), (pixel,pixel,pixel))

        screen.blit(background, (0, 0))  #draw background on screen (overwriting all)

        pygame.display.flip()  # flip the screen 30 times a second



def update_seafloor_pixel(seafloor, x, y, seafloor_width, seafloor_height):
    pixel_index = seafloor_pixel_index(x, y, seafloor_width, seafloor_height)
    assert pixel_index >= 0 and pixel_index < seafloor_width * seafloor_height, "Index was %d, x:%d, y%d" % (
        pixel_index, x, y)

    # just add one to the seafloor "pixel" at the location
    seafloor[pixel_index] += 1

    return seafloor


def draw_vent_line_part_one(seafloor, x1, y1, x2, y2, seafloor_width, seafloor_height):

    # for now ignore zero gradient lines
    if (x1 != x2 and y1 != y2):
        return seafloor

    if (x1 == x2):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            seafloor = update_seafloor_pixel(seafloor, x2, y, seafloor_width, seafloor_height)
    if (y1 == y2):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            seafloor = update_seafloor_pixel(seafloor, x, y2, seafloor_width, seafloor_height)

    return seafloor


def gradient(x1, y1, x2, y2):
    if ((x2 - x1) == 0):
        return 0
    return (y2 - y1) / (x2 - x1)


def draw_vent_line_part_two(seafloor, x1, y1, x2, y2, seafloor_width, seafloor_height):

    if (x1 == x2 or y1 == y2):
        return draw_vent_line_part_one(seafloor, x1, y1, x2, y2, seafloor_width, seafloor_height)

    rise = (y2 - y1)
    run = (x2 - x1)

    current_x = x1
    current_y = y1

    def offset(value):
        if not value:
            return 0
        return int(value / abs(value))

    while (current_x != x2 and current_y != y2):
        seafloor = update_seafloor_pixel(seafloor, current_x, current_y, seafloor_width, seafloor_height)
        current_x += offset(run)
        current_y += offset(rise)
    seafloor = update_seafloor_pixel(seafloor, current_x, current_y, seafloor_width, seafloor_height)

    return seafloor


def process_vent_line_data(data, draw_vent_line_fn, do_draw_seafloor=True):
    lines = []
    for vent_line in data:
        lines.append(
            tuple([int(value) for value in flatten([endpoint.split(",") for endpoint in vent_line.split(" -> ")])]))

    # I think we need to determine the size of the sea floor based on the lines we have
    seafloor_width = max([max(x1, x2) for x1, y1, x2, y2 in lines]) + 1
    seafloor_height = max([max(y1, y2) for x1, y1, x2, y2 in lines]) + 1

    # So now we can create a kind of screen buffer for the sea floor
    seafloor = [0 for i in range(0, seafloor_width * seafloor_height)]

    # now we just need to draw the lines
    for line in lines:
        x1, y1, x2, y2 = line
        seafloor = draw_vent_line_fn(seafloor, x1, y1, x2, y2, seafloor_width, seafloor_height)

    if (do_draw_seafloor):
        draw_seafloor(seafloor, seafloor_width, seafloor_height)
    # else:
    #     render_seafloor(seafloor, seafloor_width, seafloor_height)

    return len([x for x in seafloor if x > 1])


test_overlaps_part_one = process_vent_line_data(test_data, draw_vent_line_part_one)
print(test_overlaps_part_one == expected_overlaps_part_one)

test_overlaps_part_two = process_vent_line_data(test_data, draw_vent_line_part_two)
print(test_overlaps_part_two == expected_overlaps_part_two)

f = open('day-five-input.txt')
print(process_vent_line_data(f.readlines(), draw_vent_line_part_one, do_draw_seafloor=False))
f.close()

f = open('day-five-input.txt')
print(process_vent_line_data(f.readlines(), draw_vent_line_part_two, do_draw_seafloor=False))
f.close()
