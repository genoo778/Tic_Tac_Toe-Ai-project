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

def alpha_beta_pruning(board, depth, alpha, beta, is_maximizing):
    if check_winner(board):
        return -1 if is_maximizing else 1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        max_eval = float('-inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                eval_score = alpha_beta_pruning(board, depth + 1, alpha, beta, False)
                board[i] = " "
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                eval_score = alpha_beta_pruning(board, depth + 1, alpha, beta, True)
                board[i] = " "
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
        return min_eval

def make_ai_move():
    start_time = time.time()
    
    best_score = float('-inf')
    best_move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = alpha_beta_pruning(board, 0, float('-inf'), float('inf'), False)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i

    end_time = time.time()
    execution_time = end_time - start_time
    execution_times.append(execution_time)

    if best_move is not None:
        board[best_move] = "O"
        buttons[best_move].config(text="O", state=tk.DISABLED)
        if check_winner(board):
            messagebox.showinfo("Tic Tac Toe", "O wins!")
            reset_game()
        elif is_board_full(board):
            messagebox.showinfo("Tic Tac Toe", "It's a draw!")
            reset_game()
        else:
            update_plot()

def on_click(row, col):
    index = 3 * row + col
    if board[index] == " ":
        board[index] = "X"
        buttons[index].config(text="X", state=tk.DISABLED)
        if check_winner(board):
            messagebox.showinfo("Tic Tac Toe", "X wins!")
            reset_game()
        elif not is_board_full(board):
            make_ai_move()
        else:
            messagebox.showinfo("Tic Tac Toe", "It's a draw!")
            reset_game()

def reset_game():
    global board, execution_times
    board = create_board()
    execution_times = []
    for button in buttons:
        button.config(text=" ", state=tk.NORMAL)

def reset_game_button():
    reset_game()

def update_plot():
    cumulative_time = [sum(execution_times[:i + 1]) for i in range(len(execution_times))]
    plt.clf()  # Clear the previous plot
    plt.plot(range(1, len(cumulative_time) + 1), cumulative_time, marker='o')
    plt.title('Step-by-Step Time Complexity')
    plt.xlabel('Move Number')
    plt.ylabel('Cumulative Time (seconds)')
    plt.pause(0.1)  # Pause to allow the plot to update

def run():
    window.after(100, make_ai_move)  # Use after to schedule the first AI move after a short delay
    window.mainloop()

if __name__ == "__main__":
    board = create_board()
    execution_times = []

    window = tk.Tk()
    window.title("Tic Tac Toe")

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

    reset_button = tk.Button(window, text="Reset", command=reset_game_button)
    reset_button.grid(row=3, columnspan=3, pady=10)

    run()

    # Plot cumulative time complexity
    plt.show()
