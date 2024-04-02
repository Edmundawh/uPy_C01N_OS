from badge import oled, btn
from machine import Pin
from time import sleep_ms, ticks_ms
import framebuf as fb
import random

# Constants for the game
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
BLOCK_SIZE = 8

# Game variables
game_board = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
current_piece = None
current_x = SCREEN_WIDTH // 2
current_y = 0
score = 0

def draw_board():
    oled.fill(0)
    for y in range(len(game_board)):
        for x in range(len(game_board[y])):
            if game_board[y][x]:
                oled.fill_rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, 1)
    oled.text("Score: " + str(score), 0, SCREEN_HEIGHT - 10)
    oled.show()

def draw_piece():
    for y in range(4):
        for x in range(4):
            if current_piece[y][x]:
                oled.fill_rect((current_x + x) * BLOCK_SIZE, (current_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, 1)

def move_piece(dx, dy):
    global current_x, current_y
    if not check_collision(current_x + dx, current_y + dy, current_piece):
        current_x += dx
        current_y += dy

def check_collision(x, y, piece):
    for py in range(4):
        for px in range(4):
            if piece[py][px] and (x + px < 0 or x + px >= SCREEN_WIDTH // BLOCK_SIZE or
                                   y + py < 0 or y + py >= SCREEN_HEIGHT // BLOCK_SIZE or
                                   game_board[y + py][x + px]):
                return True
    return False

def rotate_piece():
    global current_piece
    rotated_piece = [[current_piece[y][x] for y in range(4)] for x in range(4)]
    for y in range(4):
        for x in range(4):
            rotated_piece[y][x] = current_piece[3 - x][y]
    if not check_collision(current_x, current_y, rotated_piece):
        current_piece = rotated_piece

def clear_rows():
    global score
    rows_cleared = 0
    for y in range(len(game_board)):
        if all(game_board[y]):
            del game_board[y]
            game_board.insert(0, [0] * (SCREEN_WIDTH // BLOCK_SIZE))
            rows_cleared += 1
    score += rows_cleared ** 2  # Adjust scoring as needed

def generate_piece():
    pieces = [
        [[1, 1, 1, 1]],
        [[1, 1], [1, 1]],
        [[1, 1, 1], [0, 1, 0]],
        [[0, 1, 0], [1, 1, 1]],
        # Add more pieces
    ]
    return random.choice(pieces)

def game_loop():
    global current_piece, current_x, current_y
    current_piece = generate_piece()
    current_x = SCREEN_WIDTH // 2
    current_y = 0
    while True:
        draw_board()
        draw_piece()
        if btn.U.value() == 0:
            rotate_piece()
        if btn.L.value() == 0:
            move_piece(-1, 0)
        if btn.R.value() == 0:
            move_piece(1, 0)
        if btn.D.value() == 0:
            move_piece(0, 1)
            if check_collision(current_x, current_y + 1, current_piece):
                for y in range(4):
                    for x in range(4):
                        if current_piece[y][x]:
                            game_board[current_y + y][current_x + x] = 1
                clear_rows()
                return
        sleep_ms(100)  # Adjust speed of falling blocks

def app_start():
    oled.fill(0)
    oled.show()
    while True:
        game_loop()

app_start()
