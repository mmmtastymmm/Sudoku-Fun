import numpy as np
import pytest

from classes.puzzle import Puzzle, make_solvable_puzzle


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


def test_get_options_blank():
    puzzle = Puzzle()
    options = puzzle.get_options_for_index(0, 0)
    assert len(options) == 9


def test_get_options_row_full():
    puzzle = Puzzle()
    for i in range(1, 9):
        puzzle.puzzle_grid[0, i - 1] = i
    options = puzzle.get_options_for_index(0, 8)
    assert len(options) == 1
    assert options.pop() == 9


def test_get_options_col_full():
    puzzle = Puzzle()
    for i in range(1, 9):
        puzzle.puzzle_grid[i - 1, 0] = i
    options = puzzle.get_options_for_index(8, 0)
    assert len(options) == 1
    assert options.pop() == 9


def test_get_possible_actions_already_filled():
    puzzle = Puzzle()
    puzzle.puzzle_grid[0, 0] = 1
    options = puzzle.get_options_for_index(0, 0)
    assert len(options) == 0


def test_get_options_square_full():
    puzzle = Puzzle()
    for i in range(3):
        for j in range(3):
            puzzle.puzzle_grid[i, j] = i + j * 3
    options = puzzle.get_options_for_index(0, 0)
    assert len(options) == 1
    assert options.pop() == 9


def test_puzzle_generation():
    puzzle = make_solvable_puzzle()
    assert puzzle.is_puzzle_valid()
    assert puzzle.is_finished()
    # found_ok_amount = 0
    # for i in range(9):
    #     for j in range(9):
    #         if puzzle.get_options_for_index(i, j) == 1:
    #             found_ok_amount += 1
    # assert found_ok_amount != 0
