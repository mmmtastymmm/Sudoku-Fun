from typing import Optional

import numpy as np


class Puzzle:

    def __init__(self, grid: Optional[np.ndarray] = None):
        """
        Makes a puzzle grid
        :param grid: A grid already holding some values. If passed this will be used as the grid if a correct size,
        otherwise an exception is raised
        """
        self.grid = np.zeros((9, 9), dtype=np.int8)

    def __str__(self):
        return str(self.grid)
