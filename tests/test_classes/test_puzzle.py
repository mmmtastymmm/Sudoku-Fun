import numpy as np
import pytest

from classes.puzzle import Puzzle, make_solvable_puzzle, make_puzzle_answer_key


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


def test_answer_key_generation():
    puzzle = make_puzzle_answer_key()
    assert puzzle.is_puzzle_valid()
    assert puzzle.is_finished()


def test_generate_puzzle():
    puzzle = make_solvable_puzzle()
    assert puzzle.is_puzzle_valid()
    found_ok_amount = 0
    for i in range(9):
        for j in range(9):
            if len(puzzle.get_options_for_index(i, j)) == 1:
                found_ok_amount += 1
    assert found_ok_amount != 0


def test_happy_updates():
    puzzle = Puzzle()
    assert puzzle.safe_update(0, 0, 3)
    assert puzzle.safe_update(0, 1, 4)
    assert puzzle.safe_update(0, 3, 5)
    assert puzzle.safe_update(0, 0, 6)


def test_unhappy_updates():
    puzzle = Puzzle()
    assert puzzle.safe_update(0, 0, 3)
    assert not puzzle.safe_update(0, 1, 3)
    assert not puzzle.safe_update(0, 1, 3)
    assert not puzzle.safe_update(1, 1, 3)


def test_solve_empty():
    puzzle = Puzzle()
    answer = puzzle.generate_answer_key_brute_force()
    assert answer
    assert answer.is_finished()


def test_solve_on_partially_filled():
    puzzle = make_solvable_puzzle()
    answer = puzzle.generate_answer_key_brute_force()
    assert answer
    assert answer.is_finished()


def test_solve_on_impossible_difficulty():
    # this is an "insane" level puzzle
    grid = np.array([
        [0, 0, 2, 0, 3, 0, 0, 0, 1],
        [8, 0, 9, 0, 0, 0, 0, 0, 0],
        [7, 3, 0, 4, 1, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 0, 0, 7, 0],
        [0, 0, 7, 1, 0, 8, 9, 0, 0],
        [0, 8, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 2, 5, 0, 9, 7],
        [0, 0, 0, 0, 0, 0, 3, 0, 0],
        [5, 0, 0, 0, 7, 0, 8, 6, 0],
    ])
    puzzle = Puzzle(grid)
    answer = puzzle.generate_answer_key_brute_force()
    assert answer
    assert answer.is_finished()


def test_original_list_empty_on_emtpy_puzzle():
    empty_puzzle = Puzzle()
    assert len(empty_puzzle.original_indexes) == 0


def test_original_list_has_all_filled_puzzle():
    puzzle = make_solvable_puzzle()
    for i in range(9):
        for j in range(9):
            if puzzle.puzzle_grid[i, j] != 0:
                assert (i, j) in puzzle.original_indexes
            else:
                assert (i, j) not in puzzle.original_indexes
