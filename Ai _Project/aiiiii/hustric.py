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
        self.move_number = 0

        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    self.window, text=" ", font=("sans-serif", 16), width=5, height=2,
                    command=lambda row=i, col=j: self.on_click(row, col),bg="#f5f5f5"
                )
                button.grid(row=i, column=j)
                self.buttons.append(button)

        # Initialize lists to store move numbers and execution times
        self.move_numbers = []
        self.execution_times = []

        # Create a reset button
        self.reset_button = tk.Button(self.window, text="Reset", command=self.reset_game)
        self.reset_button.grid(row=3, columnspan=3, pady=10)

    def on_click(self, row, col):
        start_time = time.time()

        index = 3 * row + col
        if self.board[index] == " ":
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe", f"{self.current_player} wins!")
                self.reset_game()
            elif " " not in self.board:
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.reset_game()
            else:
                self.switch_player()
                self.make_ai_move()

        end_time = time.time()
        execution_time = end_time - start_time

        self.move_numbers.append(self.move_number)
        self.execution_times.append(execution_time)

        # Plot the execution time as a line
        plt.plot(self.move_numbers, self.execution_times, color='blue', marker='o', linestyle='-')
        plt.xlabel('Move Number')
        plt.ylabel('Execution Time (seconds)')
        plt.title('Step-by-Step Time Complexity')
        plt.show()

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
        self.move_number += 1

    def make_ai_move(self):
        # Basic AI using a minimax algorithm
        _, node_count = self.minimax(self.board, 0, True)
        print("Nodes explored by AI:", node_count)
        
        best_score = float('-inf')
        best_move = None
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                score, _ = self.minimax(self.board, 0, False)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            self.board[best_move] = "O"
            self.buttons[best_move].config(text="O")
            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe", "O wins!")
                self.reset_game()
            elif " " not in self.board:
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.reset_game()
            else:
                self.switch_player()
    def heuristic_evaluation(self):
        if self.check_winner():
            return 1
        elif self.check_winner(player="O"):
            return -1
        else:
            return 0
    def minimax(self, board, depth, is_maximizing):
        if self.check_winner():
          return self.heuristic_evaluation(), 1
        elif " " not in board:
            return 0, 1
        node_count = 1  # Count the current node

        if is_maximizing:
            max_eval = float('-inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"
                    eval, count = self.minimax(board, depth + 1, False)
                    node_count += count
                    board[i] = " "
                    max_eval = max(max_eval, eval)
            return max_eval, node_count
        else:
            min_eval = float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"
                    eval, count = self.minimax(board, depth + 1, True)
                    node_count += count
                    board[i] = " "
                    min_eval = min(min_eval, eval)
            return min_eval, node_count

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ")
        self.current_player = "X"
        self.move_number = 0

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
