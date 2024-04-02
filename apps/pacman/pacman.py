from badge import oled, btn
from time import sleep_ms
from random import getrandbits, choice

# Define constants
CELL_SIZE = 4
GRID_WIDTH = 128 // CELL_SIZE
GRID_HEIGHT = (64 - 16) // CELL_SIZE  # Deducting 16 pixels for the score display and the additional line

# Define colors
COLOR_BLACK = 0
COLOR_WHITE = 1
COLOR_YELLOW = 2
COLOR_BLUE = 3
COLOR_RED = 4

# Define maze layout
maze = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#O####.#####.##.#####.####O#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "     #.##### ## #####.#     ",
    "     #.##          ##.#     ",
    "     #.## ######## ##.#     ",
    "######.## #      # ##.######",
    "      .   ##########   .     ",
    "######.## ########## ##.######",
    "     #.##          ##.#     ",
    "     #.## ######## ##.#     ",
    "     #.## ######## ##.#     ",
    "######.##          ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#O..##.......  .......##..O#",
    "###.##.##.########.##.##.###",
    "#......##.########.##......#",
    "#.########........########.#",
    "#.########.##  ##.########.#",
    "#..........##  ##..........#",
    "############################"
]

class PacmanGame:
    def __init__(self):
        self.pacman = [1, 1]
        self.direction = "RIGHT"
        self.score = 0
        self.game_over = False

        # Place pellets
        self.pellets = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == "."]

        # Place a single ghost
        self.ghost = [7, 13]

    def move_pacman(self):
        pacman_next = self.pacman.copy()

        if self.direction == "UP":
            pacman_next[1] -= 1
            if pacman_next[1] < 0:
                pacman_next[1] = GRID_HEIGHT - 1
        elif self.direction == "DOWN":
            pacman_next[1] += 1
            if pacman_next[1] >= GRID_HEIGHT:
                pacman_next[1] = 0
        elif self.direction == "LEFT":
            pacman_next[0] -= 1
            if pacman_next[0] < 0:
                pacman_next[0] = GRID_WIDTH - 1
        elif self.direction == "RIGHT":
            pacman_next[0] += 1
            if pacman_next[0] >= GRID_WIDTH:
                pacman_next[0] = 0

        # Check if pacman hits the wall
        if maze[pacman_next[1]][pacman_next[0]] == "#":
            return

        self.pacman = pacman_next

        # Check if pacman eats a pellet
        if tuple(self.pacman) in self.pellets:
            self.pellets.remove(tuple(self.pacman))
            self.score += 1

        # Check if all pellets are eaten
        if not self.pellets:
            self.game_over = True

    def move_ghost(self):
        ghost_next = self.ghost.copy()
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        direction = choice(directions)

        if direction == "UP":
            ghost_next[1] -= 1
            if ghost_next[1] < 0:
                ghost_next[1] = GRID_HEIGHT - 1
        elif direction == "DOWN":
            ghost_next[1] += 1
            if ghost_next[1] >= GRID_HEIGHT:
                ghost_next[1] = 0
        elif direction == "LEFT":
            ghost_next[0] -= 1
            if ghost_next[0] < 0:
                ghost_next[0] = GRID_WIDTH - 1
        elif direction == "RIGHT":
            ghost_next[0] += 1
            if ghost_next[0] >= GRID_WIDTH:
                ghost_next[0] = 0

        # Check if ghost hits the wall
        if maze[ghost_next[1]][ghost_next[0]] == "#":
            return

        self.ghost = ghost_next

    def check_collision(self):
        if self.pacman == self.ghost:
            self.game_over = True

    def draw(self):
        oled.fill(0)

        # Draw maze
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == "#":
                    oled.fill_rect(x * CELL_SIZE, y * CELL_SIZE + 16, CELL_SIZE, CELL_SIZE, COLOR_BLUE)

        # Draw pellets
        for pellet in self.pellets:
            oled.fill_rect(pellet[0] * CELL_SIZE + CELL_SIZE // 2 - 1, pellet[1] * CELL_SIZE + CELL_SIZE // 2 + 16 - 1, 2, 2, COLOR_WHITE)

        # Draw pacman
        oled.fill_circle(self.pacman[0] * CELL_SIZE + CELL_SIZE // 2, self.pacman[1] * CELL_SIZE + CELL_SIZE // 2 + 16, CELL_SIZE // 2, COLOR_YELLOW)

        # Draw ghost
        oled.fill_circle(self.ghost[0] * CELL_SIZE + CELL_SIZE // 2, self.ghost[1] * CELL_SIZE + CELL_SIZE // 2 + 16, CELL_SIZE // 2, COLOR_RED)

        # Draw score
        oled.text("Score: {}".format(self.score), 2, 2, COLOR_WHITE)

        oled.show()

def start_animation():
    for i in range(3):
        oled.fill(0)
        oled.text("Pacman Game", 20, 20, COLOR_WHITE)
        oled.show()
        sleep_ms(500)
        oled.fill(0)
        oled.text("Get Ready!", 30, 30, COLOR_WHITE)
        oled.show()
        sleep_ms(500)

def game_over_screen(score):
    oled.fill(0)
    oled.text("Game Over", 30, 8, COLOR_WHITE)
    oled.text("Score: {}".format(score), 30, 18, COLOR_WHITE)
    oled.text("[B] to Restart", 8, 38, COLOR_WHITE)
    oled.text("[U] to Exit", 20, 48, COLOR_WHITE)
    oled.show()

def app_start():
    start_animation()

    while True:
        game = PacmanGame()

        while not game.game_over:
            if btn.U.value() == 0 and game.direction != "DOWN":
                game.direction = "UP"
            elif btn.D.value() == 0 and game.direction != "UP":
                game.direction = "DOWN"
            elif btn.L.value() == 0 and game.direction != "RIGHT":
                game.direction = "LEFT"
            elif btn.R.value() == 0 and game.direction != "LEFT":
                game.direction = "RIGHT"

            # Check if button B is pressed to exit the game
            if btn.B.value() == 0:
                return  # Exit the game

            game.move_pacman()
            game.move_ghost()
            game.check_collision()
            game.draw()
            sleep_ms(150)  # Adjust pacman speed here

        game_over_screen(game.score)

        while True:
            if btn.B.value() == 0:
                break  # Restart game if 'B' is pressed
            elif btn.U.value() == 0:
                return  # Exit game if 'U' is pressed

app_start()
