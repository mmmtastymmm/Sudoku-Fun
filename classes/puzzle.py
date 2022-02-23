import random
from typing import Optional, Tuple, Iterable

import numpy as np


def is_legal_set(numbers: np.ndarray) -> bool:
    """
    Returns if the set of numbers is legal
    :param numbers: The numbers in the set
    :return: True if legal, false if illegal
    """
    numbers = numbers.flatten()
    num_zeros = np.count_nonzero(numbers == 0)
    number_set = set(numbers)
    number_set.discard(0)
    return num_zeros + len(number_set) == 9


def get_square_index(index):
    """
    Gets the index for the large square this belongs to
    :param index: The index into the whole puzzle
    :return: The index of the square
    """
    return index // 3


def make_puzzle_answer_key() -> 'Puzzle':
    puzzle = Puzzle()
    adjustments: list[Tuple[int, int]] = []
    bad_adjustments: dict[Tuple[int, int], list[int]] = {}
    while not puzzle.is_finished():
        spaces_possibilities: list[list[Tuple[int, int]]] = [[] for _ in range(10)]
        for row in range(9):
            for col in range(9):
                # Append this row col to the list with the number of options left for this spot
                spaces_possibilities[len(puzzle.get_options_for_index(
                    row, col, bad_adjustments.get((row, col), [])))].append((row, col))
        # look at the elements that have no options to see if any are still zero
        zero_options_list = spaces_possibilities.pop(0)
        blocked_cell = any(map(lambda x: puzzle.puzzle_grid[x[0], x[1]] == 0, zero_options_list))
        # Need to undo if everything is empty
        if blocked_cell:
            # Get the last move added
            last_move = adjustments.pop()
            # Get that guess's value
            bad_value = puzzle.puzzle_grid[last_move[0], last_move[1]]
            # Add a map element if not already there
            if last_move not in bad_adjustments:
                bad_adjustments[last_move] = []
            # add this bad guess, so we don't guess it again
            bad_adjustments[last_move].append(bad_value)
            # Put a zero back in the guess's spot, so we can update with a new value later
            puzzle.puzzle_grid[last_move[0], last_move[1]] = 0
            continue
        # We can still place numbers so guess again
        non_empty_lists = list(filter(lambda x: len(x) != 0, spaces_possibilities))
        first_non_empty = non_empty_lists[0]
        row_to_update, col_to_update = random.choice(first_non_empty)
        value_to_update_with = np.random.choice(list(
            puzzle.get_options_for_index(
                row_to_update, col_to_update, bad_adjustments.get((row_to_update, col_to_update), []))))
        puzzle.puzzle_grid[row_to_update, col_to_update] = value_to_update_with
        adjustments.append((row_to_update, col_to_update))
        print(puzzle)

    return puzzle


def make_solvable_puzzle() -> 'Puzzle':
    answer_key = make_puzzle_answer_key()
    puzzle = Puzzle(answer_key.puzzle_grid)
    indexes = []
    for i in range(9):
        for j in range(9):
            indexes.append((i, j))
    return answer_key


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
        pretty_puzzle = '_' * 19
        for i in range(9):
            pretty_puzzle += '\n|'
            for j in range(9):
                pretty_puzzle += str(self.puzzle_grid[i, j])
                if (j + 1) % 3 == 0:
                    pretty_puzzle += '|'
                else:
                    pretty_puzzle += ' '
            if (i + 1) % 3 == 0:
                pretty_puzzle += '\n|' + '_____+' * 2 + '_____|'
        return pretty_puzzle

    def is_puzzle_empty(self) -> bool:
        """
        Returns if no numbers are in the puzzle (ie all numbers are zero)
        :return: True if empty, false if at least one number is in the puzzle
        """
        return np.all(self.puzzle_grid == 0)

    def get_square(self, square_row, square_col) -> np.ndarray:
        """
        Gets a square given an index
        :param square_row: The square row
        :param square_col: The square col
        :return:
        """
        return self.puzzle_grid[square_row * 3:square_row * 3 + 3, square_col * 3:square_col * 3 + 3]

    def is_puzzle_valid(self) -> bool:
        """
        Checks to see if each row, col, and square has no conflict (two of the same numbers)
        :return: True if everything is ok, or false if something is illegal
        """
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

    def get_options_for_index(self, row, col, numbers_to_avoid: Optional[Iterable[int]] = None) -> set[int]:
        """
        Gets all remaining numbers that COULD go into an index based on the state of the puzzle
        :param row: the row of the element
        :param col: the col of the element
        :param numbers_to_avoid: Optional iterable of other numbers to exclude
        :return: A set of numbers which could be placed into the spot without conflicting anything in the puzzle so far
        """
        if self.puzzle_grid[row, col] != 0:
            return set()
        already_taken = set(self.puzzle_grid[row, :])
        already_taken = already_taken.union(self.puzzle_grid[:, col])
        already_taken = already_taken.union(self.get_square(get_square_index(row), get_square_index(col)).flatten())
        if numbers_to_avoid is not None:
            already_taken = already_taken.union(numbers_to_avoid)
        options = set([i for i in range(1, 10)]).difference(already_taken)
        return options

    def is_finished(self) -> bool:
        return not np.any(self.puzzle_grid == 0)
