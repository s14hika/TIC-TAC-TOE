import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Initialize the board
board = [' '] * 9

def draw_board_image(size, board, message=None):
    img = Image.new('RGB', size, color='black')
    draw = ImageDraw.Draw(img)

    # Define font and size
    try:
        font = ImageFont.truetype("arial.ttf", 30)
        small_font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        print("Arial font not found. Using default font.")
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Calculate positions
    width, height = size
    cell_width = width // 3
    cell_height = height // 3

    for i in range(9):
        row = i // 3
        col = i % 3
        x = col * cell_width
        y = row * cell_height
        if board[i] == 'X':
            draw.text((x + cell_width // 4, y + cell_height // 4), 'X', font=font, fill='blue')
        elif board[i] == 'O':
            draw.text((x + cell_width // 4, y + cell_height // 4), 'O', font=font, fill='red')

    if message:
        # Draw the game status message
        draw.text((10, height - 40), message, font=small_font, fill='white')

    return np.array(img)

def make_move(board, position, player):
    if board[position] == ' ':
        board[position] = player
        return True
    return False

def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != ' ':
            return board[condition[0]]
    return None

def is_board_full(board):
    return ' ' not in board

# Create a blank image window
W, H = 600, 800
window_name = 'Real-Time Game Display'
cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)

# Initialize game state
player = 'X'
message = None

print("Game Loop Started")

try:
    while True:
        # Create a blank image for the game board
        game_board_img = draw_board_image((W, H), board, message)
        
        # Display the game board image
        cv.imshow(window_name, game_board_img)

        key = cv.waitKey(1) & 0xFF

        if key == ord('q'):  # Press 'q' to quit
            break
        elif key in map(ord, '123456789'):
            move = int(chr(key)) - 1
            if make_move(board, move, player):
                player = 'O' if player == 'X' else 'X'

        winner = check_winner(board)
        if winner:
            message = f"Player {winner} wins!"
            game_board_img = draw_board_image((W, H), board, message)
            cv.imshow(window_name, game_board_img)
            cv.waitKey(2000)  # Display message for 2 seconds
            break
        if is_board_full(board):
            message = "It's a draw!"
            game_board_img = draw_board_image((W, H), board, message)
            cv.imshow(window_name, game_board_img)
            cv.waitKey(2000)  # Display message for 2 seconds
            break

except KeyboardInterrupt:
    print('Received Ctrl-C')

cv.destroyAllWindows()
print("Program ended")
