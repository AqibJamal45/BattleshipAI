import tkinter as tk
import random

# Window setup
root = tk.Tk()
root.title("Python Battleship")

GRID_SIZE = 10
CELL_SIZE = 2  
PLAYER_COLOR = "lightblue"
AI_COLOR = "lightgreen"

# Board states:
# 0 = water, 1 = ship, 2 = hit ship, 3 = miss water
ai_board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Ship sizes for classic Battleship
ships = [5, 4, 3, 3, 2]

player_frame = tk.Frame(root)
player_frame.grid(row=0, column=0, padx=20, pady=20)

ai_frame = tk.Frame(root)
ai_frame.grid(row=0, column=1, padx=20, pady=20)

status_label = tk.Label(root, text="Welcome to Battleship!", font=("Times New Roman", 14))
status_label.grid(row=1, column=0, columnspan=2, pady=10)

player_buttons = []
ai_buttons = []

# Create Player grid
tk.Label(player_frame, text="Player Board").grid(row=0, column=0, columnspan=GRID_SIZE)
for r in range(GRID_SIZE):
    row_buttons = []
    for c in range(GRID_SIZE):
        btn = tk.Button(player_frame, width=CELL_SIZE, height=1, bg=PLAYER_COLOR)
        btn.grid(row=r+1, column=c)  # +1 for label row
        row_buttons.append(btn)
    player_buttons.append(row_buttons)

# Create AI grid
tk.Label(ai_frame, text="AI Board").grid(row=0, column=0, columnspan=GRID_SIZE)
for r in range(GRID_SIZE):
    row_buttons = []
    for c in range(GRID_SIZE):
        btn = tk.Button(ai_frame, width=CELL_SIZE, height=1, bg=AI_COLOR)
        btn.grid(row=r+1, column=c)  # +1 for label row
        row_buttons.append(btn)
    ai_buttons.append(row_buttons)

clicked_ai_cells = set()

def place_ships_randomly(board, ships):
    for ship_length in ships:
        placed = False
        while not placed:
            orientation = random.choice(['H', 'V'])
            if orientation == 'H':
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - ship_length)
                # Check if space is free
                if all(board[row][col + i] == 0 for i in range(ship_length)):
                    for i in range(ship_length):
                        board[row][col + i] = 1
                    placed = True
            else:  # Vertical
                row = random.randint(0, GRID_SIZE - ship_length)
                col = random.randint(0, GRID_SIZE - 1)
                if all(board[row + i][col] == 0 for i in range(ship_length)):
                    for i in range(ship_length):
                        board[row + i][col] = 1
                    placed = True

def on_ai_button_click(r, c):
    if (r, c) in clicked_ai_cells:
        status_label.config(text="You already attacked this cell!")
        return

    clicked_ai_cells.add((r, c))

    if ai_board[r][c] == 1:  # Ship present
        ai_board[r][c] = 2  # Mark hit
        ai_buttons[r][c].config(bg="red")
        status_label.config(text=f"Hit at ({r}, {c})!")
    elif ai_board[r][c] == 0:  # Water
        ai_board[r][c] = 3  # Mark miss
        ai_buttons[r][c].config(bg="white")
        status_label.config(text=f"Miss at ({r}, {c})!")
    else:
        # Already hit or missed, but just in case
        status_label.config(text="You already attacked this cell!")
        return

    ai_buttons[r][c].config(state="disabled")

    # Optional: check if all ships sunk (game over)
    if all(cell != 1 for row in ai_board for cell in row):
        status_label.config(text="You sank all AI ships! You win!")
        # Disable all buttons after game over
        for row_buttons in ai_buttons:
            for btn in row_buttons:
                btn.config(state="disabled")

# Place ships on AI board
place_ships_randomly(ai_board, ships)

# Bind AI buttons to click function
for r in range(GRID_SIZE):
    for c in range(GRID_SIZE):
        ai_buttons[r][c].config(command=lambda r=r, c=c: on_ai_button_click(r, c))

root.mainloop()
