from badge import oled, btn
from time import sleep_ms
import random

# Define constants
GRID_WIDTH = 13  # Reduced width
GRID_HEIGHT = 6  # Reduced height
NUM_MINES = 4  # Reduced number of mines

# Define colors
COLOR_WHITE = 1
COLOR_BLACK = 0
COLOR_RED = 2

CELL_SIZE = 10  # Size of each cell in pixels

class MinesweeperGame:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.mines = self.place_mines()
        self.revealed = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.game_over = False
        self.cursor_x = 0
        self.cursor_y = 0

    def place_mines(self):
        mines = set()
        while len(mines) < NUM_MINES:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            mines.add((x, y))
        return mines

    def move_cursor(self, direction):
        if direction == 'U':
            self.cursor_y = max(0, self.cursor_y - 1)
        elif direction == 'D':
            self.cursor_y = min(GRID_HEIGHT - 1, self.cursor_y + 1)
        elif direction == 'L':
            self.cursor_x = max(0, self.cursor_x - 1)
        elif direction == 'R':
            self.cursor_x = min(GRID_WIDTH - 1, self.cursor_x + 1)

    def reveal_cell(self, x=None, y=None):
        if x is None:
            x = self.cursor_x
        if y is None:
            y = self.cursor_y

        if (x, y) in self.mines:
            self.game_over = True
        elif not self.revealed[y][x]:
            self.revealed[y][x] = True
            if self.count_adjacent_mines(x, y) == 0:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        new_x = x + dx
                        new_y = y + dy
                        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                            self.reveal_cell(new_x, new_y)
    
        # Check if all non-mine cells are revealed
        if all(self.revealed[y][x] or (x, y) in self.mines for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH)):
            self.game_over = True

    def count_adjacent_mines(self, x, y):
        count = sum((x + dx, y + dy) in self.mines for dx in range(-1, 2) for dy in range(-1, 2) if 0 <= x + dx < GRID_WIDTH and 0 <= y + dy < GRID_HEIGHT)
        return count

    def draw(self):
        oled.fill(0)

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.revealed[y][x]:
                    if (x, y) in self.mines:
                        oled.fill_rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, COLOR_RED)
                    else:
                        count = self.count_adjacent_mines(x, y)
                        if count > 0:
                            oled.text(str(count), x * CELL_SIZE, y * CELL_SIZE, COLOR_WHITE)
                        else:
                            oled.text("0", x * CELL_SIZE, y * CELL_SIZE, COLOR_WHITE)
                else:
                    oled.fill_rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, COLOR_BLACK)

        # Blinking cursor
        if not self.game_over:
            if (self.cursor_x, self.cursor_y) not in self.mines:
                oled.fill_rect(self.cursor_x * CELL_SIZE, self.cursor_y * CELL_SIZE, CELL_SIZE, CELL_SIZE, COLOR_WHITE)
                oled.show()
                sleep_ms(200)  # Reduced sleep duration
                oled.fill_rect(self.cursor_x * CELL_SIZE, self.cursor_y * CELL_SIZE, CELL_SIZE, CELL_SIZE, COLOR_BLACK)
                oled.show()
                sleep_ms(200)  # Reduced sleep duration

def app_start():
    game = MinesweeperGame()

    while not game.game_over:
        if btn.U.value() == 0:
            game.move_cursor('U')
        elif btn.D.value() == 0:
            game.move_cursor('D')
        elif btn.L.value() == 0:
            game.move_cursor('L')
        elif btn.R.value() == 0:
            game.move_cursor('R')
        elif btn.A.value() == 0:
            game.reveal_cell()

        game.draw()
        sleep_ms(50)  # Adjusted sleep duration for responsiveness

    # Display game over message
    oled.fill(0)
    if all(game.revealed[y][x] or (x, y) in game.mines for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH)):
        oled.text("You win!", 28, 28, COLOR_WHITE)
    else:
        oled.text("Game Over!", 28, 28, COLOR_WHITE)
    oled.show()

    # Wait for button B to be pressed to continue
    while btn.B.value() != 0:
        pass

    # Clear the display before starting a new game
    oled.fill(0)

