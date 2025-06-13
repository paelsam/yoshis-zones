from settings import ROWS, COLS, CELL_WIDTH, CELL_HEIGHT, HINT_COLOR, PLAYER_COLOR, AI_COLOR
import pygame
import os

IMG_FOLDER = os.path.join(os.path.dirname(__file__), "./imgs")
cell_sprites = [
    pygame.image.load(os.path.join(IMG_FOLDER, f"cell_{i}.png")).convert_alpha()
    for i in range(1, 6)
]
objective_1 = pygame.image.load(os.path.join(IMG_FOLDER, "objetive_1.png")).convert_alpha()
objective_2 = pygame.image.load(os.path.join(IMG_FOLDER, "objetive_2.png")).convert_alpha()

green_yoshi = pygame.image.load(os.path.join(IMG_FOLDER, "green_yoshi.png")).convert_alpha()
red_yoshi = pygame.image.load(os.path.join(IMG_FOLDER, "red_yoshi.png")).convert_alpha()

def get_special_zone_cells():
    special_cells = set()
    special_cells.update([(0,0), (0,1), (0,2), (1,0), (2,0)])
    special_cells.update([(0, COLS-1), (0, COLS-2), (0, COLS-3), (1, COLS-1), (2, COLS-1)])
    special_cells.update([(ROWS-1, 0), (ROWS-1, 1), (ROWS-1, 2), (ROWS-2, 0), (ROWS-3, 0)])
    special_cells.update([(ROWS-1, COLS-1), (ROWS-1, COLS-2), (ROWS-1, COLS-3), 
                          (ROWS-2, COLS-1), (ROWS-3, COLS-1)])
    return special_cells

def draw_board(screen, blocked_cells, possible_moves, player_pos, ai_pos, override_y=(None, None)):
    screen.fill((255, 255, 255))
    special_cells = get_special_zone_cells()

    for row in range(ROWS):
        for col in range(COLS):
            cell_pos = (row, col)
            rect = pygame.Rect(col * CELL_WIDTH, row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)

            # Determinar sprite de la celda
            if cell_pos in special_cells:
                base_sprite = objective_1 if (row + col) % 2 == 0 else objective_2
                image = base_sprite.copy()

                # Aplicar filtro si un yoshi está encima
                if cell_pos == player_pos:
                    image.fill((*PLAYER_COLOR, 100), special_flags=pygame.BLEND_RGBA_MULT)
                elif cell_pos == ai_pos:
                    image.fill((*AI_COLOR, 100), special_flags=pygame.BLEND_RGBA_MULT)

                scaled_img = pygame.transform.scale(image, (CELL_WIDTH, CELL_HEIGHT))
                screen.blit(scaled_img, rect)
                pygame.draw.rect(screen, (200, 0, 0), rect, 2)  # borde rojo
            else:
                sprite_index = (row * COLS + col) % len(cell_sprites)
                image = pygame.transform.scale(cell_sprites[sprite_index], (CELL_WIDTH, CELL_HEIGHT))
                screen.blit(image, rect)

    # Dibujar celdas bloqueadas con overlay de color
    for (r, c), color in blocked_cells.items():
        rect = pygame.Rect(c * CELL_WIDTH, r * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
        overlay = pygame.Surface((CELL_WIDTH, CELL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*color, 100))
        screen.blit(overlay, rect)

    # Posibles movimientos
    for r, c in possible_moves:
        rect = pygame.Rect(c * CELL_WIDTH, r * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
        pygame.draw.rect(screen, HINT_COLOR, rect, 3)

    # Yoshi jugador (verde)
    yoshi_green_scaled = pygame.transform.scale(green_yoshi, (CELL_WIDTH, CELL_HEIGHT))
    screen.blit(yoshi_green_scaled, (player_pos[1] * CELL_WIDTH, player_pos[0] * CELL_HEIGHT))

    # Yoshi IA (rojo)
    yoshi_red_scaled = pygame.transform.scale(red_yoshi, (CELL_WIDTH, CELL_HEIGHT))
    screen.blit(yoshi_red_scaled, (ai_pos[1] * CELL_WIDTH, ai_pos[0] * CELL_HEIGHT))
