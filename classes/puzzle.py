from typing import Optional

import numpy as np


def is_legal_set(numbers: np.ndarray) -> bool:
    numbers = numbers.flatten()
    num_zeros = np.count_nonzero(numbers == 0)
    number_set = set(numbers)
    number_set.discard(0)
    return num_zeros + len(number_set) == 9


class Puzzle:

    def __init__(self, grid: Optional[np.ndarray] = None):
        """
        Makes a puzzle grid
        :param grid: A grid already holding some values. If passed this will be used as the grid if a correct size and
        contains values [0-9], otherwise an exception is raised
        """
        if grid is None:
            self.puzzle_grid = np.zeros((9, 9), dtype=np.int8)
        else:
            self.puzzle_grid = grid
        # Now make sure the grid is valid, and if not raise an exception
        if not self.is_puzzle_valid():
            raise ValueError("The input grid was not valid")

    def __str__(self) -> str:
        return str(self.puzzle_grid)

    def is_puzzle_empty(self) -> bool:
        return np.all(self.puzzle_grid == 0)

    def get_square(self, row, col) -> np.ndarray:
        return self.puzzle_grid[row * 3:row * 3 + 3, col * 3:col * 3 + 3]

    def is_puzzle_valid(self) -> bool:
        # Check only has legal values
        if not np.all((self.puzzle_grid >= 0) & (self.puzzle_grid <= 9)):
            return False
        # Check has the right shape
        if not np.all(np.equal(self.puzzle_grid.shape, (9, 9))):
            return False
        # Check all squares legal
        for row in range(3):
            for col in range(3):
                if not is_legal_set(self.get_square(row, col)):
                    return False
        # Check all rows legal
        for row in range(9):
            if not is_legal_set(self.puzzle_grid[row, :]):
                return False
        # Check all cols legal
        for col in range(9):
            if not is_legal_set(self.puzzle_grid[:, col]):
                return False

        # Passed all checks so it is valid
        return True

    @classmethod
    def make_solvable_puzzle(cls):
        pass
