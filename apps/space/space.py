from badge import oled, btn
from time import sleep_ms
from random import randint, choice

# Define constants
CELL_SIZE = 6  # Increased cell size for bigger enemies
GRID_WIDTH = 128 // CELL_SIZE
GRID_HEIGHT = (64 - 16) // CELL_SIZE  # Deducting 16 pixels for the score display and the additional line
PLAYER_X = 1  # X-coordinate for the player's spaceship

# Define colors
COLOR_BLACK = 0
COLOR_WHITE = 1

class SpaceInvaders:
    def __init__(self):
        self.player_y = GRID_HEIGHT // 2  # Starting position of the player's spaceship
        self.obstacles = []  # Initial obstacles
        self.bullets = []  # Bullets fired by obstacles
        self.enemy_bullets = []  # Bullets fired by enemies
        self.score = 0
        self.game_over = False

    def move_player(self, direction):
        if direction == "UP" and self.player_y > 0:
            self.player_y -= 1
        elif direction == "DOWN" and self.player_y < GRID_HEIGHT - 1:
            self.player_y += 1

    def move_obstacles(self):
        for obstacle in self.obstacles:
            obstacle[0] -= 1
            if obstacle[0] <= 0:
                self.obstacles.remove(obstacle)

        # Generate new obstacles randomly
        if randint(0, 10) > 8:
            self.obstacles.append([GRID_WIDTH - 1, randint(0, GRID_HEIGHT - 1)])

    def move_bullets(self):
        for bullet in self.bullets:
            bullet[0] += 1
            if bullet[0] >= GRID_WIDTH:
                self.bullets.remove(bullet)
            elif bullet in self.obstacles:  # If bullet hits an obstacle
                self.obstacles.remove(bullet)
                self.score += 1

        for bullet in self.enemy_bullets:
            bullet[0] -= 1
            if bullet[0] <= PLAYER_X + 1:
                if bullet[1] == self.player_y:
                    self.game_over = True

    def draw(self):
        oled.fill(0)

        # Draw player's spaceship
        oled.fill_rect(PLAYER_X * CELL_SIZE, self.player_y * CELL_SIZE + 16, CELL_SIZE, CELL_SIZE, COLOR_WHITE)

        # Draw obstacles (enemies)
        for obstacle in self.obstacles:
            oled.fill_rect(obstacle[0] * CELL_SIZE, obstacle[1] * CELL_SIZE + 16, CELL_SIZE, CELL_SIZE, COLOR_WHITE)

        # Draw bullets
        for bullet in self.bullets:
            oled.fill_rect(bullet[0] * CELL_SIZE, bullet[1] * CELL_SIZE + 16, CELL_SIZE, CELL_SIZE, COLOR_WHITE)

        for bullet in self.enemy_bullets:
            oled.fill_rect(bullet[0] * CELL_SIZE, bullet[1] * CELL_SIZE + 16, CELL_SIZE, CELL_SIZE, COLOR_WHITE)

        # Draw score
        oled.text("Score: {}".format(self.score), 2, 2, COLOR_WHITE)

        # Draw line
        oled.hline(0, 64, 128, COLOR_WHITE)

        oled.show()

def app_start():
    while True:
        game = SpaceInvaders()

        while not game.game_over:
            if btn.B.value() == 0:
                return  # Exit game if 'B' is pressed
            elif btn.U.value() == 0:
                game.move_player("UP")
            elif btn.D.value() == 0:
                game.move_player("DOWN")
            elif btn.A.value() == 0:
                game.bullets.append([PLAYER_X + 1, game.player_y])  # Fire bullet when 'A' is pressed

            game.move_obstacles()  # Generate new obstacles
            game.move_bullets()
            game.draw()
            sleep_ms(150)  # Adjust game speed here

            # Check collision with obstacles
            for obstacle in game.obstacles:
                if obstacle[0] <= PLAYER_X + 1:
                    if obstacle[1] == game.player_y:
                        game.game_over = True

            # Enemy bullet firing mechanism
            if randint(0, 10) > 8:
                for obstacle in game.obstacles:
                    if obstacle[0] == GRID_WIDTH - 1:
                        game.enemy_bullets.append([obstacle[0], obstacle[1]])

        # Display "Game Over" and "Score" until 'B' or 'A' button is pressed
        while True:
            oled.fill(0)
            oled.text("Game Over", 30, 8, COLOR_WHITE)  # Adjusted position
            oled.text("Score: {}".format(game.score), 30, 18, COLOR_WHITE)  # Adjusted position
            oled.text("[B] to Exit", 20, 48, COLOR_WHITE)
            oled.show()

            if btn.B.value() == 0:
                return  # Exit game if 'B' is pressed

