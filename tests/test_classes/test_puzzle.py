from classes.puzzle import Puzzle


def test_empty_puzzle_constructor():
    puzzle = Puzzle()
    # Ensure that it's the right shape
    assert puzzle.grid.shape == (9, 9)
    # Ensure it's empty
    assert puzzle.grid.sum() == 0


def test_grid_provided_constructor():
    pass
