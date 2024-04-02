from badge import oled, btn
from time import sleep_ms
from random import getrandbits

# Define constants
CELL_SIZE = 4
GRID_WIDTH = 128 // CELL_SIZE
GRID_HEIGHT = (64 - 16) // CELL_SIZE  # Deducting 16 pixels for the score display and the additional line

# Define colors
COLOR_BLACK = 0
COLOR_WHITE = 1

class SnakeGame:
    def __init__(self):
        self.snake = [[10, 10]]
        self.food = self.generate_food()
        self.direction = "RIGHT"
        self.score = 0
        self.game_over = False

    def generate_food(self):
        return [getrandbits(7) % GRID_WIDTH, getrandbits(6) % GRID_HEIGHT]

    def move(self):
        head = self.snake[0].copy()

        if self.direction == "UP":
            head[1] -= 1
        elif self.direction == "DOWN":
            head[1] += 1
        elif self.direction == "LEFT":
            head[0] -= 1
        elif self.direction == "RIGHT":
            head[0] += 1

        # Check if snake hits the wall or itself
        if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT or head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, head)

        # Check if snake eats food
        if head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def draw(self):
        oled.fill(0)

        # Draw food
        oled.fill_rect(self.food[0] * CELL_SIZE, self.food[1] * CELL_SIZE + 16, CELL_SIZE, CELL_SIZE, COLOR_WHITE)

        # Draw snake
        for segment in self.snake:
            oled.fill_rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE + 16, CELL_SIZE, CELL_SIZE, COLOR_WHITE)

        # Draw score
        oled.text("Score: {}".format(self.score), 2, 2, COLOR_WHITE)

        # Draw line
        oled.hline(0, 64, 128, COLOR_WHITE)

        oled.show()

def app_start():
    while True:
        game = SnakeGame()

        while not game.game_over:
            if btn.U.value() == 0 and game.direction != "DOWN":
                game.direction = "UP"
            elif btn.D.value() == 0 and game.direction != "UP":
                game.direction = "DOWN"
            elif btn.L.value() == 0 and game.direction != "RIGHT":
                game.direction = "LEFT"
            elif btn.R.value() == 0 and game.direction != "LEFT":
                game.direction = "RIGHT"

            game.move()
            game.draw()
            sleep_ms(150)  # Adjust snake speed here

        # Display "Game Over" and "Score" until 'B' or 'A' button is pressed
        while True:
            oled.fill(0)
            oled.text("Game Over", 30, 8, COLOR_WHITE)  # Adjusted position
            oled.text("Score: {}".format(game.score), 30, 18, COLOR_WHITE)  # Adjusted position
            oled.text("[B] to Restart", 8, 38, COLOR_WHITE)
            oled.text("[U] to Exit", 20, 48, COLOR_WHITE)
            oled.show()

            if btn.B.value() == 0:
                break  # Restart game if 'B' is pressed
            elif btn.U.value() == 0:
                return  # Exit game if 'U' is pressed

app_start()







