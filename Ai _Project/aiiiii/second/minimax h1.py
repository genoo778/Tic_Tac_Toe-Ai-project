import tkinter as tk
from tkinter import messagebox
import time
import matplotlib.pyplot as plt

def create_board():
    return [" " for _ in range(9)]

def check_winner(board):
    lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
             (0, 3, 6), (1, 4, 7), (2, 5, 8),
             (0, 4, 8), (2, 4, 6)]

    for line in lines:
        if board[line[0]] == board[line[1]] == board[line[2]] != " ":
            return True
    return False

def is_board_full(board):
    return " " not in board

def center_occupancy_heuristic(board, player):
    center_index = 4
    center_score = 2 if board[center_index] == player else 0
    return center_score

def minimax(board, depth, is_maximizing, player):
    if check_winner(board):
        return -1 if is_maximizing else 1
    elif is_board_full(board):
        return 0

    scores = []
    for i in range(9):
        if board[i] == " ":
            board[i] = player
            score = minimax(board, depth + 1, not is_maximizing, "O" if player == "X" else "X")
            board[i] = " "
            scores.append(score)

    return max(scores) if is_maximizing else min(scores)

move_number = 0  # Initialize move_number
execution_times = []  # List to store execution times

def make_ai_move():
    global move_number, execution_times
    start_time = time.time()

    best_score = float('-inf')
    best_move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, False, "X")
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i

    end_time = time.time()
    execution_time = end_time - start_time
    execution_times.append(execution_time)

    move_number += 1

    if best_move is not None:
        board[best_move] = "O"
        buttons[best_move].config(text="O", state=tk.DISABLED)
        if check_winner(board):
            messagebox.showinfo("Tic Tac Toe", "O wins!")
            show_plots()

        elif is_board_full(board):
            messagebox.showinfo("Tic Tac Toe", "It's a draw!")
            show_plots()

def on_click(row, col):
    global move_number
    index = 3 * row + col
    if board[index] == " ":
        board[index] = "X"
        buttons[index].config(text="X", state=tk.DISABLED)
        if check_winner(board):
            messagebox.showinfo("Tic Tac Toe", "X wins!")
            show_plots()
        elif not is_board_full(board):
            make_ai_move()
        else:
            messagebox.showinfo("Tic Tac Toe", "It's a draw!")
            show_plots()

def reset_game():
    global board, move_number, execution_times
    board = create_board()
    move_number = 0
    execution_times = []
    for button in buttons:
        button.config(text=" ", state=tk.NORMAL)

def show_plots():
    plt.plot(range(1, move_number + 1), execution_times, color='blue', marker='o', linestyle='-')
    plt.xlabel('Move Number')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Cumulative Time Complexity Analysis')
    plt.show()

def run():
    window.mainloop()

if __name__ == "__main__":
    board = create_board()

    window = tk.Tk()
    window.title("Tic Tac Toe")
    window.configure(bg="white")

    buttons = []
    for i in range(3):
        for j in range(3):
            button = tk.Button(
                window, text=" ", font=("sans-serif", 16), width=5, height=2,
                command=lambda row=i, col=j: on_click(row, col),
                bg="#f5f5f5"
            )
            button.grid(row=i, column=j, padx=5, pady=5)
            buttons.append(button)

    # Create a reset button
    reset_button = tk.Button(window, text="Reset", bg="#f5f5f5", command=reset_game)
    reset_button.grid(row=3, columnspan=3, pady=10)

    run()
