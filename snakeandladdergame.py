import tkinter as tk
import random
BOARD_SIZE = 10
CELL_SIZE = 60
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE
snakes = {
    99: 54,
    70: 55,
    52: 42,
    25: 2,
    95: 72
}
ladders = {
    6: 25,
    11: 40,
    60: 85,
    46: 90,
    17: 69
}
class SnakeAndLadder:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake and Ladder 🐍🎲")
        
        self.canvas = tk.Canvas(root, width=WINDOW_SIZE, height=WINDOW_SIZE, bg="white")
        self.canvas.pack()
        self.draw_board()
        self.players = {"Player 1": 0, "Player 2": 0}
        self.player_tokens = {
            "Player 1": self.canvas.create_oval(5, 5, 25, 25, fill="blue"),
            "Player 2": self.canvas.create_oval(30, 5, 50, 25, fill="red")
        }

        self.turn_order = list(self.players.keys())
        self.current_player_index = 0
        self.roll_button = tk.Button(root, text="🎲 Roll Dice", command=self.play_turn, font=("Arial", 14))
        self.roll_button.pack(pady=10)
        self.status = tk.Label(root, text="Player 1's Turn", font=("Arial", 14))
        self.status.pack()

    def draw_board(self):
        num = 100
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightyellow")
                self.canvas.create_text(x1+30, y1+30, text=str(num))
                num -= 1
        for head, tail in snakes.items():
            self.draw_line(head, tail, "red")
        for start, end in ladders.items():
            self.draw_line(start, end, "green")

    def draw_line(self, start, end, color):
        x1, y1 = self.get_coords(start)
        x2, y2 = self.get_coords(end)
        self.canvas.create_line(x1, y1, x2, y2, width=3, fill=color, arrow=tk.LAST)

    def get_coords(self, pos):
        row = (100 - pos) // BOARD_SIZE
        col = (pos - 1) % BOARD_SIZE
        if (row % 2 == 0):
            col = BOARD_SIZE - 1 - col
        x = col * CELL_SIZE + CELL_SIZE // 2
        y = row * CELL_SIZE + CELL_SIZE // 2
        return x, y

    def play_turn(self):
        player = self.turn_order[self.current_player_index]
        roll = random.randint(1, 6)
        self.status.config(text=f"{player} rolled a {roll}")

        new_pos = self.players[player] + roll
        if new_pos <= 100:
            self.players[player] = new_pos

            if new_pos in ladders:
                self.players[player] = ladders[new_pos]
                self.status.config(text=f"{player} climbed a ladder to {self.players[player]}!")
            elif new_pos in snakes:
                self.players[player] = snakes[new_pos]
                self.status.config(text=f"{player} got bitten by a snake! Back to {self.players[player]}")
        x, y = self.get_coords(self.players[player])
        if player == "Player 1":
            self.canvas.coords(self.player_tokens[player], x-15, y-15, x+15, y+15)
        else:
            self.canvas.coords(self.player_tokens[player], x-10, y-10, x+10, y+10)
        if self.players[player] == 100:
            self.status.config(text=f"🎉 {player} wins! 🎉")
            self.roll_button.config(state="disabled")
            return
        self.current_player_index = (self.current_player_index + 1) % len(self.turn_order)
        next_player = self.turn_order[self.current_player_index]
        self.status.config(text=f"{player} rolled {roll}. Now it's {next_player}'s turn.")
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeAndLadder(root)
    root.mainloop()