app_start()

# from badge import oled, btn
# from time import sleep_ms
# import random

# # Define constants
# GRID_WIDTH = 13  # Reduced width
# GRID_HEIGHT = 6  # Reduced height
# NUM_MINES = 4  # Reduced number of mines

# # Define colors
# COLOR_WHITE = 1
# COLOR_BLACK = 0
# COLOR_RED = 2

# CELL_SIZE = 10  # Size of each cell in pixels

# class MinesweeperGame:
#     def __init__(self):
#         self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
#         self.mines = self.place_mines()
#         self.revealed = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
#         self.game_over = False
#         self.cursor_x = 0
#         self.cursor_y = 0

#     def place_mines(self):
#         mines = set()
#         while len(mines) < NUM_MINES:
#             x = random.randint(0, GRID_WIDTH - 1)
#             y = random.randint(0, GRID_HEIGHT - 1)
#             mines.add((x, y))
#         return mines

#     def move_cursor(self, direction):
#         if direction == 'U':
#             self.cursor_y = max(0, self.cursor_y - 1)
#         elif direction == 'D':
#             self.cursor_y = min(GRID_HEIGHT - 1, self.cursor_y + 1)
#         elif direction == 'L':
#             self.cursor_x = max(0, self.cursor_x - 1)
#         elif direction == 'R':
#             self.cursor_x = min(GRID_WIDTH - 1, self.cursor_x + 1)

#     def reveal_cell(self, x=None, y=None):
#         if x is None:
#             x = self.cursor_x
#         if y is None:
#             y = self.cursor_y

#         if (x, y) in self.mines:
#             self.game_over = True
#         elif not self.revealed[y][x]:
#             self.revealed[y][x] = True
#             if self.count_adjacent_mines(x, y) == 0:
#                 for dx in range(-1, 2):
#                     for dy in range(-1, 2):
#                         new_x = x + dx
#                         new_y = y + dy
#                         if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
#                             self.reveal_cell(new_x, new_y)

#     def count_adjacent_mines(self, x, y):
#         count = sum((x + dx, y + dy) in self.mines for dx in range(-1, 2) for dy in range(-1, 2) if 0 <= x + dx < GRID_WIDTH and 0 <= y + dy < GRID_HEIGHT)
#         return count

#     def draw(self):
#         oled.fill(0)

#         for y in range(GRID_HEIGHT):
#             for x in range(GRID_WIDTH):
#                 if self.revealed[y][x]:
#                     if (x, y) in self.mines:
#                         oled.fill_rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, COLOR_RED)
#                     else:
#                         count = self.count_adjacent_mines(x, y)
#                         if count > 0:
#                             oled.text(str(count), x * CELL_SIZE, y * CELL_SIZE, COLOR_WHITE)
#                         else:
#                             oled.text("0", x * CELL_SIZE, y * CELL_SIZE, COLOR_WHITE)
#                 else:
#                     oled.fill_rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, COLOR_BLACK)

#         # Blinking cursor
#         if not self.game_over:
#             if (self.cursor_x, self.cursor_y) not in self.mines:
#                 oled.fill_rect(self.cursor_x * CELL_SIZE, self.cursor_y * CELL_SIZE, CELL_SIZE, CELL_SIZE, COLOR_WHITE)
#                 oled.show()
#                 sleep_ms(300)
#                 oled.fill_rect(self.cursor_x * CELL_SIZE, self.cursor_y * CELL_SIZE, CELL_SIZE, CELL_SIZE, COLOR_BLACK)
#                 oled.show()
#                 sleep_ms(300)

# def app_start():
#     game = MinesweeperGame()

#     while not game.game_over:
#         if btn.U.value() == 0:
#             game.move_cursor('U')
#         elif btn.D.value() == 0:
#             game.move_cursor('D')
#         elif btn.L.value() == 0:
#             game.move_cursor('L')
#         elif btn.R.value() == 0:
#             game.move_cursor('R')
#         elif btn.A.value() == 0:
#             game.reveal_cell()

#         game.draw()
#         sleep_ms(100)  # Adjust speed here

