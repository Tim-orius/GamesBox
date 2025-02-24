import numpy as np


class MaskCreator:

    mask = np.zeros((9, 9), dtype=int)

    def __init__(self):
        """ """

    def add_mask_entry(self):
        """ """

        zeros = np.argwhere(self.mask == 0)
        indices = np.ravel_multi_index([zeros[:, 0], zeros[:, 1]], self.mask.shape)

        idx = np.random.choice(indices)

        self.mask[np.unravel_index(idx, self.mask.shape)] = 1

    def generate_start_mask(self, start_entries=20):
        """ """

        for ii in range(start_entries):
            self.add_mask_entry()

    def remove_mask_entry(self, ii, jj):
        self.mask[ii][jj] = 0