app_start()

# from badge import oled, btn
# from time import sleep_ms
# from random import randint, choice

# # Define constants
# CELL_SIZE = 6  # Increased cell size for bigger enemies
# GRID_WIDTH = 128 // CELL_SIZE
# GRID_HEIGHT = (64 - 16) // CELL_SIZE  # Deducting 16 pixels for the score display and the additional line
# PLAYER_X = 1  # X-coordinate for the player's spaceship

# # Define colors
# COLOR_BLACK = 0
# COLOR_WHITE = 1

# class SpaceInvaders:
#     def __init__(self):
#         self.player_y = GRID_HEIGHT // 2  # Starting position of the player's spaceship
#         self.obstacles = []  # Initial obstacles
#         self.bullets = []  # Bullets fired by obstacles
#         self.score = 0
#         self.game_over = False

#     def move_player(self, direction):
#         if direction == "UP" and self.player_y > 0:
#             self.player_y -= 1
#         elif direction == "DOWN" and self.player_y < GRID_HEIGHT - 1:
#             self.player_y += 1

#     def move_obstacles(self):
#         for obstacle in self.obstacles:
#             obstacle[0] -= 1
#             if obstacle[0] <= 0:
#                 self.obstacles.remove(obstacle)

#         # Generate new obstacles randomly
#         if randint(0, 10) > 8:
#             self.obstacles.append([GRID_WIDTH - 1, randint(0, GRID_HEIGHT - 1)])

#     def move_bullets(self):
#         for bullet in self.bullets:
#             bullet[0] += 1
#             if bullet[0] >= GRID_WIDTH:
#                 self.bullets.remove(bullet)
#             elif bullet in self.obstacles:  # If bullet hits an obstacle
#                 self.obstacles.remove(bullet)
#                 self.score += 1

#     def draw(self):
#         oled.fill(0)

#         # Draw player's spaceship
#         oled.fill_rect(PLAYER_X * CELL_SIZE, self.player_y * CELL_SIZE + 16, CELL_SIZE, CELL_SIZE, COLOR_WHITE)

#         # Draw obstacles (enemies)
#         for obstacle in self.obstacles:
#             oled.fill_rect(obstacle[0] * CELL_SIZE, obstacle[1] * CELL_SIZE + 16, CELL_SIZE, CELL_SIZE, COLOR_WHITE)

#         # Draw bullets
#         for bullet in self.bullets:
#             oled.fill_rect(bullet[0] * CELL_SIZE, bullet[1] * CELL_SIZE + 16, CELL_SIZE, CELL_SIZE, COLOR_WHITE)

#         # Draw score
#         oled.text("Score: {}".format(self.score), 2, 2, COLOR_WHITE)

#         # Draw line
#         oled.hline(0, 64, 128, COLOR_WHITE)

#         oled.show()

# def app_start():
#     while True:
#         game = SpaceInvaders()

#         while not game.game_over:
#             if btn.B.value() == 0:
#                 return  # Exit game if 'B' is pressed
#             elif btn.U.value() == 0:
#                 game.move_player("UP")
#             elif btn.D.value() == 0:
#                 game.move_player("DOWN")
#             elif btn.A.value() == 0:
#                 game.bullets.append([PLAYER_X + 1, game.player_y])  # Fire bullet when 'A' is pressed

#             game.move_obstacles()  # Generate new obstacles
#             game.move_bullets()
#             game.draw()
#             sleep_ms(150)  # Adjust game speed here

#             # Check collision with obstacles
#             for obstacle in game.obstacles:
#                 if obstacle[0] <= PLAYER_X + 1:
#                     if obstacle[1] == game.player_y:
#                         game.game_over = True

#         # Display "Game Over" and "Score" until 'B' or 'A' button is pressed
#         while True:
#             oled.fill(0)
#             oled.text("Game Over", 30, 8, COLOR_WHITE)  # Adjusted position
#             oled.text("Score: {}".format(game.score), 30, 18, COLOR_WHITE)  # Adjusted position
#             oled.text("[B] to Exit", 20, 48, COLOR_WHITE)
#             oled.show()

#             if btn.B.value() == 0:
#                 return  # Exit game if 'B' is pressed

# app_start()




