import tkinter as tk
from tkinter import messagebox
import random
import time
import matplotlib.pyplot as plt

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.board = [" " for _ in range(9)]  # 3x3 board represented as a list
        self.current_player = "X"
        self.execution_times = []  # List to store execution times

        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    self.window, text=" ", font=("sans-serif", 16), width=5, height=2,
                    command=lambda row=i, col=j: self.on_click(row, col),
                    bg="#f5f5f5"
                )
                button.grid(row=i, column=j)
                self.buttons.append(button)

        # Create a reset button
        reset_button = tk.Button(self.window, text="Reset", command=self.reset_game, bg="#f5f5f5")
        reset_button.grid(row=3, column=1, pady=10)    

    def on_click(self, row, col):
        start_time = time.time()

        index = 3 * row + col
        if self.board[index] == " ":
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner():
                self.show_result()
            elif " " not in self.board:
                self.show_result(draw=True)
            else:
                self.switch_player()
                self.make_ai_move()

        end_time = time.time()
        execution_time = end_time - start_time
        self.execution_times.append(execution_time)

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

    def make_ai_move(self):
        # Medium-level AI: Combining random moves and strategic blocking
        available_spots = [i for i in range(9) if self.board[i] == " "]
        if available_spots:
            # Random move with 60% probability
            if random.random() < 0.6:
                ai_move = random.choice(available_spots)
            else:
                # Strategic blocking move
                ai_move = self.strategic_blocking()

            self.board[ai_move] = "O"
            self.buttons[ai_move].config(text="O")
            if self.check_winner():
                self.show_result()
            elif " " not in self.board:
                self.show_result(draw=True)
            else:
                self.switch_player()

    def strategic_blocking(self):
        # Check if there's a move to block the player from winning
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "X"
                if self.check_winner():
                    self.board[i] = " "
                    return i
                self.board[i] = " "

        # If no blocking move, return a random move
        return random.choice([i for i in range(9) if self.board[i] == " "])

    def show_result(self, draw=False):
        if draw:
            messagebox.showinfo("Tic Tac Toe", "It's a draw!")
        else:
            winner = self.current_player
            messagebox.showinfo("Tic Tac Toe", f"{winner} wins!")

        self.plot_time_complexity()
        self.reset_game()

    def plot_time_complexity(self):
        cumulative_time = [sum(self.execution_times[:i + 1]) for i in range(len(self.execution_times))]
        plt.plot(range(1, len(cumulative_time) + 1), cumulative_time, marker='o')
        plt.title('Cumulative Time Complexity Analysis')
        plt.xlabel('Move Number')
        plt.ylabel('Cumulative Time (seconds)')
        plt.show()

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ")
        self.current_player = "X"
        self.execution_times = []

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
