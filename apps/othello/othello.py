from badge import oled, btn
from time import sleep_ms

# Define constants
CELL_SIZE = 8
GRID_SIZE = 8
GRID_WIDTH = GRID_SIZE * CELL_SIZE
GRID_HEIGHT = GRID_SIZE * CELL_SIZE
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64

# Define colors
COLOR_BLACK = 0
COLOR_WHITE = 1

class ReversiGame:
    def __init__(self):
        self.board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.board[3][3] = 'W'
        self.board[4][4] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.current_player = 'B'  # Black plays first
        self.selected_cell = [3, 2]  # Initial selected cell
        self.scroll_offset = [0, 0]

    def draw(self):
        oled.fill(0)

        # Draw grid lines
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                oled.rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE, 1)

        # # Draw gridlines
        # for i in range(GRID_SIZE):
        #     for j in range(GRID_SIZE):
        #         x = i * CELL_SIZE
        #         y = j * CELL_SIZE
        #         oled.rect(x, y, CELL_SIZE, CELL_SIZE, COLOR_BLACK)

        # Draw pieces
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x = i * CELL_SIZE
                y = j * CELL_SIZE
                if self.board[i][j] == 'B':
                    self.draw_black_cross(x, y)
                elif self.board[i][j] == 'W':
                    self.draw_piece(x, y, COLOR_WHITE)

        # Highlight selected cell
        x = self.selected_cell[0] * CELL_SIZE
        y = self.selected_cell[1] * CELL_SIZE
        oled.rect(x, y, CELL_SIZE, CELL_SIZE, COLOR_WHITE)

        oled.show()

    def draw_piece(self, x, y, color):
        piece_size = CELL_SIZE // 2
        piece_x = x + CELL_SIZE // 2
        piece_y = y + CELL_SIZE // 2
        oled.fill_circle(piece_x, piece_y, piece_size, color)

    def draw_black_cross(self, x, y):
        cross_size = CELL_SIZE // 2
        cross_x = x + CELL_SIZE // 2
        cross_y = y + CELL_SIZE // 2
        oled.line(cross_x - cross_size, cross_y - cross_size, cross_x + cross_size, cross_y + cross_size, COLOR_WHITE)
        oled.line(cross_x + cross_size, cross_y - cross_size, cross_x - cross_size, cross_y + cross_size, COLOR_WHITE)

    def handle_input(self):
        initial_selected_cell = self.selected_cell.copy()

        if btn.U.value() == 0:
            if self.selected_cell[1] > 0:
                self.selected_cell[1] -= 1
        elif btn.D.value() == 0:
            if self.selected_cell[1] < GRID_SIZE - 1:
                self.selected_cell[1] += 1
        elif btn.L.value() == 0:
            if self.selected_cell[0] > 0:
                self.selected_cell[0] -= 1
        elif btn.R.value() == 0:
            if self.selected_cell[0] < GRID_SIZE - 1:
                self.selected_cell[0] += 1
        elif btn.A.value() == 0:  # Place piece
            if self.is_valid_move():
                self.place_piece()
                self.current_player = 'W' if self.current_player == 'B' else 'B'

        if initial_selected_cell != self.selected_cell:
            self.scroll_offset[0] = min(max(0, self.scroll_offset[0]), GRID_WIDTH - DISPLAY_WIDTH)
            self.scroll_offset[1] = min(max(0, self.scroll_offset[1]), GRID_HEIGHT - DISPLAY_HEIGHT)

    def is_valid_move(self):
        x, y = self.selected_cell
        if self.board[x][y] != ' ':
            return False
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                if self.check_and_flip(x, y, dx, dy, self.current_player):
                    return True
        return False

    def place_piece(self):
        x, y = self.selected_cell
        self.board[x][y] = self.current_player
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                self.check_and_flip(x, y, dx, dy, self.current_player)

    def check_and_flip(self, x, y, dx, dy, player):
        nx, ny = x + dx, y + dy
        to_flip = []
        while 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and self.board[nx][ny] != ' ' and self.board[nx][ny] != player:
            to_flip.append((nx, ny))
            nx += dx
            ny += dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and self.board[nx][ny] == player:
            for flip_x, flip_y in to_flip:
                self.board[flip_x][flip_y] = player
            return True
        return False

    def is_game_over(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True

def app_start():
    game = ReversiGame()

    while not game.is_game_over():
        game.handle_input()
        game.draw()
        sleep_ms(100)

    oled.fill(0)
    oled.text("Game Over!", 30, 28, COLOR_WHITE)
    oled.show()

    while True:
        pass

app_start()


# from badge import oled, btn
# from time import sleep_ms

# # Define constants
# CELL_SIZE = 8
# GRID_SIZE = 8
# GRID_WIDTH = GRID_SIZE * CELL_SIZE
# GRID_HEIGHT = GRID_SIZE * CELL_SIZE
# DISPLAY_WIDTH = 128
# DISPLAY_HEIGHT = 64

# # Define colors
# COLOR_BLACK = 0
# COLOR_WHITE = 1

# class ReversiGame:
#     def __init__(self):
#         self.board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
#         self.board[3][3] = 'W'
#         self.board[4][4] = 'W'
#         self.board[3][4] = 'B'
#         self.board[4][3] = 'B'
#         self.current_player = 'B'  # Black plays first
#         self.selected_cell = [3, 2]  # Initial selected cell
#         self.scroll_offset = [0, 0]

#     def draw(self):
#         oled.fill(0)

#         # Determine the visible range of cells
#         start_x = max(0, self.selected_cell[0] - DISPLAY_WIDTH // CELL_SIZE // 2)
#         start_y = max(0, self.selected_cell[1] - DISPLAY_HEIGHT // CELL_SIZE // 2)
#         end_x = min(GRID_SIZE, start_x + DISPLAY_WIDTH // CELL_SIZE)
#         end_y = min(GRID_SIZE, start_y + DISPLAY_HEIGHT // CELL_SIZE)

#         # Draw grid lines and pieces
#         for i in range(start_x, end_x):
#             for j in range(start_y, end_y):
#                 x = (i - start_x) * CELL_SIZE
#                 y = (j - start_y) * CELL_SIZE
#                 if [i, j] == self.selected_cell:
#                     oled.rect(x, y, CELL_SIZE, CELL_SIZE, COLOR_WHITE)
#                 else:
#                     oled.rect(x, y, CELL_SIZE, CELL_SIZE, COLOR_BLACK)
#                 if self.board[i][j] == 'B':
#                     self.draw_black_cross(x, y)
#                 elif self.board[i][j] == 'W':
#                     self.draw_piece(x, y, COLOR_WHITE)

#         oled.show()

#     def draw_piece(self, x, y, color):
#         piece_size = CELL_SIZE // 2
#         piece_x = x + CELL_SIZE // 2
#         piece_y = y + CELL_SIZE // 2
#         oled.fill_circle(piece_x, piece_y, piece_size, color)

#     def draw_black_cross(self, x, y):
#         cross_size = CELL_SIZE // 2
#         cross_x = x + CELL_SIZE // 2
#         cross_y = y + CELL_SIZE // 2
#         oled.line(cross_x - cross_size, cross_y - cross_size, cross_x + cross_size, cross_y + cross_size, COLOR_WHITE)
#         oled.line(cross_x + cross_size, cross_y - cross_size, cross_x - cross_size, cross_y + cross_size, COLOR_WHITE)

#     def handle_input(self):
#         # Record the initial selected cell position for comparison
#         initial_selected_cell = self.selected_cell.copy()

#         if btn.U.value() == 0:
#             if self.selected_cell[1] > 0:
#                 self.selected_cell[1] -= 1
#         elif btn.D.value() == 0:
#             if self.selected_cell[1] < GRID_SIZE - 1:
#                 self.selected_cell[1] += 1
#         elif btn.L.value() == 0:
#             if self.selected_cell[0] > 0:
#                 self.selected_cell[0] -= 1
#         elif btn.R.value() == 0:
#             if self.selected_cell[0] < GRID_SIZE - 1:
#                 self.selected_cell[0] += 1
#         elif btn.A.value() == 0:  # Place piece
#             self.place_piece()
#             self.current_player = 'W' if self.current_player == 'B' else 'B'

#         # Check if the selected cell position has changed
#         if initial_selected_cell != self.selected_cell:
#             # Ensure the scroll offset does not go beyond the board boundaries
#             self.scroll_offset[0] = min(max(0, self.scroll_offset[0]), GRID_WIDTH - DISPLAY_WIDTH)
#             self.scroll_offset[1] = min(max(0, self.scroll_offset[1]), GRID_HEIGHT - DISPLAY_HEIGHT)

#     def place_piece(self):
#         x, y = self.selected_cell
#         if self.board[x][y] == ' ':
#             self.board[x][y] = self.current_player
#             # Check for flips in all directions
#             for dx in range(-1, 2):
#                 for dy in range(-1, 2):
#                     if dx == 0 and dy == 0:
#                         continue
#                     self.check_and_flip(x, y, dx, dy, self.current_player)

#     def check_and_flip(self, x, y, dx, dy, player):
#         nx, ny = x + dx, y + dy
#         to_flip = []
#         while 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and self.board[nx][ny] != ' ' and self.board[nx][ny] != player:
#             to_flip.append((nx, ny))
#             nx += dx
#             ny += dy
#         if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and self.board[nx][ny] == player:
#             for flip_x, flip_y in to_flip:
#                 self.board[flip_x][flip_y] = player

#     def is_game_over(self):
#         # Game ends when the board is full
#         for row in self.board:
#             if ' ' in row:
#                 return False
#         return True

# def app_start():
#     game = ReversiGame()

#     while not game.is_game_over():
#         game.handle_input()
#         game.draw()
#         sleep_ms(100)

#     oled.fill(0)
#     oled.text("Game Over!", 30, 28, COLOR_WHITE)
#     oled.show()

#     while True:
#         pass

# app_start()





