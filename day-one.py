import functools

def count_changes(current_value, next_value):
    if (type(current_value) is tuple):
        last_value, current_increases = current_value
    else:
        last_value, current_increases = (current_value, 0)
    if (next_value > last_value):
        current_increases += 1

    return (next_value, current_increases)

WINDOW_SIZE = 3
def smooth_data(current_value, next_value):

    if (type(current_value) is tuple):
        current_smoothed_data, windows = current_value
    else:
        current_smoothed_data, windows = ([],[[current_value]])

    # add our next value to active windows
    for window in windows:
        window.append(next_value)

        # if the addition of the next value makes this window big enough to use
        # for smoothing, then let's add the sum to the current_smoothed_data
        if (len(window) == WINDOW_SIZE):
            current_smoothed_data.append(sum(window))

    # Also append the next_value as an entry in a new window
    windows.append([next_value])

    # We want to remove any windows from our current set if they have been used
    # for calculations already
    return (current_smoothed_data, list(filter(lambda window: len(window) < WINDOW_SIZE, windows)))

f = open('day-one-input.txt')
next_value, increases = functools.reduce(count_changes, [int(x) for x in f.readlines()])
f.close()

print("Raw Increases %d" % increases)

f = open('day-one-input.txt')
current_smoothed_data, windows = functools.reduce(smooth_data, [int(x) for x in f.readlines()])
next_value, increases = functools.reduce(count_changes, current_smoothed_data)
print("Smoothed Increases %d" % increases)
f.close()
