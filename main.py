import pygame
from settings import screen, FPS, CELL_WIDTH, CELL_HEIGHT, YOSHI_COLOR
from board import draw_board, get_special_zone_cells
from classes.yoshi import yoshi_moves
from helpers.start_screen import show_start_screen
from helpers.difficulty_menu import show_difficulty_menu

clock = pygame.time.Clock()

def game_loop(difficulty):
    selected_yoshi = None
    possible_moves = []
    yoshi_pos = (3, 3)
    blocked_cells = {}

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = mouse_x // CELL_WIDTH
                row = mouse_y // CELL_HEIGHT

                if (row, col) == yoshi_pos:
                    selected_yoshi = (row, col)
                    possible_moves = yoshi_moves(row, col, blocked_cells)
                elif (row, col) in possible_moves:
                    if yoshi_pos in get_special_zone_cells():
                        blocked_cells[yoshi_pos] = YOSHI_COLOR
                    yoshi_pos = (row, col)
                    selected_yoshi = None
                    possible_moves = []
                else:
                    selected_yoshi = None
                    possible_moves = []

        draw_board(screen, blocked_cells, possible_moves, yoshi_pos)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    
    
if __name__ == "__main__":    
    show_start_screen()
    selected_difficulty = show_difficulty_menu()
    game_loop(selected_difficulty)
