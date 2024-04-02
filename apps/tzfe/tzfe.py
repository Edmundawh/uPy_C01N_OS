from badge import oled, btn
from time import sleep_ms
import urandom

# Define constants
MIN_CELL_SIZE = 8  # Minimum cell size to ensure visibility
MAX_CELL_SIZE = 16  # Maximum cell size to fit within the screen width
MAX_GRID_WIDTH = 128  # Maximum grid width to fit within the screen width
MAX_GRID_HEIGHT = 64  # Maximum grid height to fit within the screen height
GRID_SIZE = 4  # Initial grid size
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64

# Define colors
COLOR_BLACK = 0
COLOR_WHITE = 1

class Game2048:
    def __init__(self):
        # Adjust the grid size and cell size to fit within the screen
        self.cell_size = min(MAX_GRID_WIDTH // GRID_SIZE, MAX_CELL_SIZE)
        self.grid_width = GRID_SIZE * self.cell_size
        self.grid_height = GRID_SIZE * self.cell_size
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        # Find empty cells
        empty_cells = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if self.grid[x][y] == 0]
        if empty_cells:
            # Choose a random empty cell
            x, y = urandom.choice(empty_cells)
            # Assign either 2 or 4 to the cell with a 90%/10% chance respectively
            self.grid[x][y] = 2 if urandom.getrandbits(4) > 0 else 4

    def draw(self):
        oled.fill(0)
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                number = str(self.grid[x][y]) if self.grid[x][y] != 0 else ""
                # Adjust the x and y positions to center the grid horizontally and vertically
                x_pos = (DISPLAY_WIDTH - self.grid_width) // 2 + x * self.cell_size + (self.cell_size - len(number) * 8) // 2
                y_pos = (DISPLAY_HEIGHT - self.grid_height) // 2 + y * self.cell_size + (self.cell_size - 8) // 2
                oled.text(number, x_pos, y_pos, COLOR_WHITE)
        oled.show()

    def handle_input(self):
        if btn.U.value() == 0:
            self.move_tiles("up")
        elif btn.D.value() == 0:
            self.move_tiles("down")
        elif btn.L.value() == 0:
            self.move_tiles("left")
        elif btn.R.value() == 0:
            self.move_tiles("right")
        elif btn.B.value() == 0:
            # If button B is pressed, exit the game
            self.exit_game()

    def move_tiles(self, direction):
        dx, dy = 0, 0
        if direction == "up":
            dy = -1
        elif direction == "down":
            dy = 1
        elif direction == "left":
            dx = -1
        elif direction == "right":
            dx = 1

        # Move tiles in the specified direction
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if self.grid[x][y] != 0:
                    new_x, new_y = x + dx, y + dy
                    while 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and self.grid[new_x][new_y] == 0:
                        self.grid[new_x][new_y] = self.grid[x][y]
                        self.grid[x][y] = 0
                        x, y = new_x, new_y
                        new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and self.grid[new_x][new_y] == self.grid[x][y]:
                        self.grid[new_x][new_y] *= 2
                        self.grid[x][y] = 0
        self.add_random_tile()

    def is_game_over(self):
        # Check if the game is over (no more moves possible)
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if self.grid[x][y] == 0:
                    return False
                if (x < GRID_SIZE - 1 and self.grid[x][y] == self.grid[x + 1][y]) or \
                   (y < GRID_SIZE - 1 and self.grid[x][y] == self.grid[x][y + 1]):
                    return False
        return True

    def exit_game(self):
        # Clear the display
        oled.fill(0)
        oled.show()
        # Exit the application
        raise SystemExit

def app_start():
    game = Game2048()

    while not game.is_game_over():
        game.handle_input()
        game.draw()
        sleep_ms(100)

    # Display "Game Over!" message
    oled.fill(0)
    oled.text("Game Over!", 30, 28, COLOR_WHITE)
    oled.show()

    # Wait for button B to be pressed to exit the game
    while btn.B.value():
        pass  # Wait for button B to be pressed

    # Clear the display
    oled.fill(0)
    oled.show()

app_start()

# from badge import oled, btn
# from time import sleep_ms
# import urandom

