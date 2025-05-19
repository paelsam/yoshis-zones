from settings import ROWS, COLS, CELL_WIDTH, CELL_HEIGHT, HINT_COLOR, PLAYER_COLOR, AI_COLOR
import pygame

def get_special_zone_cells():
    special_cells = set()

    special_cells.update([(0,0), (0,1), (0,2), (1,0), (2,0)])

    special_cells.update([(0, COLS-1), (0, COLS-2), (0, COLS-3), (1, COLS-1), (2, COLS-1)])

    special_cells.update([(ROWS-1, 0), (ROWS-1, 1), (ROWS-1, 2), (ROWS-2, 0), (ROWS-3, 0)])

    special_cells.update([(ROWS-1, COLS-1), (ROWS-1, COLS-2), (ROWS-1, COLS-3), 
                         (ROWS-2, COLS-1), (ROWS-3, COLS-1)])
    return special_cells

def draw_board(screen, blocked_cells, possible_moves, player_pos, ai_pos):
    screen.fill((255, 255, 255))
    

    special_cells = get_special_zone_cells()
    for row, col in special_cells:
        rect = pygame.Rect(col * CELL_WIDTH, row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
        pygame.draw.rect(screen, (230, 230, 230), rect) 
        pygame.draw.rect(screen, (200, 0, 0), rect, 2)


    for (r, c), color in blocked_cells.items():
        rect = pygame.Rect(c * CELL_WIDTH, r * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
        pygame.draw.rect(screen, color, rect)

   
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_WIDTH, row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)


    for r, c in possible_moves:
        rect = pygame.Rect(c * CELL_WIDTH, r * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
        pygame.draw.rect(screen, HINT_COLOR, rect, 3)


    player_center = (player_pos[1] * CELL_WIDTH + CELL_WIDTH // 2, 
                    player_pos[0] * CELL_HEIGHT + CELL_HEIGHT // 2)
    pygame.draw.circle(screen, PLAYER_COLOR, player_center, CELL_WIDTH // 3)
    pygame.draw.circle(screen, (0, 100, 0), player_center, CELL_WIDTH // 3, 2)
    

    ai_center = (ai_pos[1] * CELL_WIDTH + CELL_WIDTH // 2, 
                ai_pos[0] * CELL_HEIGHT + CELL_HEIGHT // 2)
    pygame.draw.circle(screen, AI_COLOR, ai_center, CELL_WIDTH // 3)
    pygame.draw.circle(screen, (100, 0, 0), ai_center, CELL_WIDTH // 3, 2)