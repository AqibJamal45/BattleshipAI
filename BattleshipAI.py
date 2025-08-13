import tkinter as tk
import random

# --- Game setup ---
GRID_SIZE = 10
CELL_SIZE = 2
PLAYER_COLOR = "lightblue"
AI_COLOR = "lightgreen"
HIT_COLOR = "red"
MISS_COLOR = "white"
SHIP_COLOR = "gray"
PREVIEW_OK_COLOR = "yellow"
PREVIEW_BAD_COLOR = "pink"

ships = [5, 4, 3, 3, 2]  # Ship sizes

# Boards: 0 = water, 1 = ship, 2 = hit, 3 = miss
player_board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
ai_board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

clicked_ai_cells = set()
clicked_player_cells = set()

# Placement state
placing_ships = True
current_ship_index = 0
ship_orientation = 'H'  # H = horizontal, V = vertical

# --- Tkinter window ---
root = tk.Tk()
root.title("Python Battleship")

player_frame = tk.Frame(root)
player_frame.grid(row=0, column=0, padx=20, pady=20)

ai_frame = tk.Frame(root)
ai_frame.grid(row=0, column=1, padx=20, pady=20)

status_label = tk.Label(root, text="Place your ship of length 5", font=("Times New Roman", 14))
status_label.grid(row=1, column=0, columnspan=2, pady=10)

player_buttons = []
ai_buttons = []

# --- Functions ---
def place_ships_randomly(board, ships):
    for ship_length in ships:
        placed = False
        while not placed:
            orientation = random.choice(['H', 'V'])
            if orientation == 'H':
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - ship_length)
                if all(board[row][col + i] == 0 for i in range(ship_length)):
                    for i in range(ship_length):
                        board[row][col + i] = 1
                    placed = True
            else:
                row = random.randint(0, GRID_SIZE - ship_length)
                col = random.randint(0, GRID_SIZE - 1)
                if all(board[row + i][col] == 0 for i in range(ship_length)):
                    for i in range(ship_length):
                        board[row + i][col] = 1
                    placed = True

def check_game_over(board):
    return all(cell != 1 for row in board for cell in row)

def disable_all_buttons():
    for row_buttons in ai_buttons:
        for btn in row_buttons:
            btn.config(state="disabled")
    replay_button.grid(row=2, column=0, columnspan=2, pady=10)  # Show replay button

def ai_turn():
    while True:
        r = random.randint(0, GRID_SIZE - 1)
        c = random.randint(0, GRID_SIZE - 1)
        if (r, c) not in clicked_player_cells:
            clicked_player_cells.add((r, c))
            if player_board[r][c] == 1:
                player_board[r][c] = 2
                player_buttons[r][c].config(bg=HIT_COLOR)
                status_label.config(text=f"AI hit your ship at ({r}, {c})!")
            else:
                player_board[r][c] = 3
                player_buttons[r][c].config(bg=MISS_COLOR)
                status_label.config(text=f"AI missed at ({r}, {c}).")
            break

    if check_game_over(player_board):
        status_label.config(text="AI sank all your ships! You lose!")
        disable_all_buttons()

def on_ai_button_click(r, c):
    if placing_ships:
        status_label.config(text="Finish placing your ships first!")
        return

    if (r, c) in clicked_ai_cells:
        status_label.config(text="You already attacked this cell!")
        return

    clicked_ai_cells.add((r, c))

    if ai_board[r][c] == 1:
        ai_board[r][c] = 2
        ai_buttons[r][c].config(bg=HIT_COLOR)
        status_label.config(text=f"Hit at ({r}, {c})!")
    else:
        ai_board[r][c] = 3
        ai_buttons[r][c].config(bg=MISS_COLOR)
        status_label.config(text=f"Miss at ({r}, {c})!")

    ai_buttons[r][c].config(state="disabled")

    if check_game_over(ai_board):
        status_label.config(text="You sank all AI ships! You win!")
        disable_all_buttons()
        return

    root.after(500, ai_turn)