# # Define constants
# MIN_CELL_SIZE = 8  # Minimum cell size to ensure visibility
# MAX_CELL_SIZE = 16  # Maximum cell size to fit within the screen width
# MAX_GRID_WIDTH = 128  # Maximum grid width to fit within the screen width
# MAX_GRID_HEIGHT = 64  # Maximum grid height to fit within the screen height
# GRID_SIZE = 4  # Initial grid size
# DISPLAY_WIDTH = 128
# DISPLAY_HEIGHT = 64

# # Define colors
# COLOR_BLACK = 0
# COLOR_WHITE = 1

# class Game2048:
#     def __init__(self):
#         # Adjust the grid size and cell size to fit within the screen
#         self.cell_size = min(MAX_GRID_WIDTH // GRID_SIZE, MAX_CELL_SIZE)
#         self.grid_width = GRID_SIZE * self.cell_size
#         self.grid_height = GRID_SIZE * self.cell_size
#         self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
#         self.add_random_tile()
#         self.add_random_tile()

#     def add_random_tile(self):
#         # Find empty cells
#         empty_cells = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if self.grid[x][y] == 0]
#         if empty_cells:
#             # Choose a random empty cell
#             x, y = urandom.choice(empty_cells)
#             # Assign either 2 or 4 to the cell with a 90%/10% chance respectively
#             self.grid[x][y] = 2 if urandom.getrandbits(4) > 0 else 4

#     def draw(self):
#         oled.fill(0)
#         for x in range(GRID_SIZE):
#             for y in range(GRID_SIZE):
#                 number = str(self.grid[x][y]) if self.grid[x][y] != 0 else ""
#                 # Adjust the x and y positions to center the grid horizontally and vertically
#                 x_pos = (DISPLAY_WIDTH - self.grid_width) // 2 + x * self.cell_size + (self.cell_size - len(number) * 8) // 2
#                 y_pos = (DISPLAY_HEIGHT - self.grid_height) // 2 + y * self.cell_size + (self.cell_size - 8) // 2
#                 oled.text(number, x_pos, y_pos, COLOR_WHITE)
#         oled.show()

#     def handle_input(self):
#         if btn.U.value() == 0:
#             self.move_tiles("up")
#         elif btn.D.value() == 0:
#             self.move_tiles("down")
#         elif btn.L.value() == 0:
#             self.move_tiles("left")
#         elif btn.R.value() == 0:
#             self.move_tiles("right")

#     def move_tiles(self, direction):
#         dx, dy = 0, 0
#         if direction == "up":
#             dy = -1
#         elif direction == "down":
#             dy = 1
#         elif direction == "left":
#             dx = -1
#         elif direction == "right":
#             dx = 1

#         # Move tiles in the specified direction
#         for x in range(GRID_SIZE):
#             for y in range(GRID_SIZE):
#                 if self.grid[x][y] != 0:
#                     new_x, new_y = x + dx, y + dy
#                     while 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and self.grid[new_x][new_y] == 0:
#                         self.grid[new_x][new_y] = self.grid[x][y]
#                         self.grid[x][y] = 0
#                         x, y = new_x, new_y
#                         new_x, new_y = x + dx, y + dy
#                     if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and self.grid[new_x][new_y] == self.grid[x][y]:
#                         self.grid[new_x][new_y] *= 2
#                         self.grid[x][y] = 0
#         self.add_random_tile()

#     def is_game_over(self):
#         # Check if the game is over (no more moves possible)
#         for x in range(GRID_SIZE):
#             for y in range(GRID_SIZE):
#                 if self.grid[x][y] == 0:
#                     return False
#                 if (x < GRID_SIZE - 1 and self.grid[x][y] == self.grid[x + 1][y]) or \
#                    (y < GRID_SIZE - 1 and self.grid[x][y] == self.grid[x][y + 1]):
#                     return False
#         return True

# def app_start():
#     game = Game2048()

#     while not game.is_game_over():
#         game.handle_input()
#         game.draw()
#         sleep_ms(100)

#     # Display "Game Over!" message
#     oled.fill(0)
#     oled.text("Game Over!", 30, 28, COLOR_WHITE)
#     oled.show()

#     # Wait for button B to be pressed to exit the game
#     while btn.B.value():
#         pass  # Wait for button B to be pressed

#     # Clear the display
#     oled.fill(0)
#     oled.show()

# app_start()