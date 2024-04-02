from badge import oled, btn
from time import sleep_ms

# Define constants
CELL_SIZE = 10
GRID_WIDTH = 7
GRID_HEIGHT = 6
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64

# Define shapes
SHAPE_EMPTY = 0
SHAPE_CROSS = 1
SHAPE_CIRCLE = 2

class ConnectFourGame:
    def __init__(self):
        self.grid = [[SHAPE_EMPTY for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_player = SHAPE_CROSS
        self.selected_column = 0

    def draw(self):
        oled.fill(0)

        # Draw grid lines
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                oled.rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE, 1)

        # Draw discs
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                if self.grid[j][i] == SHAPE_CROSS:
                    draw_cross(i, j)
                elif self.grid[j][i] == SHAPE_CIRCLE:
                    draw_circle(i, j)

        # Draw arrow indicating the column where the next piece will be dropped
        arrow_x = self.selected_column * CELL_SIZE + CELL_SIZE // 2
        arrow_y = GRID_HEIGHT * CELL_SIZE
        oled.text('^', arrow_x, arrow_y, 1)

        oled.show()

    def handle_input(self):
        if btn.L.value() == 0:
            if self.selected_column > 0:
                self.selected_column -= 1
        elif btn.R.value() == 0:
            if self.selected_column < GRID_WIDTH - 1:
                self.selected_column += 1
        elif btn.A.value() == 0:
            self.drop_disc()

    def drop_disc(self):
        for row in range(GRID_HEIGHT - 1, -1, -1):
            if self.grid[row][self.selected_column] == SHAPE_EMPTY:
                self.grid[row][self.selected_column] = self.current_player
                self.current_player = SHAPE_CIRCLE if self.current_player == SHAPE_CROSS else SHAPE_CROSS
                break

    def check_winner(self):
        # Check horizontally
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH - 3):
                if self.grid[row][col] == self.grid[row][col + 1] == self.grid[row][col + 2] == self.grid[row][col + 3] != SHAPE_EMPTY:
                    return self.grid[row][col]

        # Check vertically
        for row in range(GRID_HEIGHT - 3):
            for col in range(GRID_WIDTH):
                if self.grid[row][col] == self.grid[row + 1][col] == self.grid[row + 2][col] == self.grid[row + 3][col] != SHAPE_EMPTY:
                    return self.grid[row][col]

        # Check diagonally (positive slope)
        for row in range(GRID_HEIGHT - 3):
            for col in range(GRID_WIDTH - 3):
                if self.grid[row][col] == self.grid[row + 1][col + 1] == self.grid[row + 2][col + 2] == self.grid[row + 3][col + 3] != SHAPE_EMPTY:
                    return self.grid[row][col]

        # Check diagonally (negative slope)
        for row in range(3, GRID_HEIGHT):
            for col in range(GRID_WIDTH - 3):
                if self.grid[row][col] == self.grid[row - 1][col + 1] == self.grid[row - 2][col + 2] == self.grid[row - 3][col + 3] != SHAPE_EMPTY:
                    return self.grid[row][col]

        # No winner
        return SHAPE_EMPTY

def draw_cross(col, row):
    x = col * CELL_SIZE
    y = row * CELL_SIZE
    oled.line(x + 2, y + 2, x + CELL_SIZE - 2, y + CELL_SIZE - 2, 1)
    oled.line(x + CELL_SIZE - 2, y + 2, x + 2, y + CELL_SIZE - 2, 1)

def draw_circle(col, row):
    x_center = col * CELL_SIZE + CELL_SIZE // 2
    y_center = row * CELL_SIZE + CELL_SIZE // 2
    radius = CELL_SIZE // 2 - 2
    oled.circle(x_center, y_center, radius, 1)

def app_start():
    game = ConnectFourGame()

    while True:
        game.handle_input()
        game.draw()
        winner = game.check_winner()
        if winner != SHAPE_EMPTY:
            oled.fill(0)
            if winner == SHAPE_CROSS:
                oled.text("Cross Wins!", 20, 28, 1)
            else:
                oled.text("Circle Wins!", 20, 28, 1)
            oled.show()
            break
        sleep_ms(100)

    while True:
        if btn.B.value() == 0:
            return

app_start()
