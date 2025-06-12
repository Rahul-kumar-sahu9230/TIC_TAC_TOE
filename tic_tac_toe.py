import tkinter as tk
from tkinter import messagebox
import random
import pickle
import os

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("3-Move Limit Tic-Tac-Toe")
        self.root.geometry("520x700")
        self.root.configure(bg="#d9b996")

        self.q_table = {}
        self.load_q_table()
        self.single_player = False
        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="🎮 3-Move Tic-Tac-Toe", font=("Helvetica", 24, 'bold'),
                 bg="#ffe6cc", fg="#333").pack(pady=40)

        tk.Button(self.root, text="Single Player (vs AI)", font=("Helvetica", 16),
                  bg="#ccffcc", command=self.start_single_player).pack(pady=20)

        tk.Button(self.root, text="Double Player", font=("Helvetica", 16),
                  bg="#ffcccc", command=self.start_double_player).pack(pady=20)

    def start_single_player(self):
        self.single_player = True
        self.train_ai(10000)
        self.setup_game()

    def start_double_player(self):
        self.single_player = False
        self.setup_game()

    def setup_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.board = ['' for _ in range(9)]
        self.buttons = []
        self.current_player = 'X'
        self.moves = {'X': [], 'O': []}
        self.greyed = {'X': None, 'O': None}
        self.move_counts = {'X': 0, 'O': 0}
        self.win_counts = {'X': 0, 'O': 0}

        tk.Label(self.root, text="🎮 3-Move Tic-Tac-Toe", font=("Helvetica", 24, 'bold'),
                 bg="#ffe6cc", fg="#333").pack(pady=10)

        self.board_frame = tk.Frame(self.root, bg="#ffe6cc")
        self.board_frame.pack(pady=5)

        for i in range(9):
            btn = tk.Button(self.board_frame, text='', font=("Helvetica", 28),
                            width=4, height=2, bg="white", fg="black",
                            relief="solid", borderwidth=2,
                            command=lambda i=i: self.make_move(i))
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        self.table_frame = tk.Frame(self.root, bg="#ffe6cc")
        self.table_frame.pack(pady=10)

        self.labels = {}
        headers = ["Player", "Moves", "Wins"]
        for i, header in enumerate(headers):
            tk.Label(self.table_frame, text=header, font=("Helvetica", 14, 'bold'),
                     bg="#ffe6cc", fg="#222", width=10).grid(row=0, column=i)

        for i, player in enumerate(['X', 'O']):
            tk.Label(self.table_frame, text=player, font=("Helvetica", 14),
                     bg="#ffe6cc", width=10).grid(row=i+1, column=0)
            self.labels[f"{player}_moves"] = tk.Label(self.table_frame, text="0", font=("Helvetica", 14),
                                                      bg="#ffe6cc", width=10)
            self.labels[f"{player}_moves"].grid(row=i+1, column=1)
            self.labels[f"{player}_wins"] = tk.Label(self.table_frame, text="0", font=("Helvetica", 14),
                                                     bg="#ffe6cc", width=10)
            self.labels[f"{player}_wins"].grid(row=i+1, column=2)

        self.controls = tk.Frame(self.root, bg="#ffe6cc")
        self.controls.pack(pady=20)

        tk.Button(self.controls, text="🔁 Reset Game", font=("Helvetica", 14),
                  bg="#ccffcc", command=self.reset_game, width=15).pack(side="left", padx=10)

        tk.Button(self.controls, text="🏠 Main Menu", font=("Helvetica", 14),
                  bg="#ccccff", command=self.create_main_menu, width=15).pack(side="left", padx=10)

        self.update_counters()

    def reset_game(self):
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'
        self.moves = {'X': [], 'O': []}
        self.greyed = {'X': None, 'O': None}
        self.move_counts = {'X': 0, 'O': 0}
        for btn in self.buttons:
            btn.config(text='', fg='black', state='normal')
        self.update_counters()

    def make_move(self, index):
        if self.board[index] != '':
            return

        player = self.current_player
        opponent = 'O' if player == 'X' else 'X'

        if self.greyed[player] is not None:
            old_idx = self.greyed[player]
            self.board[old_idx] = ''
            self.buttons[old_idx].config(text='', fg='black')
            self.moves[player].pop(0)
            self.greyed[player] = None

        self.board[index] = player
        self.moves[player].append(index)
        self.move_counts[player] += 1
        self.update_move_labels(player)
        self.update_counters()

        if len(self.moves[opponent]) == 3 and self.greyed[opponent] is None:
            oldest = self.moves[opponent][0]
            self.buttons[oldest].config(fg='gray')
            self.greyed[opponent] = oldest

        if self.check_winner(player):
            self.win_counts[player] += 1
            self.update_counters()
            messagebox.showinfo("🏆 Winner!", f"Player {player} wins!")
            self.reset_game()
            return
        elif '' not in self.board:
            messagebox.showinfo("🤝 Draw", "It's a draw!")
            self.reset_game()
            return

        self.current_player = opponent

        if self.single_player and self.current_player == 'O':
            self.root.after(300, self.ai_move)

    def ai_move(self):
        state = tuple(self.board)
        actions = [i for i, x in enumerate(self.board) if x == '']
        if not actions:
            return
        if state in self.q_table:
            action = max(actions, key=lambda a: self.q_table[state].get(a, 0))
        else:
            action = random.choice(actions)
        self.make_move(action)

    def update_move_labels(self, player):
        subscript_nums = ['₁', '₂', '₃']
        color = 'red' if player == 'X' else 'blue'

        for i, move_index in enumerate(self.moves[player]):
            label = f"{player}\n{subscript_nums[i]}"
            fg_color = 'gray' if self.greyed[player] == move_index else color
            self.buttons[move_index].config(text=label, fg=fg_color)

    def update_counters(self):
        for p in ['X', 'O']:
            self.labels[f"{p}_moves"].config(text=str(self.move_counts[p]))
            self.labels[f"{p}_wins"].config(text=str(self.win_counts[p]))

    def check_winner(self, player):
        combos = [(0,1,2),(3,4,5),(6,7,8),
                  (0,3,6),(1,4,7),(2,5,8),
                  (0,4,8),(2,4,6)]
        return any(all(self.board[i] == player for i in combo) for combo in combos)

    def check_winner_sim(self, board, player):
        combos = [(0,1,2),(3,4,5),(6,7,8),
                  (0,3,6),(1,4,7),(2,5,8),
                  (0,4,8),(2,4,6)]
        return any(all(board[i] == player for i in combo) for combo in combos)

    def train_ai(self, episodes=10000):
        alpha = 0.5
        gamma = 0.9
        epsilon = 0.2

        for _ in range(episodes):
            board = [''] * 9
            current = 'X'
            moves = {'X': [], 'O': []}
            greyed = {'X': None, 'O': None}

            while True:
                state = tuple(board)
                actions = [i for i, x in enumerate(board) if x == '']
                if not actions:
                    break

                if state not in self.q_table or not self.q_table[state] or random.random() < epsilon:
                    action = random.choice(actions)
                else:
                    action = max(self.q_table[state], key=self.q_table[state].get)

                if state not in self.q_table:
                    self.q_table[state] = {}
                if action not in self.q_table[state]:
                    self.q_table[state][action] = 0

                if greyed[current] is not None:
                    board[greyed[current]] = ''
                    moves[current].pop(0)
                    greyed[current] = None

                board[action] = current
                moves[current].append(action)

                if len(moves['X' if current == 'O' else 'O']) == 3 and greyed['X' if current == 'O' else 'O'] is None:
                    opponent_old = moves['X' if current == 'O' else 'O'][0]
                    greyed['X' if current == 'O' else 'O'] = opponent_old

                reward = 0
                done = False
                if self.check_winner_sim(board, current):
                    reward = 1
                    done = True

                next_state = tuple(board)
                if next_state not in self.q_table:
                    self.q_table[next_state] = {}

                max_next = max(self.q_table[next_state].values(), default=0)
                self.q_table[state][action] += alpha * (reward + gamma * max_next - self.q_table[state][action])

                if done:
                    break

                current = 'O' if current == 'X' else 'X'

        self.save_q_table()

    def save_q_table(self):
        with open("q_table.pkl", "wb") as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self):
        if os.path.exists("q_table.pkl"):
            with open("q_table.pkl", "rb") as f:
                self.q_table = pickle.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
    
    # n right now this code is perfectly working fine.
