import time
from typing import Optional, Tuple

import pygame

from classes.puzzle import Puzzle, make_solvable_puzzle


def format_time(secs: float) -> str:
    """
    Formats the time for the clock display
    :param secs: How many seconds have passed in the game so far
    :return: The formatted time string
    """
    sec = secs % 60
    minute = secs // 60

    time_passed = f" {minute}:{sec:02d}"
    return time_passed


def draw_cell(window: pygame.Surface, value: int, row: int, col: int, board_width: int, board_height: int,
              selected: bool, original_indexes: list[Tuple[int, int]]):
    """
    Draws one cell
    :param window: Surface to draw on
    :param value: the value the cell holds
    :param row: the row of the cell
    :param col: the col of the cell
    :param board_width: The width of the sudoku board
    :param board_height: The width of the sudoku board
    :param selected: if the cell is currently selected
    :param original_indexes: if the cell is an original index
    :return: Nothing, the cell is drawn
    """
    fnt = pygame.font.SysFont("comicsans", 40)

    gap_width = board_width / 9
    gap_height = board_height / 9
    x = col * gap_width
    y = row * gap_height
    selected_color = (38, 182, 149)
    if (row, col) in original_indexes:
        number_color = (0, 0, 0)
    else:
        number_color = (170, 170, 170)
    if value != 0:
        text = fnt.render(str(value), True, number_color)
        window.blit(text, (x + (gap_width / 2 - text.get_width() / 2), y + (gap_height / 2 - text.get_height() / 2)))

    if selected:
        pygame.draw.rect(window, selected_color, (x, y, gap_width, gap_height), 3)


def draw_sudoku_board(window: pygame.Surface, puzzle: Puzzle, board_width: int, board_height: int):
    rows, cols = puzzle.puzzle_grid.shape
    # Draw Grid Lines
    gap = board_width / rows
    for i in range(rows + 1):
        if i % 3 == 0:
            thick = 4
        else:
            thick = 1
        pygame.draw.line(window, (0, 0, 0), (0, i * gap), (board_width, i * gap), thick)
        pygame.draw.line(window, (0, 0, 0), (i * gap, 0), (i * gap, board_height), thick)
    # Draw all the boxes
    for row in range(9):
        for col in range(9):
            is_selected = puzzle.selected == (row, col)
            draw_cell(window, puzzle.puzzle_grid[row, col], row, col, board_width, board_height,
                      is_selected, puzzle.original_indexes)


def get_clicked_row_col(mouse_position: Tuple[int, int], board_width: int, board_height: int, rows, cols) \
        -> Optional[Tuple[int, int]]:
    """
    Gets the clicked box coordinates
    :param mouse_position: The mouse position from pygame
    :param board_width: How high for the sudoku board
    :param board_height: How wide for the sudoku board
    :param rows: how many rows are in the board
    :param cols: how many cols are in the board
    :return: None if outside the board, or the (row, col)
    """
    # These are "swapped", so this is a correct unpacking
    mouse_y, mouse_x = mouse_position
    if mouse_x > board_width or mouse_y > board_height:
        return None
    indexes = int(mouse_x / (board_width / rows)), int(mouse_y / (board_height / cols))
    return indexes


def redraw_window(window: pygame.Surface, puzzle: Puzzle, game_time: float, is_done: bool):
    """
    Draws the grid on the window surface provided
    :param window: The window to draw on
    :param puzzle: The puzzle to draw
    :param game_time: How long the user has been working on the puzzle
    :return: None, draws the border
    """
    window.fill((255, 255, 255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(game_time), True, (0, 0, 0))
    window.blit(text, (540 - 160, 560))
    if is_done:
        window.blit(fnt.render("Done!:", True, (0, 0, 0)), (20, 560))
    # Draw grid and board
    draw_sudoku_board(window, puzzle, 540, 540)


def handle_arrow_keys(event: pygame.event.Event, puzzle: Puzzle):
    """
    Moves the selected box with the arrow keys
    :param event: The key event
    :param puzzle: the puzzle to update
    :return: None, with the side effect of the puzzle selected state updated
    """
    if not puzzle.selected:
        return
    if event.key == pygame.K_UP:
        puzzle.selected = max(puzzle.selected[0] - 1, 0), puzzle.selected[1]
    if event.key == pygame.K_DOWN:
        puzzle.selected = min(puzzle.selected[0] + 1, 8), puzzle.selected[1]
    if event.key == pygame.K_LEFT:
        puzzle.selected = puzzle.selected[0], max(puzzle.selected[1] - 1, 0)
    if event.key == pygame.K_RIGHT:
        puzzle.selected = puzzle.selected[0], min(puzzle.selected[1] + 1, 8)


def main():
    # Initialize the pygame fonts
    pygame.font.init()
    board_width = 540
    board_height = 540
    rows = 9
    cols = 9
    window = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku Fun")
    puzzle = make_solvable_puzzle()
    run = True
    is_puzzle_solved = False
    start = time.time()
    play_time = 0
    while run:
        if not is_puzzle_solved:
            play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                handle_number_updates(event, puzzle)
                handle_arrow_keys(event, puzzle)

            if event.type == pygame.MOUSEBUTTONDOWN:
                puzzle.selected = (get_clicked_row_col(pygame.mouse.get_pos(), board_width, board_height, rows, cols))

        is_puzzle_solved = puzzle.is_puzzle_solved()
        redraw_window(window, puzzle, play_time, is_puzzle_solved)
        pygame.display.update()


def handle_number_updates(event: pygame.event.Event, puzzle: Puzzle):
    """
    If the user updates a number add that to the puzzle
    :param event: a pygame event
    :param puzzle: the puzzle to update
    :return: None, the puzzle could be modified
    """
    if puzzle.selected is None:
        return
    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
        puzzle.safe_update(puzzle.selected[0], puzzle.selected[1], 1)
    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
        puzzle.safe_update(puzzle.selected[0], puzzle.selected[1], 2)
    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
        puzzle.safe_update(puzzle.selected[0], puzzle.selected[1], 3)
    if event.key == pygame.K_4 or event.key == pygame.K_KP4:
        puzzle.safe_update(puzzle.selected[0], puzzle.selected[1], 4)
    if event.key == pygame.K_5 or event.key == pygame.K_KP5:
        puzzle.safe_update(puzzle.selected[0], puzzle.selected[1], 5)
    if event.key == pygame.K_6 or event.key == pygame.K_KP6:
        puzzle.safe_update(puzzle.selected[0], puzzle.selected[1], 6)
    if event.key == pygame.K_7 or event.key == pygame.K_KP7:
        puzzle.safe_update(puzzle.selected[0], puzzle.selected[1], 7)
    if event.key == pygame.K_8 or event.key == pygame.K_KP8:
        puzzle.safe_update(puzzle.selected[0], puzzle.selected[1], 8)
    if event.key == pygame.K_9 or event.key == pygame.K_KP9:
        puzzle.safe_update(puzzle.selected[0], puzzle.selected[1], 9)
    if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
        puzzle.safe_update(puzzle.selected[0], puzzle.selected[1], 0)


if __name__ == "__main__":
    main()
    pygame.quit()
