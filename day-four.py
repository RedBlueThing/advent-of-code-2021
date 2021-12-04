import functools

expected_score = 4512
expected_losing_score = 1924
test_data = [
    "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1", "", "22 13 17 11  0", " 8  2 23  4 24",
    "21  9 14 16  7", " 6 10  3 18  5", " 1 12 20 15 19", "", " 3 15  0  2 22", " 9 18 13 17  5", "19  8  7 25 23",
    "20 11 10 24  4", "14 21 16 12  6", "", "14 21 17 24  4", "10 16 15  9 19", "18  8 23 26 20", "22 11 13  6  5",
    " 2  0 12  3  7"
]


def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, list) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


def process_row(raw_data_line, current_board_rows):
    """
    assumes a row of numbers
    """
    assert raw_data_line, "Raw data line was %s" % raw_data_line
    print(raw_data_line)
    try:
        current_board_rows.append([{
            "matched": False,
            "number": int(value)
        } for value in [x for x in raw_data_line.split(" ") if x]])
        return current_board_rows
    except:
        print("Exception? %s" % raw_data_line)
        raise


def process_game_data(raw_data):
    # Turn our input random numbers into an array of numbers
    random_numbers = [int(x) for x in raw_data[0].split(",")]
    boards = []
    current_board_rows = []
    # Start from the third line because we know what our input will look like
    for raw_data_line in raw_data[2:]:
        # We are done with a board, time to start the next one
        if not raw_data_line or raw_data_line == "\n":
            assert current_board_rows, "Why haven't we got any rows %s,%s,%s" % (raw_data_line, str(boards),
                                                                                 str(current_board_rows))
            boards.append(current_board_rows)
            current_board_rows = []
            continue
        # We have a board row to process
        current_board_rows = process_row(raw_data_line, current_board_rows)

    boards.append(current_board_rows)
    return boards, random_numbers


def row_at_index(board, index):
    return board[index]


def column_at_index(board, index):
    return [row[index] for row in board]


def call_number_on_board_row(board_row, called_number):
    return [{**entry, **{"matched": entry["matched"] or entry["number"] == called_number}} for entry in board_row]


def call_number(board, called_number):
    return [call_number_on_board_row(board_row, called_number) for board_row in board]


def size_of_board(board):
    return (len(board), len(board[0]))


def winning_board(board):
    rows, columns = size_of_board(board)
    for index in range(0, rows):
        if all([entry["matched"] for entry in row_at_index(board, index)]):
            return True
    for index in range(0, columns):
        if all([entry["matched"] for entry in column_at_index(board, index)]):
            return True


def score_board(board, called_number):
    # sum of all the unmatched numbers
    return sum([entry["number"] for entry in flatten(board) if not entry["matched"]]) * called_number


def find_winning_score(boards, random_numbers):
    for called_number in random_numbers:
        boards = [call_number(board, called_number) for board in boards]
        for board in boards:
            if winning_board(board):
                return score_board(board, called_number)


def find_losing_score(boards, random_numbers):
    winning_board_scores = []
    remaining_boards = boards
    for called_number in random_numbers:
        remaining_boards = [call_number(board, called_number) for board in remaining_boards]
        winning_board_scores += [
            score_board(board, called_number) for board in remaining_boards if winning_board(board)
        ]
        remaining_boards = [board for board in remaining_boards if not winning_board(board)]
    return winning_board_scores[-1]


test_score = find_winning_score(*process_game_data(test_data))
print(test_score == expected_score)
test_score = find_losing_score(*process_game_data(test_data))
print(test_score == expected_losing_score)

f = open('day-four-input.txt')
part_one_score = find_winning_score(*process_game_data(f.readlines()))
print(part_one_score)
f.close()

f = open('day-four-input.txt')
part_two_score = find_losing_score(*process_game_data(f.readlines()))
print(part_two_score)
f.close()
