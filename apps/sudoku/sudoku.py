from badge import oled, btn
from time import sleep_ms
import random

# Define constants
CELL_SIZE = 12
GRID_SIZE = 9
GRID_WIDTH = GRID_SIZE * CELL_SIZE
GRID_HEIGHT = GRID_SIZE * CELL_SIZE
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64

# Define colors
COLOR_BLACK = 0
COLOR_WHITE = 1

class SudokuGame:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.generate_puzzle()
        self.selected_cell = [0, 0]
        self.selected_number = 1  # Initial selected number
        self.scroll_offset = [0, 0]

    def generate_puzzle(self):
        # Initialize a partially filled grid (for demonstration purposes)
        self.grids = [
            [[5, 3, 0, 0, 7, 0, 0, 0, 0],
             [6, 0, 0, 1, 9, 5, 0, 0, 0],
             [0, 9, 8, 0, 0, 0, 0, 6, 0],
             [8, 0, 0, 0, 6, 0, 0, 0, 3],
             [4, 0, 0, 8, 0, 3, 0, 0, 1],
             [7, 0, 0, 0, 2, 0, 0, 0, 6],
             [0, 6, 0, 0, 0, 0, 2, 8, 0],
             [0, 0, 0, 4, 1, 9, 0, 0, 5],
             [0, 0, 0, 0, 8, 0, 0, 7, 9]],

            [[0, 2, 0, 0, 7, 0, 0, 0, 0],
             [6, 0, 0, 1, 0, 5, 0, 0, 0],
             [0, 0, 8, 0, 0, 0, 0, 6, 0],
             [8, 0, 0, 0, 6, 0, 0, 0, 3],
             [4, 0, 0, 8, 0, 3, 0, 0, 1],
             [7, 0, 0, 0, 2, 0, 0, 0, 6],
             [0, 6, 0, 0, 0, 0, 2, 8, 0],
             [0, 0, 0, 4, 1, 9, 0, 0, 5],
             [0, 0, 0, 0, 8, 0, 0, 7, 9]],

            [[8, 0, 4, 0, 2, 0, 1, 0, 6],
             [0, 0, 0, 0, 0, 0, 0, 8, 0],
             [5, 0, 0, 0, 0, 7, 0, 0, 0],
             [0, 6, 0, 2, 0, 0, 0, 0, 0],
             [0, 0, 1, 0, 6, 0, 3, 0, 4],
             [0, 0, 0, 0, 0, 0, 0, 0, 9],
             [4, 0, 0, 5, 0, 0, 8, 0, 3],
             [0, 0, 0, 0, 3, 0, 0, 9, 0],
             [0, 0, 8, 0, 0, 0, 0, 2, 0]],
        ]

        #choose random grid
        self.grid = random.choice(self.grids)
        
    def draw(self):
        oled.fill(0)

        # Determine the visible range of cells
        start_x = max(0, self.selected_cell[0] - DISPLAY_WIDTH // CELL_SIZE // 2)
        start_y = max(0, self.selected_cell[1] - DISPLAY_HEIGHT // CELL_SIZE // 2)
        end_x = min(GRID_SIZE, start_x + DISPLAY_WIDTH // CELL_SIZE)
        end_y = min(GRID_SIZE, start_y + DISPLAY_HEIGHT // CELL_SIZE)

        # Draw grid lines within the 3x3 grid
        for i in range(start_x // 3 * 3, (end_x + 2) // 3 * 3, 3):
            for j in range(start_y // 3 * 3, (end_y + 2) // 3 * 3, 3):
                oled.rect((i - start_x) * CELL_SIZE - self.scroll_offset[0], 
                          (j - start_y) * CELL_SIZE - self.scroll_offset[1], 
                          3 * CELL_SIZE, 3 * CELL_SIZE, COLOR_WHITE)

        # Draw numbers
        for i in range(start_x, end_x):
            for j in range(start_y, end_y):
                number = str(self.grid[i][j]) if self.grid[i][j] != 0 else ""
                x = (i - start_x) * CELL_SIZE - self.scroll_offset[0] + 4
                y = (j - start_y) * CELL_SIZE - self.scroll_offset[1] + 4
                oled.text(number, x, y, COLOR_WHITE)
                
                # Display selected number in the selected cell
                if [i, j] == self.selected_cell:
                    oled.text(str(self.selected_number), x, y, COLOR_WHITE)

        # Highlight selected cell
        x = (self.selected_cell[0] - start_x) * CELL_SIZE - self.scroll_offset[0]
        y = (self.selected_cell[1] - start_y) * CELL_SIZE - self.scroll_offset[1]
        oled.rect(x, y, CELL_SIZE, CELL_SIZE, COLOR_WHITE)

        oled.show()

    def handle_input(self):
        # Record the initial selected cell position for comparison
        initial_selected_cell = self.selected_cell.copy()

        if btn.U.value() == 0:
            if self.selected_cell[1] > 0:
                self.selected_cell[1] -= 1
                if self.selected_cell[1] < self.scroll_offset[1] // CELL_SIZE:
                    self.scroll_offset[1] -= CELL_SIZE
        elif btn.D.value() == 0:
            if self.selected_cell[1] < GRID_SIZE - 1:
                self.selected_cell[1] += 1
                if self.selected_cell[1] >= (self.scroll_offset[1] + DISPLAY_HEIGHT // CELL_SIZE):
                    self.scroll_offset[1] += CELL_SIZE
        elif btn.L.value() == 0:
            if self.selected_cell[0] > 0:
                self.selected_cell[0] -= 1
                if self.selected_cell[0] < self.scroll_offset[0] // CELL_SIZE:
                    self.scroll_offset[0] -= CELL_SIZE
        elif btn.R.value() == 0:
            if self.selected_cell[0] < GRID_SIZE - 1:
                self.selected_cell[0] += 1
                if self.selected_cell[0] >= (self.scroll_offset[0] + DISPLAY_WIDTH // CELL_SIZE):
                    self.scroll_offset[0] += CELL_SIZE
        elif btn.A.value() == 0:  # Clear or enter number into the cell
            self.enter_number()
        elif btn.B.value() == 0:  # Cycle through numbers
            self.selected_number = (self.selected_number % 9) + 1

        # Check if the selected cell position has changed
        if initial_selected_cell != self.selected_cell:
            # Ensure the scroll offset does not go beyond the board boundaries
            self.scroll_offset[0] = min(max(0, self.scroll_offset[0]), GRID_WIDTH - DISPLAY_WIDTH)
            self.scroll_offset[1] = min(max(0, self.scroll_offset[1]), GRID_HEIGHT - DISPLAY_HEIGHT)

    def enter_number(self):
        cell_value = self.grid[self.selected_cell[0]][self.selected_cell[1]]
        # If the selected cell is empty, enter the selected number into the cell
        if cell_value == 0:
            # If the number is valid (no conflicts), update the grid
            if self.is_valid_move(self.selected_number, self.selected_cell[0], self.selected_cell[1]):
                self.grid[self.selected_cell[0]][self.selected_cell[1]] = self.selected_number
        # If the selected cell is occupied, clear it
        else:
            self.grid[self.selected_cell[0]][self.selected_cell[1]] = 0

    def is_valid_move(self, number, row, col):
        # Check if placing 'number' at (row, col) violates Sudoku rules
        # 1. Check row
        for i in range(GRID_SIZE):
            if self.grid[i][col] == number:
                return False

        # 2. Check column
        for j in range(GRID_SIZE):
            if self.grid[row][j] == number:
                return False

        # 3. Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.grid[i][j] == number:
                    return False

        return True

    def is_game_over(self):
        # Check if the game is over (i.e., the grid is completely filled)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    return False
        return True

def app_start():
    game = SudokuGame()

    while not game.is_game_over():
        game.handle_input()
        game.draw()
        sleep_ms(100)

    oled.fill(0)
    oled.text("Game Over!", 30, 28, COLOR_WHITE)
    oled.show()

    while True:
        if btn.B.value()==0:
            return

app_start()