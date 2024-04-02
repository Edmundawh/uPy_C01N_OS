from badge import oled, btn
from time import sleep_ms
from random import getrandbits

# Define constants
BIRD_X = 20  # Initial x-coordinate of the bird
BIRD_SIZE = 4  # Size of the bird sprite
GRAVITY = 0.5  # Gravity constant
FLAP_STRENGTH = -4.0  # Strength of the bird's flap
PIPE_WIDTH = 8
GAP_HEIGHT = 16  # Gap between pipes
PIPE_SPEED = 1  # Speed at which pipes move to the left

class FlappyBirdGame:
    def __init__(self):
        self.bird_y = 30  # Initial y-coordinate of the bird
        self.pipe_x = 128  # Initial x-coordinate of the pipes
        self.pipe_gap_y = 0  # Initial y-coordinate of the gap between pipes
        self.score = 0
        self.game_over = False

    def flap(self):
        self.bird_y += FLAP_STRENGTH

    def move_pipes(self):
        self.pipe_x -= PIPE_SPEED
        if self.pipe_x < -PIPE_WIDTH:
            self.pipe_x = 128
            self.pipe_gap_y = getrandbits(6) % (64 - GAP_HEIGHT)

    def check_collision(self):
        # Check if bird hits ground or ceiling
        if self.bird_y < 0 or self.bird_y + BIRD_SIZE > 64:
            self.game_over = True
            return

        # Check if bird hits pipe
        if (BIRD_X + BIRD_SIZE > self.pipe_x and BIRD_X < self.pipe_x + PIPE_WIDTH) and \
           (self.bird_y < self.pipe_gap_y or self.bird_y + BIRD_SIZE > self.pipe_gap_y + GAP_HEIGHT):
            self.game_over = True
            return

        # Check if bird passes through pipe
        if BIRD_X == self.pipe_x + PIPE_WIDTH:
            self.score += 1

    def draw(self):
        oled.fill(0)

        # Draw bird
        oled.fill_rect(BIRD_X, int(self.bird_y), BIRD_SIZE, BIRD_SIZE, 1)

        # Draw pipes
        oled.fill_rect(int(self.pipe_x), 0, PIPE_WIDTH, self.pipe_gap_y, 1)
        oled.fill_rect(int(self.pipe_x), self.pipe_gap_y + GAP_HEIGHT, PIPE_WIDTH, 64 - self.pipe_gap_y - GAP_HEIGHT, 1)

        # Draw score
        oled.text("Score: {}".format(self.score), 2, 2, 1)

        oled.show()

def show_starting_animation():
    text_x = 128
    while True:
        # Clear the display and draw the background animation
        oled.fill(0)
        # Draw "Flappy Bird" text moving from right to left
        oled.text(" Let's Play", text_x, 8, 10)
        oled.text("Flappy Bird!", text_x,18, 1)
        oled.text("[A] to Flap", 18, 38, 1)
        oled.show()

        # Update text position for next frame
        text_x -= 1
        if text_x <= -85:  # Width of "Flappy Bird" text is approximately 85 pixels
            text_x = 128

        # Delay for smooth animation
        sleep_ms(50)

        # Check for button press to exit animation and start the game
        if btn.A.value() == 0:
            return

        # Check for button press to exit animation and exit the game
        if btn.U.value() == 0:
            return True


def app_start():
    while True:
        if show_starting_animation():
            return  # Exit the application if button U is pressed during animation

        game = FlappyBirdGame()

        while not game.game_over:
            game.bird_y += GRAVITY  # Apply gravity
            game.move_pipes()
            game.check_collision()
            game.draw()
            sleep_ms(50)  # Adjust game speed here

            if btn.U.value() == 0:
                return  # Exit the game if 'U' button is pressed during gameplay

            if btn.A.value() == 0:
                game.flap()  # Flap when button 'A' is pressed

        # Display "Game Over" and "Score" until 'B' or 'U' button is pressed
        while True:
            oled.fill(0)
            oled.text("Game Over", 30, 8, 1)
            oled.text("Score: {}".format(game.score), 30, 18, 1)
            oled.text("[B] to Restart", 8, 38, 1)
            oled.text("[U] to Exit", 20, 48, 1)
            oled.show()

            if btn.B.value() == 0:
                break
            elif btn.U.value() == 0:
                return

            sleep_ms(100)  # Add a small delay to avoid multiple button presses

app_start()


