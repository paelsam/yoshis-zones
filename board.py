from settings import ROWS, COLS, CELL_WIDTH, CELL_HEIGHT, HINT_COLOR
import pygame

def get_special_zone_cells():
    special_cells = set()
    corners = [(0, 0), (0, COLS - 1), (ROWS - 1, 0), (ROWS - 1, COLS - 1)]
    for row, col in corners:
        for i in range(-2, 3):
            if 0 <= col + i < COLS:
                special_cells.add((row, col + i))
            if 0 <= row + i < ROWS:
                special_cells.add((row + i, col))
    return special_cells

def draw_board(screen, blocked_cells, possible_moves, yoshi_pos):
    screen.fill((255, 255, 255))
    
    corners = [(0, 0), (0, COLS - 1), (ROWS - 1, 0), (ROWS - 1, COLS - 1)]
    for row, col in corners:
        for i in range(-2, 3):
            if 0 <= col + i < COLS:
                rect = pygame.Rect((col + i) * CELL_WIDTH, row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                pygame.draw.rect(screen, (255, 0, 0), rect, 2)
            if 0 <= row + i < ROWS:
                rect = pygame.Rect(col * CELL_WIDTH, (row + i) * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                pygame.draw.rect(screen, (255, 0, 0), rect, 2)

    for (r, c), color in blocked_cells.items():
        rect = pygame.Rect(c * CELL_WIDTH, r * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
        pygame.draw.rect(screen, color, rect)

    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_WIDTH, row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

    for r, c in possible_moves:
        rect = pygame.Rect(c * CELL_WIDTH, r * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
        pygame.draw.rect(screen, HINT_COLOR, rect, 2)

    # Yoshi
    y_row, y_col = yoshi_pos
    yoshi_center = (y_col * CELL_WIDTH + CELL_WIDTH // 2, y_row * CELL_HEIGHT + CELL_HEIGHT // 2)
    pygame.draw.circle(screen, (0, 200, 0), yoshi_center, CELL_WIDTH // 3)