#     # Display game over message
#     oled.fill(0)
#     oled.text("Game Over!", 28, 28, COLOR_WHITE)
#     oled.show()

#     # Wait for button B to be pressed to continue
#     while btn.B.value() != 0:
#         pass

#     # Clear the display before starting a new game
#     oled.fill(0)

# app_start()



# from badge import oled, btn
# from time import sleep_ms
# import random

# # Define constants
# GRID_WIDTH = 13  # Reduced width
# GRID_HEIGHT = 6  # Reduced height
# NUM_MINES = 4  # Reduced number of mines

# # Define colors
# COLOR_WHITE = 1
# COLOR_BLACK = 0
# COLOR_RED = 2

# CELL_SIZE = 10  # Size of each cell in pixels

# class MinesweeperGame:
#     def __init__(self):
#         self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
#         self.mines = self.place_mines()
#         self.revealed = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
#         self.game_over = False
#         self.cursor_x = 0
#         self.cursor_y = 0

#     def place_mines(self):
#         mines = set()
#         while len(mines) < NUM_MINES:
#             x = random.randint(0, GRID_WIDTH - 1)
#             y = random.randint(0, GRID_HEIGHT - 1)
#             mines.add((x, y))
#         return mines

#     def move_cursor(self, direction):
#         if direction == 'U':
#             self.cursor_y = max(0, self.cursor_y - 1)
#         elif direction == 'D':
#             self.cursor_y = min(GRID_HEIGHT - 1, self.cursor_y + 1)
#         elif direction == 'L':
#             self.cursor_x = max(0, self.cursor_x - 1)
#         elif direction == 'R':
#             self.cursor_x = min(GRID_WIDTH - 1, self.cursor_x + 1)

#     def reveal_cell(self, x=None, y=None):
#         if x is None:
#             x = self.cursor_x
#         if y is None:
#             y = self.cursor_y

#         if (x, y) in self.mines:
#             self.game_over = True
#         elif not self.revealed[y][x]:
#             self.revealed[y][x] = True
#             if self.count_adjacent_mines(x, y) == 0:
#                 for dx in range(-1, 2):
#                     for dy in range(-1, 2):
#                         new_x = x + dx
#                         new_y = y + dy
#                         if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
#                             self.reveal_cell(new_x, new_y)

#     def count_adjacent_mines(self, x, y):
#         count = sum((x + dx, y + dy) in self.mines for dx in range(-1, 2) for dy in range(-1, 2) if 0 <= x + dx < GRID_WIDTH and 0 <= y + dy < GRID_HEIGHT)
#         return count

#     def draw(self):
#         oled.fill(0)

#         for y in range(GRID_HEIGHT):
#             for x in range(GRID_WIDTH):
#                 if self.revealed[y][x]:
#                     if (x, y) in self.mines:
#                         oled.fill_rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, COLOR_RED)
#                     else:
#                         count = self.count_adjacent_mines(x, y)
#                         oled.text(str(count), x * CELL_SIZE, y * CELL_SIZE, COLOR_WHITE)
#                 else:
#                     if self.cursor_x == x and self.cursor_y == y:
#                         oled.fill_rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, COLOR_RED)
#                     else:
#                         oled.fill_rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, COLOR_BLACK)

#         oled.show()

# def app_start():
#     game = MinesweeperGame()

#     while not game.game_over:
#         if btn.U.value() == 0:
#             game.move_cursor('U')
#         elif btn.D.value() == 0:
#             game.move_cursor('D')
#         elif btn.L.value() == 0:
#             game.move_cursor('L')
#         elif btn.R.value() == 0:
#             game.move_cursor('R')
#         elif btn.A.value() == 0:
#             game.reveal_cell()

#         game.draw()
#         sleep_ms(100)  # Adjust speed here

#     # Display game over message
#     oled.fill(0)
#     oled.text("Game Over!", 28, 28, COLOR_WHITE)
#     oled.show()

#     # Wait for button B to be pressed to continue
#     while btn.B.value() != 0:
#         pass

#     # Clear the display before starting a new game
#     oled.fill(0)

# app_start()
