import pygame
import random
from settings import screen, ROWS, COLS, FPS, CELL_WIDTH, CELL_HEIGHT, PLAYER_COLOR, AI_COLOR
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
    font = pygame.font.SysFont("Arial", 24)
    
    player_text = font.render(f"Jugador (Verde): {player_zones}", True, (0, 0, 0))
    ai_text = font.render(f"IA (Rojo): {ai_zones}", True, (0, 0, 0))
    
    screen.blit(player_text, (10, 10))
    screen.blit(ai_text, (10, 40))
    
    turn_text = font.render(
        f"Turno: {'Jugador' if turn == 'player' else 'IA'}", 
        True, 
        (0, 0, 0)
    )
    screen.blit(turn_text, (10, 70))
    
    if game_over:
        result_font = pygame.font.SysFont("Arial", 36)
        if player_zones > ai_zones:
            result_text = result_font.render("¡Gana el Jugador!", True, PLAYER_COLOR)
        elif ai_zones > player_zones:
            result_text = result_font.render("¡Gana la IA!", True, AI_COLOR)
        else:
            result_text = result_font.render("¡Empate!", True, (0, 0, 200))
        
        screen.blit(result_text, (
            screen.get_width() // 2 - result_text.get_width() // 2,
            screen.get_height() - 50
        ))

def game_loop(difficulty):
    blocked_cells = {}
    
    player_pos = get_random_position(blocked_cells)
    ai_pos = get_random_position(blocked_cells)
    while ai_pos == player_pos:
        ai_pos = get_random_position(blocked_cells)
    
    ai = YoshiAI(difficulty)
    
    selected_yoshi = None
    possible_moves = []
    turn = 'player'
    game_over = False
    player_zones = 0
    ai_zones = 0
    
    running = True
    while running:
        if turn == 'ai' and not game_over:
            pygame.time.delay(500)
            
            best_move = ai.get_best_move(blocked_cells, player_pos, ai_pos)
            if best_move:
                if ai_pos in ai.get_all_special_cells() and ai_pos not in blocked_cells:
                    blocked_cells[ai_pos] = AI_COLOR
                ai_pos = best_move
                turn = 'player'
            
            game_over = ai.is_game_over(blocked_cells)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN and turn == 'player' and not game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = mouse_x // CELL_WIDTH
                row = mouse_y // CELL_HEIGHT
                
                if (row, col) == player_pos:
                    selected_yoshi = (row, col)
                    possible_moves = yoshi_moves(row, col, blocked_cells)
                
                elif (row, col) in possible_moves:
                    if player_pos in ai.get_all_special_cells() and player_pos not in blocked_cells:
                        blocked_cells[player_pos] = PLAYER_COLOR
                    
                    player_pos = (row, col)
                    selected_yoshi = None
                    possible_moves = []
                    turn = 'ai'
                    
                    player_zones, ai_zones = calculate_controlled_zones(ai, blocked_cells)
                    game_over = True if player_zones + ai_zones == 4 else False
        
        player_zones, ai_zones = calculate_controlled_zones(ai, blocked_cells)
        draw_board(screen, blocked_cells, possible_moves, player_pos, ai_pos)
        draw_game_info(screen, player_zones, ai_zones, turn, game_over)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":    
    show_start_screen()
    selected_difficulty = show_difficulty_menu()
    game_loop(selected_difficulty)