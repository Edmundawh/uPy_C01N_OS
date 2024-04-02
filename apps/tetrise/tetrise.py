from badge import oled, btn
from time import sleep_ms, ticks_ms
from random import choice

# Define constants
CELL_SIZE = 4
GRID_WIDTH = 128 // CELL_SIZE
GRID_HEIGHT = 64 // CELL_SIZE

# Define colors
COLOR_BLACK = 0
COLOR_WHITE = 1

class TetrisGame:
    def __init__(self):
        self.grid = [[COLOR_BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.generate_piece()
        self.piece_x = GRID_WIDTH // 2
        self.piece_y = 0
        self.score = 0
        self.game_over = False
        self.last_move_time = ticks_ms()
        self.move_interval = 500  # milliseconds

    def generate_piece(self):
        pieces = [
            [[1, 1, 1],         # I piece
            [1, 1, 1],
            [1, 1, 1]],

            [[1, 1, 1],      # T piece
            [1, 1, 1],
            [0, 1, 0],
            [0, 1, 0]],

            [[1, 1, 1, 1],         # L piece
            [1, 1, 1, 1],
            [1, 1, 0, 0],
            [1, 1, 0, 0]],

            [[1, 1,1],         # J piece
            [1, 1,1],
            [0, 1, 1],
            [0, 1,1]],

            [[1, 1, 1],         # O piece
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]],

            [[0, 0, 1, 1],         # Z piece
            [1, 1, 1, 1],
            [1, 1, 0, 0]]
        ]
        return choice(pieces)



    def rotate_piece(self):
        self.current_piece = [[self.current_piece[y][x] for y in range(len(self.current_piece))] for x in range(len(self.current_piece[0]) - 1, -1, -1)]

    def move_piece_down(self):
        self.piece_y += 1
        if self.check_collision():
            self.piece_y -= 1
            self.lock_piece()
            self.clear_lines()
            self.current_piece = self.generate_piece()
            self.piece_x = GRID_WIDTH // 2
            self.piece_y = 0
            if self.check_collision():
                self.game_over = True

    def move_piece_sideways(self, direction):
        new_x = self.piece_x + direction
        if 0 <= new_x < GRID_WIDTH:
            self.piece_x = new_x
            if self.check_collision():
                self.piece_x -= direction

    def check_collision(self):
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[0])):
                if self.current_piece[y][x] == 1:
                    if (self.piece_x + x < 0 or self.piece_x + x >= GRID_WIDTH or
                            self.piece_y + y >= GRID_HEIGHT or
                            self.grid[self.piece_y + y][self.piece_x + x] != COLOR_BLACK):
                        return True
        return False

    def lock_piece(self):
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[0])):
                if self.current_piece[y][x] == 1:
                    self.grid[self.piece_y + y][self.piece_x + x] = COLOR_WHITE
        self.current_piece = self.generate_piece()  # Generate a new piece

    def clear_lines(self):
        lines_cleared = 0
        for y in range(GRID_HEIGHT):
            if COLOR_BLACK not in self.grid[y]:
                del self.grid[y]
                self.grid.insert(0, [COLOR_BLACK for _ in range(GRID_WIDTH)])
                lines_cleared += 1
        self.score += lines_cleared

    def draw(self):
        oled.fill(0)

        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] == COLOR_WHITE:
                    oled.fill_rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, COLOR_WHITE)

        # Draw current piece
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[0])):
                if self.current_piece[y][x] == 1:
                    oled.fill_rect((self.piece_x + x) * CELL_SIZE, (self.piece_y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE, COLOR_WHITE)

        # Draw score
        oled.text("Score: {}".format(self.score), 2, 2, COLOR_WHITE)

        oled.show()

def app_start():
    game = TetrisGame()

    while not game.game_over:
        if btn.B.value() == 0:
            return  # Exit game if 'B' is pressed

        if ticks_ms() - game.last_move_time >= game.move_interval:
            game.move_piece_down()
            game.last_move_time = ticks_ms()

        if btn.U.value() == 0:
            game.rotate_piece()
        elif btn.D.value() == 0:
            game.move_piece_down()
        elif btn.L.value() == 0:
            game.move_piece_sideways(-1)
        elif btn.R.value() == 0:
            game.move_piece_sideways(1)

        game.draw()
        sleep_ms(50)  # Adjust speed here

    # Display "Game Over" and "Score" until 'B' or 'A' button is pressed
    while True:
        oled.fill(0)
        oled.text("Game Over", 30, 8, COLOR_WHITE)
        oled.text("Score: {}".format(game.score), 30, 18, COLOR_WHITE)
        oled.text("[B] to Restart", 8, 38, COLOR_WHITE)
        oled.text("[U] to Exit", 20, 48, COLOR_WHITE)
        oled.show()

        if btn.B.value() == 0:
            app_start()  # Restart game if 'B' is pressed
        elif btn.U.value() == 0:
            return  # Exit game if 'U' is pressed

app_start()