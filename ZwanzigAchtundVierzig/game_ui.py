import tkinter as tk

from tkinter import messagebox

from colormapper import ColorMapper
from game_grid import GameGrid


class GameUI:
    def __init__(self, root, grid: GameGrid):
        self.root = root
        self.grid = grid
        self.frame = []
        self.color_mapper = ColorMapper()
        self.setup()

    def restart(self):
        for frame_row in self.frame:
            for label in frame_row:
                label.destroy()

        self.frame = []


    def setup(self):
        self.scoreboard = tk.Label(self.root, text="Score: 0", anchor="center")
        self.scoreboard.grid(row=0, columnspan=self.grid.frame_size, sticky="nsew", padx=5, pady=5)

        for ii in range(self.grid.frame_size):
            self.frame.append([])
            for jj in range(self.grid.frame_size):
                field_element = tk.Label(self.root, text="0", bg="#FFFFFF", borderwidth=5, anchor="center")
                field_element.grid(row=ii+1, column=jj, sticky="nsew", padx=5, pady=5)
                self.frame[ii].append(field_element)

        self.update()

    def update(self):
        self.scoreboard.config(text="Score: "+str(self.grid.score))
        for xx in range(self.grid.frame_size):
            for yy in range(self.grid.frame_size):
                value = self.grid.field[xx][yy]
                self.frame[xx][yy].config(text=str(value), bg=self.color_mapper.get_value_color(value))

    def grid_config(self):
        """Set the grid configuration."""
        # Configure rows and columns
        self.root.grid_rowconfigure(0, weight=1)
        for i in range(self.grid.frame_size):
            self.root.grid_rowconfigure(i+1, weight=3)
            self.root.grid_columnconfigure(i, weight=3)

    def end(self):
        messagebox.showinfo("Game Over", "No empty spots available. Score: " + str(self.grid.score))
