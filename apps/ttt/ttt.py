from badge import oled, btn
from time import sleep_ms
from random import choice

# Define constants
GRID_SIZE = 3
CELL_SIZE = 21  # Adjusted to fit the screen
GRID_WIDTH = GRID_SIZE * CELL_SIZE
GRID_HEIGHT = GRID_SIZE * CELL_SIZE

# Define colors
COLOR_BLACK = 0
COLOR_WHITE = 1

class TicTacToeGame:
    def __init__(self, player_mode):
        self.grid = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.selected_row = 0
        self.selected_col = 0
        self.player_mode = player_mode
        
        if self.player_mode == "Robot":
            self.current_player = 'O'  # Let the AI (O) play first

    def check_winner(self):
        # Check rows
        for row in self.grid:
            if row[0] == row[1] == row[2] != ' ':
                self.game_over = True
                self.winner = row[0]
                return

        # Check columns
        for col in range(GRID_SIZE):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] != ' ':
                self.game_over = True
                self.winner = self.grid[0][col]
                return

        # Check diagonals
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != ' ':
            self.game_over = True
            self.winner = self.grid[0][0]
            return
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != ' ':
            self.game_over = True
            self.winner = self.grid[0][2]
            return

        # Check if it's a draw
        if all([cell != ' ' for row in self.grid for cell in row]):
            self.game_over = True
            self.winner = 'Draw'

    def draw(self):
        oled.fill(0)

        # Draw grid lines
        for i in range(GRID_SIZE + 1):
            oled.vline(i * CELL_SIZE, 0, GRID_HEIGHT, COLOR_WHITE)
            oled.hline(0, i * CELL_SIZE, GRID_WIDTH, COLOR_WHITE)

        # Highlight selected box
        oled.rect(self.selected_col * CELL_SIZE, self.selected_row * CELL_SIZE, CELL_SIZE, CELL_SIZE, COLOR_WHITE)

        # Draw X's and O's
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] == 'X':
                    self.draw_x(row, col)
                elif self.grid[row][col] == 'O':
                    self.draw_o(row, col)

        # Draw turn indicator
        if not self.game_over:
            oled.text("Your" if self.current_player == 'X' else "Opponent", GRID_WIDTH + 5, 15, COLOR_WHITE)
            oled.text("Turn", GRID_WIDTH + 5, 30, COLOR_WHITE)

        oled.show()

    def draw_x(self, row, col):
        oled.line(col * CELL_SIZE + 2, row * CELL_SIZE + 2, (col + 1) * CELL_SIZE - 2, (row + 1) * CELL_SIZE - 2, COLOR_WHITE)
        oled.line((col + 1) * CELL_SIZE - 2, row * CELL_SIZE + 2, col * CELL_SIZE + 2, (row + 1) * CELL_SIZE - 2, COLOR_WHITE)

    def draw_o(self, row, col):
        oled.circle(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE // 2 - 2, COLOR_WHITE)

    def handle_input(self):
        if self.player_mode != "Robot":
            # Handle button presses for selecting boxes
            if btn.U.value() == 0:
                self.selected_row = (self.selected_row - 1) % GRID_SIZE
            elif btn.D.value() == 0:
                self.selected_row = (self.selected_row + 1) % GRID_SIZE
            elif btn.L.value() == 0:
                self.selected_col = (self.selected_col - 1) % GRID_SIZE
            elif btn.R.value() == 0:
                self.selected_col = (self.selected_col + 1) % GRID_SIZE
            elif btn.A.value() == 0:
                if self.grid[self.selected_row][self.selected_col] == ' ':
                    self.grid[self.selected_row][self.selected_col] = self.current_player
                    self.check_winner()
                    if not self.game_over:
                        self.current_player = 'O' if self.current_player == 'X' else 'X'

        if self.player_mode == "Robot":
            if self.current_player == 'O':
                self.make_ai_move()
            else:
                # Handle button presses for selecting boxes
                if btn.U.value() == 0:
                    self.selected_row = (self.selected_row - 1) % GRID_SIZE
                elif btn.D.value() == 0:
                    self.selected_row = (self.selected_row + 1) % GRID_SIZE
                elif btn.L.value() == 0:
                    self.selected_col = (self.selected_col - 1) % GRID_SIZE
                elif btn.R.value() == 0:
                    self.selected_col = (self.selected_col + 1) % GRID_SIZE
                elif btn.A.value() == 0:
                    if self.grid[self.selected_row][self.selected_col] == ' ':
                        self.grid[self.selected_row][self.selected_col] = self.current_player
                        self.check_winner()
                        if not self.game_over:
                            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def make_ai_move(self):
        best_score = float('-inf')
        best_move = None

        # Iterate over all empty cells and simulate each move
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == ' ':
                    # Make the move
                    self.grid[i][j] = 'O'
                    score = self.minimax(False)
                    # Undo the move
                    self.grid[i][j] = ' '
                    
                    # Update best move if score is better
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        # Make the best move
        if best_move:
            self.grid[best_move[0]][best_move[1]] = 'O'
            self.check_winner()
            if not self.game_over:
                self.current_player = 'X'

    def minimax(self, is_maximizing):
        # Check if the game is over
        self.check_winner()
        if self.game_over:
            if self.winner == 'O':
                return 1
            elif self.winner == 'X':
                return -1
            else:
                return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    if self.grid[i][j] == ' ':
                        self.grid[i][j] = 'O'
                        score = self.minimax(False)
                        self.grid[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    if self.grid[i][j] == ' ':
                        self.grid[i][j] = 'X'
                        score = self.minimax(True)
                        self.grid[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score

    def evaluate_board(self):
        # Evaluate the board position
        for row in self.grid:
            if row.count('O') == GRID_SIZE:
                return 1
            elif row.count('X') == GRID_SIZE:
                return -1

        for col in range(GRID_SIZE):
            if [self.grid[i][col] for i in range(GRID_SIZE)].count('O') == GRID_SIZE:
                return 1
            elif [self.grid[i][col] for i in range(GRID_SIZE)].count('X') == GRID_SIZE:
                return -1

        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] == 'O' or \
           self.grid[0][2] == self.grid[1][1] == self.grid[2][0] == 'O':
            return 1
        elif self.grid[0][0] == self.grid[1][1] == self.grid[2][2] == 'X' or \
             self.grid[0][2] == self.grid[1][1] == self.grid[2][0] == 'X':
            return -1

        return 0

def start_page():
    oled.fill(0)
    oled.text("Select Mode:", 5, 10, COLOR_WHITE)
    oled.text("[A] Robot", 5, 30, COLOR_WHITE)
    oled.text("[B] 2 Players", 5, 45, COLOR_WHITE)
    oled.show()

    while True:
        if btn.A.value() == 0:
            return "Robot"
        elif btn.B.value() == 0:
            return "2 Player"

def end_game(winner):
    oled.fill(0)
    if winner == 'Draw':
        oled.text("Draw", 48, 20, COLOR_WHITE)
    else:
        oled.text("Win" if winner == 'X' else "Lose", 48, 20, COLOR_WHITE)
    oled.text("[U] to Exit", 20, 40, COLOR_WHITE)
    oled.show()

    while True:
        if btn.U.value() == 0:
            return

def app_start():
    player_mode = start_page()

    if player_mode == "Robot":
        game = TicTacToeGame(player_mode)
        while not game.game_over:
            game.handle_input()
            game.draw()
            sleep_ms(100)
        end_game(game.winner)
    elif player_mode == "2 Player":
        game = TicTacToeGame(player_mode)
        while not game.game_over:
            game.handle_input()
            game.draw()
            sleep_ms(100)
        end_game(game.winner)

app_start()

# from badge import oled, btn
# from time import sleep_ms
# from random import choice

# # Define constants
# GRID_SIZE = 3
# CELL_SIZE = 21  # Adjusted to fit the screen
# GRID_WIDTH = GRID_SIZE * CELL_SIZE
# GRID_HEIGHT = GRID_SIZE * CELL_SIZE

# # Define colors
# COLOR_BLACK = 0
# COLOR_WHITE = 1

# class TicTacToeGame:
#     def __init__(self, player_mode):
#         self.grid = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
#         self.current_player = 'X'
#         self.game_over = False
#         self.winner = None
#         self.selected_row = 0
#         self.selected_col = 0
#         self.player_mode = player_mode
        
#         if self.player_mode == "Robot":
#             self.current_player = 'O'  # Let the AI (O) play first

#     def check_winner(self):
#         # Check rows
#         for row in self.grid:
#             if row[0] == row[1] == row[2] != ' ':
#                 self.game_over = True
#                 self.winner = row[0]
#                 return

#         # Check columns
#         for col in range(GRID_SIZE):
#             if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] != ' ':
#                 self.game_over = True
#                 self.winner = self.grid[0][col]
#                 return

#         # Check diagonals
#         if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != ' ':
#             self.game_over = True
#             self.winner = self.grid[0][0]
#             return
#         if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != ' ':
#             self.game_over = True
#             self.winner = self.grid[0][2]
#             return

#         # Check if it's a draw
#         if all([cell != ' ' for row in self.grid for cell in row]):
#             self.game_over = True
#             self.winner = 'Draw'

#     def draw(self):
#         oled.fill(0)

#         # Draw grid lines
#         for i in range(GRID_SIZE + 1):
#             oled.vline(i * CELL_SIZE, 0, GRID_HEIGHT, COLOR_WHITE)
#             oled.hline(0, i * CELL_SIZE, GRID_WIDTH, COLOR_WHITE)

#         # Highlight selected box
#         oled.rect(self.selected_col * CELL_SIZE, self.selected_row * CELL_SIZE, CELL_SIZE, CELL_SIZE, COLOR_WHITE)

#         # Draw X's and O's
#         for row in range(GRID_SIZE):
#             for col in range(GRID_SIZE):
#                 if self.grid[row][col] == 'X':
#                     self.draw_x(row, col)
#                 elif self.grid[row][col] == 'O':
#                     self.draw_o(row, col)

#         # Draw turn indicator
#         if not self.game_over:
#             oled.text("Your" if self.current_player == 'X' else "Opponent", GRID_WIDTH + 5, 15, COLOR_WHITE)
#             oled.text("Turn", GRID_WIDTH + 5, 30, COLOR_WHITE)

#         oled.show()

#     def draw_x(self, row, col):
#         oled.line(col * CELL_SIZE + 2, row * CELL_SIZE + 2, (col + 1) * CELL_SIZE - 2, (row + 1) * CELL_SIZE - 2, COLOR_WHITE)
#         oled.line((col + 1) * CELL_SIZE - 2, row * CELL_SIZE + 2, col * CELL_SIZE + 2, (row + 1) * CELL_SIZE - 2, COLOR_WHITE)

#     def draw_o(self, row, col):
#         oled.circle(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE // 2 - 2, COLOR_WHITE)

#     def handle_input(self):
#         if self.player_mode != "Robot":
#             # Handle button presses for selecting boxes
#             if btn.U.value() == 0:
#                 self.selected_row = (self.selected_row - 1) % GRID_SIZE
#             elif btn.D.value() == 0:
#                 self.selected_row = (self.selected_row + 1) % GRID_SIZE
#             elif btn.L.value() == 0:
#                 self.selected_col = (self.selected_col - 1) % GRID_SIZE
#             elif btn.R.value() == 0:
#                 self.selected_col = (self.selected_col + 1) % GRID_SIZE
#             elif btn.A.value() == 0:
#                 if self.grid[self.selected_row][self.selected_col] == ' ':
#                     self.grid[self.selected_row][self.selected_col] = self.current_player
#                     self.check_winner()
#                     if not self.game_over:
#                         self.current_player = 'O' if self.current_player == 'X' else 'X'

#         if self.player_mode == "Robot":
#             if self.current_player == 'O':
#                 self.make_ai_move()
#             else:
#                 # Handle button presses for selecting boxes
#                 if btn.U.value() == 0:
#                     self.selected_row = (self.selected_row - 1) % GRID_SIZE
#                 elif btn.D.value() == 0:
#                     self.selected_row = (self.selected_row + 1) % GRID_SIZE
#                 elif btn.L.value() == 0:
#                     self.selected_col = (self.selected_col - 1) % GRID_SIZE
#                 elif btn.R.value() == 0:
#                     self.selected_col = (self.selected_col + 1) % GRID_SIZE
#                 elif btn.A.value() == 0:
#                     if self.grid[self.selected_row][self.selected_col] == ' ':
#                         self.grid[self.selected_row][self.selected_col] = self.current_player
#                         self.check_winner()
#                         if not self.game_over:
#                             self.current_player = 'O' if self.current_player == 'X' else 'X'

#     def make_ai_move(self):
#         empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == ' ']
#         if empty_cells:
#             row, col = choice(empty_cells)
#             self.grid[row][col] = 'O'
#             self.check_winner()
#             if not self.game_over:
#                 self.current_player = 'X'

# def start_page():
#     oled.fill(0)
#     oled.text("Select Mode:", 5, 10, COLOR_WHITE)
#     oled.text("[A] Robot", 5, 30, COLOR_WHITE)
#     oled.text("[B] 2 Players", 5, 45, COLOR_WHITE)
#     oled.show()

#     while True:
#         if btn.A.value() == 0:
#             return "Robot"
#         elif btn.B.value() == 0:
#             return "2 Player"

# def end_game(winner):
#     oled.fill(0)
#     if winner == 'Draw':
#         oled.text("Draw", 48, 20, COLOR_WHITE)
#     else:
#         oled.text("Win" if winner == 'X' else "Lose", 48, 20, COLOR_WHITE)
#     oled.text("[U] to Exit", 20, 40, COLOR_WHITE)
#     oled.show()

#     while True:
#         if btn.U.value() == 0:
#             return

# def app_start():
#     player_mode = start_page()

#     if player_mode == "Robot":
#         game = TicTacToeGame(player_mode)
#         while not game.game_over:
#             game.handle_input()
#             game.draw()
#             sleep_ms(100)
#         end_game(game.winner)
#     elif player_mode == "2 Player":
#         game = TicTacToeGame(player_mode)
#         while not game.game_over:
#             game.handle_input()
#             game.draw()
#             sleep_ms(100)
#         end_game(game.winner)

# app_start()