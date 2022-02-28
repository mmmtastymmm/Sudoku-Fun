import time
from typing import Optional, Tuple

import pygame

from classes.puzzle import Puzzle, make_solvable_puzzle


def format_time(secs):
    sec = secs % 60
    minute = secs // 60

    mat = f" {minute}:{sec:02d}"
    return mat


def draw_cube(window, value, row, col, board_width, board_height, selected: bool,
              original_indexes: list[Tuple[int, int]]):
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


def draw_grid(window, puzzle: Puzzle, board_width: int, board_height: int):
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

    for row in range(9):
        for col in range(9):
            is_selected = puzzle.selected == (row, col)
            draw_cube(window, puzzle.puzzle_grid[row, col], row, col, board_width, board_height,
                      is_selected, puzzle.original_indexes)


def get_clicked_row_col(mouse_position: Tuple[int, int], board_width: int, board_height: int, rows, cols) \
        -> Optional[Tuple[int, int]]:
    # These are "swapped", so this is a correct unpacking
    mouse_y, mouse_x = mouse_position
    if mouse_x > board_width or mouse_y > board_height:
        return None
    indexes = int(mouse_x / (board_width / rows)), int(mouse_y / (board_height / cols))
    return indexes


def redraw_window(window, puzzle: Puzzle, game_time, strikes):
    window.fill((255, 255, 255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(game_time), True, (0, 0, 0))
    window.blit(text, (540 - 160, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, True, (255, 0, 0))
    window.blit(text, (20, 560))
    # Draw grid and board
    draw_grid(window, puzzle, 540, 540)


def handle_arrow_keys(event, puzzle):
    if not puzzle.selected:
        return
    if event.key == pygame.K_LEFT:
        puzzle.selected[0] = max(puzzle.selected[0] - 1, 0)
    if event.key == pygame.K_RIGHT:
        puzzle.selected[0] = min(puzzle.selected[0] + 1, 8)
    if event.key == pygame.K_UP:
        puzzle.selected[1] = max(puzzle.selected[1] - 1, 0)
    if event.key == pygame.K_DOWN:
        puzzle.selected[1] = min(puzzle.selected[1] + 1, 8)


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
    key = None
    run = True
    done = False
    start = time.time()
    strikes = 0
    play_time = 0
    while run:
        if not done:
            play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                handle_number_updates(event, puzzle)
                handle_arrow_keys(event, puzzle)

            # if event.key == pygame.K_RETURN:
            #     i, j = board.selected
            #     if board.cubes[i][j].temp != 0:
            #         if board.place(board.cubes[i][j].temp):
            #             print("Success")
            #         else:
            #             print("Wrong")
            #             strikes += 1
            #         key = None
            #
            #         if board.is_finished():
            #             print("Game over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                puzzle.selected = (get_clicked_row_col(pygame.mouse.get_pos(), board_width, board_height, rows, cols))

        # if board.selected and key is not None:
        #     board.sketch(key)
        done = puzzle.is_finished()
        redraw_window(window, puzzle, play_time, strikes)
        pygame.display.update()


def handle_number_updates(event, puzzle):
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


main()
pygame.quit()
