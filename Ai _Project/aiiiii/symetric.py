import tkinter as tk
from tkinter import messagebox
import time
import matplotlib.pyplot as plt

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.board = [" " for _ in range(9)]  # 3x3 board represented as a list
        self.current_player = "X"
        self.move_times = []

        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    self.window, text=" ", font=("sans-serif", 16), width=5, height=2,
                    command=lambda row=i, col=j: self.on_click(row, col), bg="#f5f5f5"
                )
                button.grid(row=i, column=j)
                self.buttons.append(button)
        reset_button = tk.Button(self.window, text="Reset",
                                 command=self.reset_game, bg="#f5f5f5")
        reset_button.grid(row=3, column=1, pady=10)      

    def on_click(self, row, col):
        start_time = time.time()

        index = 3 * row + col
        if self.board[index] == " ":
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner():
                end_time = time.time()
                self.move_times.append(end_time - start_time)
                self.show_result()
            elif " " not in self.board:
                end_time = time.time()
                self.move_times.append(end_time - start_time)
                self.show_result(draw=True)
            else:
                end_time = time.time()
                self.move_times.append(end_time - start_time)
                self.switch_player()
                self.make_ai_move()
                self.plot_time_complexity()

    def make_ai_move(self):
        # Basic AI using a minimax algorithm
        best_score = float('-inf')
        best_move = None
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            self.board[best_move] = "O"
            self.buttons[best_move].config(text="O")
            if self.check_winner():
                self.show_result()
            elif " " not in self.board:
                self.show_result(draw=True)
            else:
    
                self.switch_player()
    def get_symmetric_moves(self):
        # Returns a subset of symmetrically equivalent moves
        return [0, 2, 6, 8]            

    def show_result(self, draw=False):
        if draw:
            messagebox.showinfo("Tic Tac Toe", "It's a draw!")
        else:
            messagebox.showinfo("Tic Tac Toe", f"{self.current_player} wins!")

    def plot_time_complexity(self):
        cumulative_time = [sum(self.move_times[:i + 1]) for i in range(len(self.move_times))]
        plt.plot(range(1, len(cumulative_time) + 1), cumulative_time, marker='o', color='blue')
        plt.title('Step-by-Step Time Complexity')
        plt.xlabel('Move Number')
        plt.ylabel('Cumulative Time (seconds)')
        plt.draw()
        plt.pause(0.1)  # Pause to allow the plot to be displayed
        self.window.update_idletasks()

    def check_winner(self):
        lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                 (0, 3, 6), (1, 4, 7), (2, 5, 8),
                 (0, 4, 8), (2, 4, 6)]

        for line in lines:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != " ":
                return True
        return False

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
    
    def rotate_board(self, board):
        # Rotate the board 90 degrees clockwise
        return [board[6], board[3], board[0], board[7], board[4], board[1], board[8], board[5], board[2]]

    def reflect_board(self, board):
        # Reflect the board horizontally
        return [board[2], board[1], board[0], board[5], board[4], board[3], board[8], board[7], board[6]]    

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner():
            return -1 if is_maximizing else 1
        elif " " not in board:
            return 0

        if is_maximizing:
            max_eval = float('-inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"
                    eval = self.minimax(board, depth + 1, False)
                    board[i] = " "
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"
                    eval = self.minimax(board, depth + 1, True)
                    board[i] = " "
                    min_eval = min(min_eval, eval)
            return min_eval

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ")
        self.current_player = "X"
        self.move_times = []

    def run(self):
        self.window.mainloop()

# Main program
if __name__ == "__main__":
    game = TicTacToe()
    game.run()
