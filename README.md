# 🧠 3-Move Limit Tic-Tac-Toe (with Q-Learning AI)

This project is a unique twist on the classic Tic-Tac-Toe game — developed using **Python (Tkinter)** and powered by a **self-learning Q-Learning AI**.

🎯 **Main Rule**: Each player can only have **3 active moves** on the board at any time. Once a 4th move is made, the earliest move disappears — adding a new layer of challenge!

---

## 🚀 Features

- 🎮 **Game Modes**
  - **Single Player** (You vs AI)
  - **Two Player** (Local multiplayer)
  - **AI Difficulty Levels** (Easy, Medium, Hard)

- 🧠 **Q-Learning AI**
  - Learns from self-play
  - Stores training in `ai_q_table.pkl`
  - Automatically trains if the table is missing
  - Live **training progress bar**

- 🖼️ **User Interface**
  - Built using **Tkinter**
  - Interactive buttons and a clear game layout
  - **Back button** navigation
  - **Name input** for players in Two-Player mode
  - Win detection with visual highlighting

- 📊 **Scoreboard**
  - Real-time tracking of player wins
  - Separate stats for Single and Two Player modes

---

## 🏁 How to Run

```bash
python tic_tac_toe_3move.py
