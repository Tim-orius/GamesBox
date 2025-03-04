import numpy as np


class Minefield:
    def __init__(self, field_size:tuple[int, int], percent_mines:int):
        """Representation for a minefield for the game Minesweeper.

        :param field_size: Size of the field (height x width)
        :param percent_mines: Amount of mines in percent (0 - 100)
        """
        self.field = None
        self.marker_field = None

        self.field_size = field_size
        self.amount_mines = max(1, int(field_size[0]*field_size[1] * percent_mines/100))
        self.mines_left = self.amount_mines

        self.setup()

    def setup(self):
        """ """

        self.field = np.zeros(shape=self.field_size, dtype=int)
        self.marker_field = np.zeros(shape=self.field_size, dtype=int)

        self.spawn_mines()
        self.setup_hints()

    def spawn_mines(self):
        """ """
        spawn_positions = np.argwhere(self.field == 0)
        selection = np.random.choice(range(len(spawn_positions)), size=self.amount_mines, replace=False)

        for index in selection:
            x, y = spawn_positions[index]
            # 1 marks a mine during spawning, will later be replaced with a 9
            self.field[x][y] = 1

    def setup_hints(self):
        """ """
        padded_field = np.pad(self.field, ((1, 1), (1, 1)), mode='constant', constant_values=0)

        # Kernel of ones
        kernel = np.ones(shape=(3,3), dtype=int)
        kernel[1][1] = 0
        m, n = kernel.shape
        x, y = self.field_size

        for ii in range(x):
            for jj in range(y):
                if self.field[ii][jj] == 1:
                    # Replace mine marker with 9 instead of 1 since 1 is now a hint marker
                    self.field[ii][jj] = 9
                else:
                    # Basic convolution operation to count mines at neighbouring positions
                    region = padded_field[ii:ii + m, jj:jj + n]
                    hint = np.sum(region * kernel)
                    self.field[ii][jj] = hint

        self.amount_mines = len(np.argwhere(self.field == 9))

    def action(self, x, y, flag):
        """Handler for action events on a field position

        :param x: X coordinate for the clicked box
        :param y: Y coordinate for the clicked box
        :param flag: Flag to flag if a flag is to be set. (True -> place flag; False -> sweep field)
        """
        if flag:
            self.flag(x, y)
            return None
        else:
            return self.sweep(x, y)


    def flag(self, x, y):
        """Toggle flag on position (x, y)

        :param x: X coordinate
        :param y: Y coordinate
        """
        marker_val = self.marker_field[x][y]
        # Markers: 0 -> hidden tile, 1 -> revealed tile, -1 -> flagged tile
        if marker_val == 0:
            self.marker_field[x][y] = -1
        elif marker_val < 0:
            self.marker_field[x][y] = 0
        else:
            return

    def sweep(self, x, y):
        """Sweep position (x, y)

        :param x: X coordinate
        :param y: Y coordinate
        :return: Whether a mine was hit
        """
        if self.field[x][y] == 9:
            self.reveal_all()
            self.marker_field[x][y] = 99
            return True
        else:
            self.sweep_field(x, y)
            return False

    def sweep_field(self, x, y):
        """Recursive function to sweep the field around the given coordinates.

        :param x: X coordinate
        :param y: Y coordinate
        """
        # Bounds check
        if x not in range(0, self.field_size[0]) or y not in range(0, self.field_size[1]):
            return

        value = self.field[x][y]
        marker_value = self.marker_field[x][y]
        if value > 8 or marker_value > 0:
            return

        self.marker_field[x][y] = 1

        if value == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        self.sweep_field(x + dx, y + dy)

    def check_finish(self):
        """Check if the minefield has been swept completely and all mines are flagged.

        :return: whether all hint-tiles have been revealed and only mines are left uncovered.
        :rtype: bool
        """
        # All revealed tiles: any tile not revealed (marker < 1) and not a mine (field < 9)
        hints_unrevealed = np.any((self.marker_field < 1) & (self.field < 9))

        if not hints_unrevealed:
            return True
        return False

    def reveal_all(self):
        self.marker_field = np.ones_like(self.marker_field)
