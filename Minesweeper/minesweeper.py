import tkinter as tk
from mines_ui import MinesweeperUI


def main():
    root = tk.Tk()
    mines = MinesweeperUI(root, images_in_ui=False)
    root.mainloop()


if __name__ == "__main__":
    main()