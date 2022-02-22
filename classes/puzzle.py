from typing import Optional

import numpy as np


class Puzzle:

    def __init__(self, grid: Optional[np.ndarray] = None):
        """
        Makes a puzzle grid
        :param grid: A grid already holding some values. If passed this will be used as the grid if a correct size and
        contains values [0-9], otherwise an exception is raised
        """
        if grid is None:
            self.grid = np.zeros((9, 9), dtype=np.int8)
        else:
            self.grid = grid
        # Now make sure the grid is valid, and if not raise an exception
        if not self.is_puzzle_valid():
            raise ValueError("The input grid was not valid")

    def __str__(self):
        return str(self.grid)

    def is_puzzle_empty(self):
        return np.all(self.grid == 0)

    def is_puzzle_valid(self):
        return np.all((self.grid >= 0) & (self.grid <= 9)) and np.all(np.equal(self.grid.shape, (9, 9)))
