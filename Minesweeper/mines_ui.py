import tkinter as tk
from tkinter import messagebox as mb
from tkinter.font import Font

from minefield import Minefield
from colormapper import ColorMapper


class MinesweeperUI:
    def __init__(self, root, images_in_ui:bool=True):
        """UI Element for Minesweeper game.

        :param root: tkinter instance
        :param images_in_ui: Whether to display the images in /assets/img/ for flags and mines (otherwise use "F" and "X")
        """
        self.root = root
        self.use_images_ui = images_in_ui

        self.minefield = None
        self.color_mapper = ColorMapper()
        self.frame = []

        self.asset_flag = tk.PhotoImage(file="assets/img/flag.png")
        self.asset_mine = tk.PhotoImage(file="assets/img/mine.png")
        self.tile_size_px = 40

        self.small_board = tk.Button(self.root,
                                     text="Small Board\n 8 x 8 \n 10 Mines",
                                     command=lambda: self.setup_game((8, 8), 16),
                                     bg="#FFFFFF", borderwidth=5, anchor="center")
        self.medium_board = tk.Button(self.root,
                                      text="Medium Board\n 16 x 16 \n 40 Mines",
                                      command=lambda: self.setup_game((16, 16), 16),
                                      bg="#FFFFFF", borderwidth=5, anchor="center")
        self.large_board = tk.Button(self.root,
                                     text="Large Board\n 30 x 30 \n 180 Mines",
                                     command=lambda: self.setup_game((30, 30), 20),
                                     bg="#FFFFFF", borderwidth=5, anchor="center")
        self.custom_board = tk.Button(self.root,
                                      text="Custom Minefield",
                                      command=lambda: self.custom_game(),
                                      bg="#FFFFFF", borderwidth=5, anchor="center")

        self.root.bind("<Escape>", lambda event: self.restart())
        self.init_screen()

    def init_screen(self):
        """Open the game options window."""
        # Create secondary (or popup) window.
        self.root.title("Select game size")
        self.root.geometry("400x200")

        self.small_board.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.medium_board.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.large_board.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.custom_board.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    def setup_game(self, board_shape:tuple[int, int], percent_mines:int):
        """Setup for game logic

        :param board_shape: Shape of the board (height x width)
        :param amount_mines: Number of mines on the field.
        """

        self.small_board.grid_remove()
        self.medium_board.grid_remove()
        self.large_board.grid_remove()
        self.custom_board.grid_remove()

        self.root.title("Minesweeper")
        # Set geometry
        geometry = str(board_shape[0]*self.tile_size_px)+"x"+str(board_shape[1]*self.tile_size_px)
        self.root.geometry(geometry)

        # Create minefield
        self.minefield = Minefield(field_size=board_shape, percent_mines=percent_mines)

        # Config & setup
        self.grid_config()
        self.ui_setup()

    def grid_config(self):
        """Set the grid configuration."""
        self.root.grid_rowconfigure(0, weight=1)
        # Configure rows and columns
        for ii in range(self.minefield.field_size[0]):
            self.root.grid_rowconfigure(ii+1, weight=1)
        for jj in range(self.minefield.field_size[1]):
            self.root.grid_columnconfigure(jj, weight=1)

    def ui_setup(self):
        """Setup for the game UI"""
        # Scoreboard
        self.scoreboard = tk.Label(self.root,
                                   text="Mines left: "+str(self.minefield.mines_left),
                                   borderwidth=5,
                                   anchor='n',
                                   height=self.tile_size_px
                                   )
        #self.scoreboard.grid(row=0, columnspan=self.minefield.field_size[1], padx=5, pady=5, sticky="new")

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

                field_element.grid(row=ii+1, column=jj, padx=5, pady=5)
                self.frame[ii].append(field_element)

    def restart(self):
        """Restart a game. Delete all currently displayed widgets and re-trigger initialisation screen."""
        self.scoreboard.destroy()

        for frame_row in self.frame:
            for label in frame_row:
                label.destroy()

        self.frame = []
        self.init_screen()

    def custom_game(self):
        """ """
        self.custom_game_window = tk.Toplevel()
        self.custom_game_window.title("Custom Game")

        # Create labels and entry fields
        height_label = tk.Label(self.custom_game_window, text="Height:")
        height_label.grid(row=0, column=0, padx=10, pady=10)
        self.height_entry = tk.Entry(self.custom_game_window)
        self.height_entry.grid(row=0, column=1, padx=10, pady=10)

        width_label = tk.Label(self.custom_game_window, text="Width:")
        width_label.grid(row=1, column=0, padx=10, pady=10)
        self.width_entry = tk.Entry(self.custom_game_window)
        self.width_entry.grid(row=1, column=1, padx=10, pady=10)

        mines_label = tk.Label(self.custom_game_window, text="Mine Percentage (0-100):")
        mines_label.grid(row=2, column=0, padx=10, pady=10)
        self.mines_entry = tk.Entry(self.custom_game_window)
        self.mines_entry.grid(row=2, column=1, padx=10, pady=10)

        # Create the 'Start Game' button
        start_button = tk.Button(self.custom_game_window, text="Start Game", command=self.start_custom_game)
        start_button.grid(row=3, columnspan=2, padx=10, pady=10)

    def start_custom_game(self):
        """ """
        height_inp = self.height_entry.get()
        width_inp = self.width_entry.get()
        percent_inp = self.mines_entry.get()

        if not(height_inp.isdigit() and width_inp.isdigit() and percent_inp.isdigit()):
            mb.showerror("Invalid values", "Please input valid, whole numbers.")
            return

        height = int(height_inp)
        width = int(width_inp)
        percent = int(percent_inp)

        if height <= 0 or width <= 0:
            mb.showerror("Invalid size", "Height and Width must be positive integers.")
            return

        if percent < 0 or percent > 100:
            mb.showerror("Invalid percent value", "Mine percentage must be between 0 and 100.")
            return

        self.custom_game_window.destroy()

        # Set up the game with the user-defined parameters
        self.setup_game((height, width), percent)

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
        print(self.minefield.marker_field)
        self.scoreboard.config(text="Mines left: "+str(self.minefield.mines_left))

        if reveal:
            self.minefield.reveal_all()

        for xx in range(self.minefield.field_size[0]):
            for yy in range(self.minefield.field_size[1]):
                value = self.minefield.field[xx][yy]
                marker_value = self.minefield.marker_field[xx][yy]

                if marker_value < 0 or (marker_value > 0 and value > 8):
                    # Flag or mine
                    if self.use_images_ui:
                        img = self.retrieve_image(marker_value)
                        self.frame[xx][yy].config(text="", image=img, bg=self.color_mapper.get_color(0))
                        self.frame[xx][yy].image = img
                    else:
                        display_value = self.retrieve_text(marker_value)
                        font = Font(self.root, size=16, weight="bold")
                        self.frame[xx][yy].config(text=display_value,
                                                  font=font,
                                                  bg=self.color_mapper.get_color(0)
                                                  )
                else:
                    # Undiscovered tile / hint tile
                    if marker_value == 0:
                        # Empty field / minefield, not yet swept
                        display_value = ""
                        value = 0
                    else:
                        # Hints
                        display_value = str(value)

                    font = Font(self.root, size=16, weight="bold")
                    if self.use_images_ui:
                        self.frame[xx][yy].config(text=display_value,
                                                  image="",
                                                  font=font,
                                                  bg=self.color_mapper.get_color(value)
                                                  )
                        self.frame[xx][yy].image = None
                    else:
                        self.frame[xx][yy].config(text=display_value,
                                                  font=font,
                                                  bg=self.color_mapper.get_color(value)
                                                  )

    def retrieve_image(self, value):
        """ """
        if value < 0:
            # Flag
            return self.asset_flag.copy()
        elif value > 0:
            # Reveal mine
            return self.asset_mine.copy()
        else:
            return

    def retrieve_text(self, value):
        """ """
        if value < 0:
            # Flag
            return "F"
        elif value > 0:
            # Reveal mine
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
    # Set images_in_ui to True to use images
    mines = MinesweeperUI(root=root, images_in_ui=False)
    root.mainloop()


if __name__ == "__main__":
    main()
