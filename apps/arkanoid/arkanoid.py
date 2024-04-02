from badge import oled, btn
from time import sleep_ms
from random import randint, choice

# Define constants
PADDLE_MIN_WIDTH = 10
PADDLE_MAX_WIDTH = 40
PADDLE_HEIGHT = 2
PADDLE_SPEED = 2
BALL_SIZE = 2
GRID_WIDTH = 128
GRID_HEIGHT = 64
COLOR_BLACK = 0
COLOR_WHITE = 1

# Define block types with different colors
BLOCK_COLORS = [1, 2, 3]  # You can add more colors if needed

class ArkanoidGame:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.paddle_width = GRID_WIDTH // 2
        self.paddle_x = self.paddle_width // 2
        self.ball_count = 1
        self.balls = [{'x': GRID_WIDTH // 2, 'y': GRID_HEIGHT // 2, 'dx': 1 if randint(0, 1) == 0 else -1, 'dy': -1} for _ in range(self.ball_count)]
        self.bricks = self.create_bricks()
        self.game_over = False

    def create_bricks(self):
        bricks = []
        brick_width = GRID_WIDTH // 10
        brick_height = 6
        for y in range(3 + self.level):  # Increase the number of rows based on the level
            for x in range(10):
                bricks.append([x * brick_width, y * brick_height, choice(BLOCK_COLORS)])
        return bricks

    def move_paddle(self, direction):
        if direction == "LEFT":
            self.paddle_x = max(0, self.paddle_x - PADDLE_SPEED)
        elif direction == "RIGHT":
            self.paddle_x = min(GRID_WIDTH - self.paddle_width, self.paddle_x + PADDLE_SPEED)

    def move_ball(self, ball):
        ball['x'] += ball['dx']
        ball['y'] += ball['dy']

        # Ball collision with walls
        if ball['x'] <= 0 or ball['x'] >= GRID_WIDTH - BALL_SIZE:
            ball['dx'] *= -1
        if ball['y'] <= 0:
            ball['dy'] *= -1

        # Ball collision with paddle
        if (ball['y'] + BALL_SIZE >= GRID_HEIGHT - PADDLE_HEIGHT and
                self.paddle_x <= ball['x'] <= self.paddle_x + self.paddle_width):
            ball['dy'] *= -1

        # Ball collision with bricks
        for brick in self.bricks:
            if (brick[0] <= ball['x'] <= brick[0] + GRID_WIDTH // 10 and
                    brick[1] <= ball['y'] <= brick[1] + 6):
                self.bricks.remove(brick)
                ball['dy'] *= -1
                self.score += 1
                break

        # Check if all bricks are cleared
        if not self.bricks:
            self.level += 1
            self.bricks = self.create_bricks()
            self.ball_count += 1
            self.balls = [{'x': GRID_WIDTH // 2, 'y': GRID_HEIGHT // 2, 'dx': 1 if randint(0, 1) == 0 else -1, 'dy': -1} for _ in range(self.ball_count)]
            self.apply_powerup()  # Apply powerup when level changes

        # Check if ball missed the paddle
        if ball['y'] >= GRID_HEIGHT:
            self.balls.remove(ball)
            if not self.balls:
                self.game_over = True

    def apply_powerup(self):
        # Randomly adjust paddle width within specified range
        self.paddle_width = randint(PADDLE_MIN_WIDTH, PADDLE_MAX_WIDTH)

    def draw(self):
        oled.fill(0)

        # Draw paddle
        oled.fill_rect(self.paddle_x, GRID_HEIGHT - PADDLE_HEIGHT, self.paddle_width, PADDLE_HEIGHT, COLOR_WHITE)

        # Draw balls
        for ball in self.balls:
            oled.fill_rect(ball['x'], ball['y'], BALL_SIZE, BALL_SIZE, COLOR_WHITE)

        # Draw bricks
        for brick in self.bricks:
            oled.fill_rect(brick[0], brick[1], GRID_WIDTH // 10, 6, brick[2])

        # Draw score and level with smaller font
        oled.text("Lv:{}".format(self.level), 2, 2, COLOR_WHITE)
        oled.text("Scr:{}".format(self.score), 60, 2, COLOR_WHITE)

        oled.show()

def show_starting_animation():
    # Initial position and velocity of the ball
    ball_x = GRID_WIDTH // 2
    ball_y = GRID_HEIGHT // 3
    vel_x = 1
    vel_y = 1

    # Animation loop
    while True:
        # Update ball position
        ball_x += vel_x
        ball_y += vel_y

        # Bounce the ball off the edges
        if ball_x <= 0 or ball_x >= GRID_WIDTH - BALL_SIZE:
            vel_x = -vel_x
        if ball_y <= 0 or ball_y >= GRID_HEIGHT - BALL_SIZE:
            vel_y = -vel_y

        # Clear the display and draw the ball
        oled.fill(COLOR_BLACK)
        oled.fill_rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE, COLOR_WHITE)
        oled.text("Welcome to", 25, 18, COLOR_WHITE)
        oled.text("Arkanoid!", 30, 28, COLOR_WHITE)
        oled.text("[A] to Start", 20, 38, COLOR_WHITE)
        oled.show()

        # Delay for smooth animation
        sleep_ms(50)

        # Check for button press to exit animation and start the game
        if btn.A.value() == 0:
            break

        # Check for button press to exit animation and exit the game
        if btn.U.value() == 0:
            return True

def app_start():
    while True:
        if show_starting_animation():
            return  # Exit the application if button U is pressed during animation
        # Start the Arkanoid game after the animation
        if game_start():
            break  # Exit the loop if game_start() returns True
        sleep_ms(100)  # Add a small delay to avoid multiple button presses

def game_start():
    # Initialize the game
    game = ArkanoidGame()

    # Main game loop
    while not game.game_over:
        if btn.L.value() == 0:
            game.move_paddle("LEFT")
        elif btn.R.value() == 0:
            game.move_paddle("RIGHT")

        for ball in game.balls:
            game.move_ball(ball)

        game.draw()
        sleep_ms(50)  # Adjust ball speed here

        # Check if button U is pressed during the game
        if btn.U.value() == 0:
            return True  # Exit game immediately if 'U' is pressed

    # Display "Game Over" and "Score" until 'B' button is pressed
    while True:
        oled.fill(0)
        oled.text("Game Over", 30, 8, COLOR_WHITE)
        oled.text("Score: {}".format(game.score), 30, 18, COLOR_WHITE)
        oled.text("[B] to Restart", 8, 38, COLOR_WHITE)
        oled.text("[U] to Exit", 20, 48, COLOR_WHITE)
        oled.show()

        # Check if button U is pressed to exit the game
        if btn.U.value() == 0:
            return True

        # Check if button B is pressed to restart the game
        if btn.B.value() == 0:
            return False

        sleep_ms(100)  # Add a small delay to avoid multiple button presses

app_start()

