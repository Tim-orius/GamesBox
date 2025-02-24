import tkinter as tk
import numpy as np

class GameGrid:
    def __init__(self, frame_size:int=4, base_number:int=2, percent_double_base_on_spawn=10):
        """

        :param frame_size: Initial size of the game frame.
        :param base_number: Base number for the game.
        :param percent_double_base_on_spawn: Probability for 2*base_number to spawn in the game field.
        """
        self.frame_size = frame_size
        self.base_number = base_number
        self.percent_double_base_on_spawn = percent_double_base_on_spawn

        self.field = None
        self.new_field = None
        self.score = 0

        self.restart()

    def restart(self, spawn_no:int=2):
        self.score = 0
        self.field = np.zeros((self.frame_size, self.frame_size), dtype=int)
        self.spawn(spawn_no)

    def spawn(self, spawn_no:int, custom_value=None):
        """

        :param custom_value: A custom value to insert
        :return: Whether the spawning was successful
        """
        spawn_positions = np.argwhere(self.field == 0)
        if spawn_positions.size < spawn_no:
            return False, self.score  # Game over

        for ii in range(spawn_no):
            pos = np.random.choice(range(len(spawn_positions)))
            x, y = spawn_positions[pos]

            if custom_value is not None:
                self.field[x][y] = custom_value
            else:
                rand_num = np.random.randint(0, 100)
                spawn_value = self.base_number * 2 if rand_num < self.percent_double_base_on_spawn else self.base_number
                self.field[x][y] = spawn_value

        return True, None

    def move(self, direction:int):
        self.stack(direction)
        if not self.check_changes():
            # No change to the board
            return False

        self.field = self.new_field.copy()
        success, _ = self.spawn(spawn_no=1)

        return success


    def stack(self, direction:int, temp_field=None):
        """Stack the numbers in the grid in accordance with a given direction. The numbers are stacked back to front
        in perspective to the direction, e.g. [0, 2, 2, 2] is stacked to [0, 0, 2, 4].

        :param direction: Directions are encoded as: 0 -> UP, 1 -> Down, 2 -> Left, 3 -> Right
        :param temp_field: Instance of a field to perform the stack on. If None is given, self.field will be used.
        :return: new field as numpy array
        """
        if temp_field is None:
            temp_field = self.field.copy()
            expect_return = False
        else:
            expect_return = True

        new_field = np.zeros_like(temp_field)

        # If UP or DOWN transpose field
        if direction in [0, 1]:
            temp_field = temp_field.T

        for index, row in enumerate(temp_field):
            non_zeros = row[row!=0].tolist()
            new_row = []
            num_non_zero = len(non_zeros)

            # If DOWN o RIGHT reverse the list
            if direction in [1, 3]:
                non_zeros = non_zeros[::-1]

            skip = False
            for ii, v in enumerate(non_zeros):
                if skip:
                    skip = False
                    continue

                # Stacking logic
                if ii < num_non_zero-1 and non_zeros[ii] == non_zeros[ii+1]:
                    new_row.append(non_zeros[ii] * 2)
                    self.score += non_zeros[ii]*2
                    skip = True
                else:
                    new_row.append(non_zeros[ii])

            new_row += [0] * (self.frame_size - len(new_row))
            # If DOWN o RIGHT reverse the list
            if direction in [1, 3]:
                new_row = new_row[::-1]

            new_field[index] = new_row

        # If UP or DOWN transpose field
        if direction in [0, 1]:
            new_field = new_field.T

        if expect_return:
            return new_field.copy()
        else:
            self.new_field = new_field.copy()

    def check_changes(self):
        return not (self.field == self.new_field).all()

    def check_game_over(self):
        for ii in range(4):
            test_field = self.field.copy()
            new_field = self.stack(direction=ii, temp_field=test_field)

            if not (test_field == new_field).all():
                return False

        return True

    def copy(self):
        return self.field.copy()
