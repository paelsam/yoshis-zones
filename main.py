import pygame
import random
from settings import screen, ROWS, COLS, FPS, CELL_WIDTH, CELL_HEIGHT, PLAYER_COLOR, AI_COLOR, BOARD_HEIGHT
from board import draw_board, get_special_zone_cells
from classes.yoshi import yoshi_moves
from helpers.start_screen import show_start_screen
from helpers.difficulty_menu import show_difficulty_menu
from ai import YoshiAI

clock = pygame.time.Clock()

def get_random_position(blocked_cells):
    while True:
        pos = (random.randint(0, ROWS-1), random.randint(0, COLS-1))
        if pos not in blocked_cells and pos not in get_special_zone_cells():
            return pos

def calculate_controlled_zones(ai, blocked_cells):
    player_zones = 0
    ai_zones = 0
    
    for zone in ai.special_zones:
        player_count = 0
        ai_count = 0
        
        for cell in zone:
            if cell in blocked_cells:
                if blocked_cells[cell] == PLAYER_COLOR:
                    player_count += 1
                elif blocked_cells[cell] == AI_COLOR:
                    ai_count += 1
        
        if player_count > 2:
            player_zones += 1
        elif ai_count > 2:
            ai_zones += 1
    
    return player_zones, ai_zones

def draw_game_info(screen, player_zones, ai_zones, turn, game_over):
    width = screen.get_width()
    height = screen.get_height()
    info_height = int(height * 0.3)

    font = pygame.font.SysFont("Arial", 24)
    result_font = pygame.font.SysFont("Arial", 32)

    # Dibuja fondo inferior respetando el tamaño del tablero (BOARD_HEIGHT)
    bottom_rect = pygame.Rect(0, BOARD_HEIGHT, width, info_height)
    pygame.draw.rect(screen, (245, 245, 245), bottom_rect)

    # Información a la izquierda
    player_text = font.render(f"Jugador (Verde): {player_zones}", True, (0, 100, 0))
    ai_text = font.render(f"IA (Rojo): {ai_zones}", True, (150, 0, 0))
    # Texto de turno con color correspondiente
    turn_label = font.render("Turno:", True, (0, 0, 0))
    if turn == 'player':
        turn_value = font.render(" Jugador", True, PLAYER_COLOR)
    else:
        turn_value = font.render(" IA", True, AI_COLOR)

    screen.blit(player_text, (20, BOARD_HEIGHT + 20))
    screen.blit(ai_text, (20, BOARD_HEIGHT + 60))
    screen.blit(turn_label, (20, BOARD_HEIGHT + 100))
    screen.blit(turn_value, (20 + turn_label.get_width(), BOARD_HEIGHT + 100))

    # Resultado a la derecha
    if game_over:
        if player_zones > ai_zones:
            result = "¡Gana el Jugador!"
            color = PLAYER_COLOR
        elif ai_zones > player_zones:
            result = "¡Gana la IA!"
            color = AI_COLOR
        else:
            result = "¡Empate!"
            color = (0, 0, 200)

        result_text = result_font.render(result, True, color)
        
        # Dibuja el resultado a la derecha respetando el tamaño del tablero (BOARD_HEIGHT)
        screen.blit(result_text, (
            width - result_text.get_width() - 20, BOARD_HEIGHT + 20
        ))

        msg_font = pygame.font.SysFont("Arial", 20)
        msg = msg_font.render("Presiona R para reiniciar", True, (50, 50, 50))
        
        # Dibuja el mensaje a la derecha respetando el tamaño del tablero (BOARD_HEIGHT)
        screen.blit(msg, (
            width - msg.get_width() - 20, BOARD_HEIGHT + 60
        ))


def game_loop(difficulty):
    blocked_cells = {}
    
    player_pos = get_random_position(blocked_cells)
    ai_pos = get_random_position(blocked_cells)
    while ai_pos == player_pos:
        ai_pos = get_random_position(blocked_cells)
    
    ai = YoshiAI(difficulty)
    
    possible_moves = []
    turn = 'player'
    game_over = False
    player_zones = 0
    ai_zones = 0
    
    running = True
    while running:
        if turn == 'ai' and not game_over:
            pygame.time.delay(450)
    
            best_move = ai.get_best_move(blocked_cells, player_pos, ai_pos)
            if best_move:
                if ai_pos in ai.get_all_special_cells() and ai_pos not in blocked_cells:
                    blocked_cells[ai_pos] = AI_COLOR
                ai_pos = best_move

            player_zones, ai_zones = calculate_controlled_zones(ai, blocked_cells)
            draw_game_info(screen, player_zones, ai_zones, turn, game_over)
            turn = 'player'
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN and turn == 'player' and not game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = mouse_x // CELL_WIDTH
                row = mouse_y // CELL_HEIGHT
                
                if (row, col) == player_pos:
                    possible_moves = yoshi_moves(row, col, blocked_cells, forbidden_positions={ai_pos})
                
                elif (row, col) in possible_moves:
                    if player_pos in ai.get_all_special_cells() and player_pos not in blocked_cells:
                        blocked_cells[player_pos] = PLAYER_COLOR
                    
                    player_pos = (row, col)
                    possible_moves = []
                    turn = 'ai'
                    
                    player_zones, ai_zones = calculate_controlled_zones(ai, blocked_cells)
        
        draw_board(screen, blocked_cells, possible_moves, player_pos, ai_pos)
        player_zones, ai_zones = calculate_controlled_zones(ai, blocked_cells)
        draw_game_info(screen, player_zones, ai_zones, turn, game_over)
        
        game_over = True if player_zones + ai_zones == 4 else False
        
        pygame.display.flip()
        clock.tick(FPS)
        
        if game_over:
            draw_board(screen, blocked_cells, possible_moves, player_pos, ai_pos)
            draw_game_info(screen, player_zones, ai_zones, turn, game_over)
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            return True
        
    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    while True:
        show_start_screen()
        selected_difficulty = show_difficulty_menu()
        
        result = game_loop(selected_difficulty)

        if result is False:
            break  
        elif result == 'menu':
            continue  
        elif result is True:
            pass  
