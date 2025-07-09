# Chess Capture Checker — Program Requirements
# --------------------------------------------
# 1. Ask the user to input a white piece and its position.
#    - User chooses between two predefined piece types (e.g., "pawn" and "rook").
#    - Input format must be: "<piece> <position>", e.g., "rook d5".
#
# 2. After setting the white piece, prompt the user to add black pieces.
#    - Input format is the same: "<piece> <position>", e.g., "knight a7".
#    - User must add at least 1 black piece and can add up to 16.
#    - Once at least one black piece has been added, the user can type "done"
#      to stop adding more black pieces.
#
#
# 3. Input validation:
#    - Assume inputs are either "done" or in the correct format ("<piece> <position>").
#    - Position must be within valid chess coordinates (a-h, 1-8).
#    - Prevent user from typing "done" before adding at least one black piece.
#
# 4. After each piece is entered:
#    - Print a confirmation if the piece was added successfully.
#    - Otherwise, print an error message explaining the issue.
#
# 5. Once all pieces are placed:
#    - Print a list of black pieces (if any) that the white piece can capture.

# position: "a5"; coordinates; 0, 4
BOARD_WIDTH = 8
VALID_FILES = "abcdefgh"
VALID_RANKS = "12345678"
VALID_PIECES = ["rook", "pawn"]

# Utility functions
def get_position_from_coordinates(coordinates):
    x, y = coordinates
    return f"{VALID_FILES[x]}{y + 1}"

def get_coordinates_from_position(pos):
    file = pos[0].lower() # a-h
    rank = pos[1]         # 1-8

    x = VALID_FILES.index(file)
    y = int(rank) - 1

    return x, y

def is_position_valid(pos):
    if len(pos) != 2:
        return False
    file = pos[0].lower() # a-h
    rank = pos[1]         # 1-8
    if file not in VALID_FILES or rank not in VALID_RANKS:
        return False
    return True

# Game related functions
def get_piece_and_its_coordinates(type, black_pieces = (), white_coordinates = None):
    # type can either be 'white' or 'black'
    while True:
        formatted_user_input = input(f"Input your {type} piece and its position (example: rook a5): ")

        # 'black'-specific if block
        if type == 'black' and len(black_pieces) == 16:
            print ("You have reached the limit allowed for black pieces")
            return '', ''
        if type == 'black' and formatted_user_input == "done":
            if len(black_pieces) == 0:
                print("You must add at least 1 black piece")
                continue

            # Returning empty piece and empty coordinates when user is done
            # This is done so that you can check
            return '', ''

        piece_and_position_from_user_input = formatted_user_input.split()

        if len(piece_and_position_from_user_input) != 2:
            print("Invalid format. Should use a piece + coordinates (e.g. bishop e5).")
            continue

        piece, position = piece_and_position_from_user_input

        # 'white'-specific if block
        if type == 'white' and piece.lower().strip() not in VALID_PIECES:
            print("Only rooks and pawns are allowed for white pieces")
            continue

        # Validate position
        if not is_position_valid(position):
            print ("Invalid coordinates. Use positions from a1 to h8.")
            continue

        # Coordinates do not require addl' validation because the position is already valid
        coordinates = get_coordinates_from_position(position)

        # 'black'-specific if block
        if type == 'black' and coordinates == white_coordinates or coordinates in [b[1] for b in black_pieces]:
            print("This spot is already taken. Enter other coordinates")
            continue

        return piece, coordinates


def get_black_pieces(white_coordinates):
    black_pieces = []

    while True:
        black_piece, black_coordinates = get_piece_and_its_coordinates('black', black_pieces, white_coordinates)

        if not black_piece or not black_coordinates:
            break

        black_pieces.append((black_piece, black_coordinates))
        print(f"You've added {black_piece} at {get_position_from_coordinates(black_coordinates)}")

    return black_pieces

def get_captured_pieces(white_piece, white_coordinates, black_pieces):
    captured = []
    wx, wy = white_coordinates             # w stands for WHITE

    for piece, (bx, by) in black_pieces:  # b stands for BLACK
        if white_piece == "rook":
            if wx == bx or wy == by:
                captured.append((piece, (bx, by)))
        elif white_piece == "pawn":
            if (bx == wx - 1 or bx == wx +1) and by == wy +1:
                captured.append((piece, (bx, by)))
    return captured


# GAME START
white_piece, white_coordinates = get_piece_and_its_coordinates('white')
print (f"White {white_piece} placed at {get_position_from_coordinates(white_coordinates)}")

# black_pieces looks like this: [('bishop', (4, 5)), ('pawn', (0, 2))]
black_pieces = get_black_pieces(white_coordinates)

# captured_pieces is a list of captured pieces
captured_pieces = get_captured_pieces(white_piece, white_coordinates, black_pieces)

if captured_pieces:
    print("\nBlack pieces that can be captured:")
    for piece, coordinates in captured_pieces:
        print(f"{piece} at {get_position_from_coordinates(coordinates)}")
else:
    print("\nNo black pieces to capture")
