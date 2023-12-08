import numpy as np
from copy import deepcopy
from functools import cache

PIECE_MAP = {
    -1: "🔴",
    0: "⚫",
    1: "🔵",
}

class Game:
    def __init__(self):
        self.board = np.zeros((6, 7))
        self.turn = True

    def __str__(self) -> str:
        string = ""

        for row in self.board:
            pretty_row = list([PIECE_MAP[x] for x in row])
            string += f"{'|'.join(pretty_row)}\n"
        string += ' |'.join([str(x) for x in range(self.board.shape[1])])
        return string

    def current_piece(self):
        return -1 if self.turn else 1

    def move(self, index):
        for row in reversed(self.board):
            if row[index] == 0:
                row[index] = self.current_piece()
                self.turn = not self.turn
                return
        raise Exception("invalid move")
    
    def check_winner(self):
        # Check for a horizontal win
        for row in range(self.board.shape[0]):
            for col in range(self.board.shape[1] - 3):
                if np.all(self.board[row, col:col+4] == self.board[row, col]) and self.board[row, col] != 0:
                    return True

        # Check for a vertical win
        for row in range(self.board.shape[0] - 3):
            for col in range(self.board.shape[1]):
                if np.all(self.board[row:row+4, col] == self.board[row, col]) and self.board[row, col] != 0:
                    return True

        # Check for a diagonal win (left to right)
        for row in range(self.board.shape[0] - 3):
            for col in range(self.board.shape[1] - 3):
                if np.all(self.board[row:row+4, col:col+4].diagonal() == self.board[row, col]) and self.board[row, col] != 0:
                    return True

        # Check for a diagonal win (right to left)
        for row in range(self.board.shape[0] - 3):
            for col in range(3, self.board.shape[1]):
                if np.all(np.fliplr(self.board[row:row+4, col-3:col+1]).diagonal() == self.board[row, col]) and self.board[row, col] != 0:
                    return True

        return False

    def is_move_valid(self, index):
        return self.board[0, index] == 0

    def compute_move(self, depth=4):
        best_score = float('inf') if self.turn else float('-inf')
        best_move = None

        # Check if the game is over or if depth is 0
        if depth == 0 or self.check_winner():
            return None, self.evaluate_board()

        for move in range(self.board.shape[1]):
            if not self.is_move_valid(move):
                continue

            game = deepcopy(self)
            game.move(move)

            _, score = game.compute_move(depth - 1)

            if not self.turn:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move

        return best_move, best_score

    def evaluate_board(self):
        score = 0
        if self.check_winner():
            return 100 if self.turn else -100

        # Evaluate horizontal direction
        for row in range(self.board.shape[0]):
            for col in range(self.board.shape[1] - 3):
                score += self.evaluate_window(self.board[row, col:col+4])

        # Evaluate vertical direction
        for row in range(self.board.shape[0] - 3):
            for col in range(self.board.shape[1]):
                score += self.evaluate_window(self.board[row:row+4, col])

        # Evaluate diagonal (left to right)
        for row in range(self.board.shape[0] - 3):
            for col in range(self.board.shape[1] - 3):
                window = self.board[row:row+4, col:col+4].diagonal()
                score += self.evaluate_window(window)

        # Evaluate diagonal (right to left)
        for row in range(self.board.shape[0] - 3):
            for col in range(3, self.board.shape[1]):
                window = np.fliplr(self.board[row:row+4, col-3:col+1]).diagonal()
                score += self.evaluate_window(window)

        return score

    def evaluate_window(self, window):
        # Define weights for different states
        weights = {0: 0, 1: 1, -1: -1}

        # Count occurrences of each player's piece in the window
        counts = {piece: np.count_nonzero(window == piece) for piece in weights}

        # Calculate the score based on the weighted sum of counts
        score = sum(weights[piece] * counts[piece] for piece in weights)

        return score

def main():
    game = Game()
    print(game)
    while True:
        if game.turn:
            idx = int(input("move:"))
            game.move(idx)
            print(game)
            if game.check_winner():
                print("You win")
                return
        else:
            move, score = game.compute_move()
            print(f"move:{move}", f"score:{score}")
            game.move(move)
            print(game)
            if game.check_winner():
                print("You lose")
                return

if __name__=="__main__":
    main()
