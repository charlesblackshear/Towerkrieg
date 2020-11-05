import towerkrieg
import tkinter as tk


class GUI:
    selected_square = None
    legal_moves = None
    images = {}
    border_color = "#b35900"
    square_color = "#999966"
    accent = "yellow"
    rows = 20
    columns = 20
    square_size = 32

    def __init__(self, parent, tkriegboard):
        self.tkriegboard = tkriegboard
        self.parent = parent

        # Build Menu
        self.menubar = tk.Menu(parent)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New Game", command=self.new_game)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.parent.config(menu=self.menubar)

        # Build Frame
        self.btmfrm = tk.Frame(parent, height=64)
        self.info_label = tk.Label(self.btmfrm,
                                text="   Black has first move   ",
                                fg=self.square_color)
        self.info_label.pack(side=tk.RIGHT, padx=8, pady=5)
        self.btmfrm.pack(fill="x", side=tk.BOTTOM)

        canvas_width = self.columns * self.square_size
        canvas_height = self.rows * self.square_size
        self.canvas = tk.Canvas(parent, width=canvas_width,
                               height=canvas_height)
        self.canvas.pack(padx=8, pady=8)
        self.show_gameboard()
        self.canvas.bind("<Button-1>", self.mouse_selection)

    def new_game(self):
        self.tkriegboard.initialize_board()
        self.show_gameboard()
        self.show_gamepieces()
        self.info_label.config(text="   Black has first move   ", fg='red')

    def mouse_selection(self, event):
        if self.tkriegboard.get_status() in ['black_victory','white_victory']:
            # Match has already been won
            return

        col_size = row_size = self.square_size
        # Obtain mouse click input
        selected_column = int(event.x / col_size)
        selected_row = int(event.y / row_size)

        if self.selected_square:
            if self.selected_square != (selected_row, selected_column):
                # Destination for 3 x 3 gamepiece is being selected, not the gamepiece itself. Perform move
                self.move(self.selected_square, (selected_row, selected_column))
            self.selected_square = None
            self.legal_moves = None
            self.show_gameboard()
            self.show_gamepieces()
        else:
            # 3 x 3 gamepiece is being selected
            self.show_moves(selected_row, selected_column)
            self.show_gameboard()

    def move(self, p1, p2):
        move_result = self.tkriegboard.make_move(p1, p2, 1)     # axes = 1 bypasses axes conversion method
        turn = 'Black' if self.tkriegboard.get_turn() == 'x' else 'White'
        color = 'White' if self.tkriegboard.get_turn() == 'x' else 'Black'
        # Convert position to game notation (i.e. (2,2) represented as 'C3')
        pos1 = chr(p1[1]+65) + str(20-p1[0])
        pos2 = chr(p2[1]+65) + str(20-p2[0])

        # Populate informational text box at bottom of board
        if self.tkriegboard.get_status() == 'white_victory':
            self.info_label['text'] = f'{color} : {pos1}->{pos2}    White won!'
            self.info_label['fg'] = 'black'
        elif self.tkriegboard.get_status() == 'black_victory':
            self.info_label['text'] = f'{color} : {pos1}->{pos2}    Black won!'
            self.info_label['fg'] = 'black'
        elif move_result:
            self.info_label['text'] = f'{color} : {pos1}->{pos2}    {turn}\'s turn'

    def show_moves(self, row, col):
        board = self.tkriegboard.get_gameboard()
        footprint, footprint_none = self.tkriegboard.make_footprint(board, row, col)
        if (footprint, footprint_none) != ([-1], [-1]) and len(footprint) > 0:
            self.selected_square = (row, col)
            self.legal_moves = self.tkriegboard.moves_available(row, col)

    def show_gameboard(self):
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = (col * self.square_size)
                # Recall: In game coordinate system, first row is Row 20
                y1 = ((19 - row) * self.square_size)
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                if (self.legal_moves is not None and (19-row, col) in self.legal_moves):
                    # Highlight squares of eligible moves
                    self.canvas.create_rectangle(x1, y1, x2, y2,
                                                 fill=self.accent,
                                                 tags="area")
                else:
                    # Create squares in game area (#999966) and borders (#b35900)
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.border_color if row*col*(row-19)*(col-19) == 0 else self.square_color,
                                                 tags="area")
        self.canvas.tag_raise("occupied")
        self.canvas.tag_lower("area")

    def show_gamepieces(self):
        self.canvas.delete("occupied")
        board = self.tkriegboard.get_gameboard()
        for y, row in enumerate(board):
            for x, piece in enumerate(row):
                if piece == 'x':
                    filename = 'towerkrieg_images/black.png'
                elif piece == 'o':
                    filename = 'towerkrieg_images/white.png'
                else:
                    continue
                piecename = "%s%s%s" % (piece, str(x).zfill(2), str(y).zfill(2))
                if filename not in self.images:
                    self.images[filename] = tk.PhotoImage(file=filename)
                self.canvas.create_image(0, 0, image=self.images[filename],
                                         tags=(piecename, "occupied"),
                                         anchor="c")
                y0 = (y * self.square_size) + int(self.square_size / 2)
                x0 = (x * self.square_size) + int(self.square_size / 2)
                self.canvas.coords(piecename, x0, y0)


def main(tkriegboard):
    root = tk.Tk()
    root.title("Towerkrieg")
    gui = GUI(root, tkriegboard)
    gui.show_gameboard()
    gui.show_gamepieces()
    root.mainloop()


if __name__ == "__main__":
    game = towerkrieg.TowerkriegGame()
    main(game)