def on_player_button_click(r, c):
    global current_ship_index, placing_ships

    if not placing_ships:
        return

    length = ships[current_ship_index]

    # Check placement validity
    if ship_orientation == 'H':
        if c + length > GRID_SIZE or any(player_board[r][c + i] == 1 for i in range(length)):
            status_label.config(text="Invalid placement!")
            return
        for i in range(length):
            player_board[r][c + i] = 1
            player_buttons[r][c + i].config(bg=SHIP_COLOR)
    else:
        if r + length > GRID_SIZE or any(player_board[r + i][c] == 1 for i in range(length)):
            status_label.config(text="Invalid placement!")
            return
        for i in range(length):
            player_board[r + i][c] = 1
            player_buttons[r + i][c].config(bg=SHIP_COLOR)

    # Move to next ship
    current_ship_index += 1
    if current_ship_index < len(ships):
        status_label.config(text=f"Place your ship of length {ships[current_ship_index]}")
    else:
        placing_ships = False
        status_label.config(text="All ships placed! Start attacking the AI!")
        place_ships_randomly(ai_board, ships)

def show_preview(r, c):
    """Highlight cells for current ship placement."""
    if not placing_ships:
        return
    length = ships[current_ship_index]
    cells = []

    valid = True
    if ship_orientation == 'H':
        if c + length > GRID_SIZE:
            valid = False
        else:
            for i in range(length):
                cells.append((r, c + i))
                if player_board[r][c + i] == 1:
                    valid = False
    else:
        if r + length > GRID_SIZE:
            valid = False
        else:
            for i in range(length):
                cells.append((r + i, c))
                if player_board[r + i][c] == 1:
                    valid = False

    color = PREVIEW_OK_COLOR if valid else PREVIEW_BAD_COLOR
    for rr, cc in cells:
        player_buttons[rr][cc].config(bg=color)

def clear_preview():
    """Restore original colors after preview."""
    if not placing_ships:
        return
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if player_board[r][c] == 0:
                player_buttons[r][c].config(bg=PLAYER_COLOR)
            elif player_board[r][c] == 1:
                player_buttons[r][c].config(bg=SHIP_COLOR)

# Toggle orientation with spacebar
def toggle_orientation(event):
    global ship_orientation
    ship_orientation = 'V' if ship_orientation == 'H' else 'H'
    status_label.config(text=f"Orientation: {ship_orientation}")

root.bind("<space>", toggle_orientation)

# --- Replay functionality ---
def restart_game():
    global player_board, ai_board, clicked_ai_cells, clicked_player_cells
    global placing_ships, current_ship_index, ship_orientation

    # Reset game state
    player_board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    ai_board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    clicked_ai_cells.clear()
    clicked_player_cells.clear()
    placing_ships = True
    current_ship_index = 0
    ship_orientation = 'H'

    # Reset button colors & states
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            player_buttons[r][c].config(bg=PLAYER_COLOR, state="normal")
            ai_buttons[r][c].config(bg=AI_COLOR, state="normal")

    status_label.config(text=f"Place your ship of length {ships[current_ship_index]}")
    replay_button.grid_remove()  # Hide the replay button until next game over

# Create the Replay button (hidden at start)
replay_button = tk.Button(root, text="Replay Game", font=("Times New Roman", 14), command=restart_game)
replay_button.grid(row=2, column=0, columnspan=2, pady=10)
replay_button.grid_remove()

# --- Create boards ---
tk.Label(player_frame, text="Player Board").grid(row=0, column=0, columnspan=GRID_SIZE)
for r in range(GRID_SIZE):
    row_buttons = []
    for c in range(GRID_SIZE):
        btn = tk.Button(player_frame, width=CELL_SIZE, height=1, bg=PLAYER_COLOR,
                        command=lambda r=r, c=c: on_player_button_click(r, c))
        btn.grid(row=r+1, column=c)
        btn.bind("<Enter>", lambda e, r=r, c=c: show_preview(r, c))
        btn.bind("<Leave>", lambda e: clear_preview())
        row_buttons.append(btn)
    player_buttons.append(row_buttons)

tk.Label(ai_frame, text="AI Board").grid(row=0, column=0, columnspan=GRID_SIZE)
for r in range(GRID_SIZE):
    row_buttons = []
    for c in range(GRID_SIZE):
        btn = tk.Button(ai_frame, width=CELL_SIZE, height=1, bg=AI_COLOR,
                        command=lambda r=r, c=c: on_ai_button_click(r, c))
        btn.grid(row=r+1, column=c)
        row_buttons.append(btn)
    ai_buttons.append(row_buttons)

root.mainloop()
