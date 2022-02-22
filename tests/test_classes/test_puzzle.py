import numpy as np
import pytest

from classes.puzzle import Puzzle


def test_empty_puzzle_constructor():
    puzzle = Puzzle()
    # Ensure that it's the right shape
    assert puzzle.puzzle_grid.shape == (9, 9)
    # Ensure it's empty
    assert puzzle.is_puzzle_empty()
    assert puzzle.is_puzzle_valid()


def test_grid_provided_constructor_happy():
    input_grid = np.zeros((9, 9), dtype=np.int8)
    input_grid[0, 2] = 5
    good_puzzle = Puzzle(input_grid)
    assert np.all(np.equal(good_puzzle.puzzle_grid, input_grid))
    assert not good_puzzle.is_puzzle_empty()
    assert good_puzzle.is_puzzle_valid()


def test_grid_provided_wrong_size():
    input_grid = np.zeros((16, 16), dtype=np.int8)
    with pytest.raises(ValueError):
        Puzzle(input_grid)


def test_grid_provided_invalid_input_data():
    # Wrong number
    input_grid = np.zeros((9, 9), dtype=np.int8)
    input_grid[0, 2] = 50
    with pytest.raises(ValueError):
        Puzzle(input_grid)


def test_grid_provided_invalid_square():
    # Illegal square
    input_grid = np.zeros((9, 9), dtype=np.int8)
    input_grid[0, 2] = 5
    input_grid[1, 1] = 5
    with pytest.raises(ValueError):
        Puzzle(input_grid)


def test_grid_provided_invalid_row():
    input_grid = np.zeros((9, 9), dtype=np.int8)
    input_grid[1, 2] = 5
    input_grid[1, 8] = 5
    with pytest.raises(ValueError):
        Puzzle(input_grid)


def test_grid_provided_invalid_col():
    input_grid = np.zeros((9, 9), dtype=np.int8)
    input_grid[0, 1] = 5
    input_grid[8, 1] = 5
    with pytest.raises(ValueError):
        Puzzle(input_grid)


def test_puzzle_generation():
    puzzle = Puzzle.make_solvable_puzzle()
