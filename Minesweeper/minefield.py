import numpy as np


class Minefield:
    def __init__(self, field_size:tuple[int, int], percent_mines:int):
        """Representation for a minefield for the game Minesweeper.

        :param field_size: Size of the field (height x width)
        :param percent_mines: Amount of mines in percent (0 - 100)
        """
        self.field = None
        self.field_size = field_size
        self.amount_mines = max(1, int(field_size[0]*field_size[1] * percent_mines/100))
        self.setup()

    def setup(self):
        """ """

        self.field = np.zeros(shape=self.field_size, dtype=int)

        self.spawn_mines()
        self.setup_hints()

    def spawn_mines(self):
        """ """
        spawn_positions = np.argwhere(self.field == 0)
        selection = np.random.choice(range(len(spawn_positions)), self.amount_mines)

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
        self.field[x][y] *= -1

    def sweep(self, x, y):
        """Sweep position (x, y)

        :param x: X coordinate
        :param y: Y coordinate
        :return: Whether a mine was hit
        """
        if self.field[x][y] == 9:
            self.field += 100
            self.field[x][y] = 99
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
        if value > 8 or value < -8:
            return

        value = abs(value) + 100
        self.field[x][y] = value

        if value == 100:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        self.sweep_field(x + dx, y + dy)

    def check_finish(self):
        """ """
        not_revealed = np.argwhere((self.field >= 0) & (self.field <= 8))
        if len(not_revealed) > 0:
            return False
        return True
