import tkinter as tk
from tkinter import messagebox as mb
from tkinter.font import Font

from minefield import Minefield
from colormapper import ColorMapper


class MinesweeperUI:
    def __init__(self, root):
        self.root = root
        self.minefield = None
        self.color_mapper = ColorMapper()
        self.frame = []

        self.asset_flag = tk.PhotoImage(file="assets/img/flag.png")
        self.asset_mine = tk.PhotoImage(file="assets/img/mine.png")
        self.tile_size_px = 40

        self.use_images_ui = False

        self.root.bind("<Escape>", self.restart())

    def init_screen(self):
        """Open the game options window."""
        # Create secondary (or popup) window.
        self.init_window = tk.Toplevel()
        self.init_window.title("Select game size")
        self.init_window.minsize(400, 200)

        self.small_board = tk.Button(self.init_window,
                                     text="Small Board\n 8 x 8 \n 10 Mines",
                                     command=lambda: self.setup_game((8, 8), 16),
                                     bg="#FFFFFF", borderwidth=5, anchor="center")
        self.medium_board = tk.Button(self.init_window,
                                     text="Medium Board\n 16 x 16 \n 40 Mines",
                                     command=lambda: self.setup_game((16, 16), 16),
                                      bg="#FFFFFF", borderwidth=5, anchor="center")
        self.large_board = tk.Button(self.init_window,
                                     text="Large Board\n 30 x 30 \n 180 Mines",
                                     command=lambda: self.setup_game((30, 30), 20),
                                     bg="#FFFFFF", borderwidth=5, anchor="center")
        self.custom_board = tk.Button(self.init_window,
                                     text="Custom Minefield",
                                     command=lambda: self.custom_game(),
                                      bg="#FFFFFF", borderwidth=5, anchor="center")

        self.small_board.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.medium_board.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.large_board.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.custom_board.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    def setup_game(self, board_shape:tuple[int, int], percent_mines:int):
        """Setup for game

        :param board_shape: Shape of the board (height x width)
        :param amount_mines: Number of mines on the field.
        """

        self.init_window.destroy()

        # Set geometry
        geometry = str(board_shape[0]*self.tile_size_px)+"x"+str(board_shape[1]*self.tile_size_px)
        self.root.geometry(geometry)

        # Create minefield
        self.minefield = Minefield(field_size=board_shape, percent_mines=percent_mines)

        # Config & setup
        self.grid_config()
        self.ui_setup()

    def ui_setup(self):
        """ """
        for ii in range(self.minefield.field_size[0]):
            self.frame.append([])
            for jj in range(self.minefield.field_size[1]):
                field_element = tk.Label(self.root,
                                         text="",
                                         bg="#FFFFFF",
                                         borderwidth=5,
                                         height=self.tile_size_px,
                                         width=self.tile_size_px
                                         )
                # Bind buttons
                field_element.bind("<Button-1>", lambda event, x=ii, y=jj: self.click(x, y, False))
                field_element.bind("<Button-3>", lambda event, x=ii, y=jj: self.click(x, y, True))

                field_element.grid(row=ii, column=jj, padx=5, pady=5)
                self.frame[ii].append(field_element)

    def grid_config(self):
        """Set the grid configuration."""
        # Configure rows and columns
        for ii in range(self.minefield.field_size[0]):
            self.root.grid_rowconfigure(ii, weight=1)
        for jj in range(self.minefield.field_size[1]):
            self.root.grid_columnconfigure(jj, weight=1)

    def restart(self):
        for frame_row in self.frame:
            for label in frame_row:
                label.destroy()

        self.frame = []
        self.init_screen()

    def custom_game(self):
        mb.showinfo("Not implemented yet.")

    def click(self, x, y, flag:bool):
        """Handler for click event on a field position

        :param x: X coordinate for the clicked box
        :param y: Y coordinate for the clicked box
        :param flag: Flag to flag if a flag is to be set. (True -> right click / place flag; False -> left click / sweep field)
        """

        result = self.minefield.action(x, y, flag)
        self.update(reveal=result)
        if result:
            self.end()
        else:
            self.check_finish()

    def update(self, reveal:bool=False):
        """UI Update method. Updates the ui tiles after an action was performed. Only affects UI!

        :param reveal: If all values should be revealed (game over / finished)
        """
        print(self.minefield.field)
        for xx in range(self.minefield.field_size[0]):
            for yy in range(self.minefield.field_size[1]):
                value = self.minefield.field[xx][yy]
                # Undo set flags
                if reveal and value < 0:
                    value *= -1

                if value < 0 or value == 109 or value == 99:
                    if self.use_images_ui:
                        img = self.retrieve_image(value)
                        self.frame[xx][yy].config(text="", image=img, bg=self.color_mapper.get_color(value))
                        self.frame[xx][yy].image = img
                    else:
                        display_value = self.retrieve_text(value)
                        font = Font(self.root, size=16, weight="bold")
                        self.frame[xx][yy].config(text=display_value,
                                                  font=font,
                                                  bg=self.color_mapper.get_color(value)
                                                  )
                else:
                    if 0 <= value < 10:
                        # Empty field / minefield, not yet swept
                        display_value = ""
                        value -= 100
                    else:
                        # Hints
                        print(value)
                        value = value % 100
                        display_value = str(value)

                    font = Font(self.root, size=16, weight="bold")
                    self.frame[xx][yy].config(text=display_value,
                                              font=font,
                                              bg=self.color_mapper.get_color(value)
                                              )

    def retrieve_image(self, value):
        """ """
        if value < 0:
            # Flag
            return self.asset_flag.copy()
        elif value == 109:
            # Reveal mine
            return self.asset_mine.copy()
        elif value == 99:
            # Mine was clicked
            return self.asset_mine.copy()
        else:
            return

    def retrieve_text(self, value):
        """ """
        if value < 0:
            # Flag
            return "F"
        elif value == 109:
            # Reveal mine
            return "X"
        elif value == 99:
            # Mine was clicked
            return "X"
        else:
            return

    def check_finish(self):
        """ """
        finished = self.minefield.check_finish()
        if finished:
            answer = mb.askyesno("Minefield cleared!", "New game?")
            if answer:
                self.restart()

    def end(self):
        """ """
        answer = mb.askyesno("Game Over", "New game?")
        if answer:
            self.restart()

def main():
    root = tk.Tk()
    mines = MinesweeperUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
