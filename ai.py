import random
from settings import ROWS, COLS, PLAYER_COLOR, AI_COLOR
from classes.yoshi import yoshi_moves

class YoshiAI:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.depth = self.get_depth_from_difficulty()
        self.special_zones = self.identify_special_zones()
        
    def get_depth_from_difficulty(self):
        return {
            "Principiante": 2,
            "Amateur": 4,
            "Experto": 6
        }.get(self.difficulty, 2)
    
    def identify_special_zones(self):
        zones = []
        zones.append({(0,0), (0,1), (0,2), (1,0), (2,0)})
        zones.append({(0, COLS-1), (0, COLS-2), (0, COLS-3), (1, COLS-1), (2, COLS-1)})
        zones.append({(ROWS-1, 0), (ROWS-1, 1), (ROWS-1, 2), (ROWS-2, 0), (ROWS-3, 0)})
        zones.append({(ROWS-1, COLS-1), (ROWS-1, COLS-2), (ROWS-1, COLS-3), 
                     (ROWS-2, COLS-1), (ROWS-3, COLS-1)})
        return zones

    
    def evaluate_board(self, blocked_cells, player_pos, ai_pos):
        score = 0
        ai_controlled = 0
        player_controlled = 0
        zone_potential = 0

        
        for zone in self.special_zones:
            ai_count = 0
            player_count = 0
            empty_cells = 0
            
            for cell in zone:
                if cell in blocked_cells:
                    if blocked_cells[cell] == AI_COLOR:
                        ai_count += 1
                    else:
                        player_count += 1
                else:
                    empty_cells += 1

            
            if ai_count >= 3:
                ai_controlled += 1
            elif player_count >= 3:
                player_controlled += 1
            else:
                
                zone_diff = ai_count - player_count
                if zone_diff > 0: 
                    zone_potential += (zone_diff * 20) + (empty_cells * 5)
                elif zone_diff < 0:
                    zone_potential -= (abs(zone_diff) * 25)
                
                
                if ai_count == 2 and empty_cells >= 1:
                    zone_potential += 40 


        score += (ai_controlled * 150) - (player_controlled * 200)
        score += zone_potential 


        ai_moves = yoshi_moves(ai_pos[0], ai_pos[1], blocked_cells)
        special_zone_moves = [move for move in ai_moves if move in self.get_all_special_cells()]
        

        score += len(special_zone_moves) * 10


        for zone in self.special_zones:
            if ai_pos in zone and ai_pos not in blocked_cells:
                score += 15 

        return score
        
    def minimax(self, depth, is_maximizing, blocked_cells, player_pos, ai_pos, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or self.is_game_over(blocked_cells):
            eval_score = self.evaluate_board(blocked_cells, player_pos, ai_pos)
            return eval_score, None
        
        best_move = None
        
        if is_maximizing:
            max_eval = float('-inf')
            best_moves = []
            possible_moves = yoshi_moves(ai_pos[0], ai_pos[1], blocked_cells, forbidden_positions={player_pos})

            for move in possible_moves:
                new_blocked = blocked_cells.copy()
                if ai_pos in self.get_all_special_cells():
                    new_blocked[ai_pos] = AI_COLOR

                evaluation, _ = self.minimax(
                    depth - 1, False, new_blocked, player_pos, move, alpha, beta
                )

                if evaluation > max_eval:
                    max_eval = evaluation
                    best_moves = [move]  # Reinicia la lista con este mejor movimiento
                elif evaluation == max_eval:
                    best_moves.append(move)

                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break

            selected_move = random.choice(best_moves) if best_moves else None
            return max_eval, selected_move
        
        else: 
            min_eval = float('inf')
            possible_moves = yoshi_moves(player_pos[0], player_pos[1], blocked_cells, forbidden_positions={ai_pos})
            
            for move in possible_moves:
                new_blocked = blocked_cells.copy()
                if player_pos in self.get_all_special_cells():
                    new_blocked[player_pos] = PLAYER_COLOR
                
                evaluation, _ = self.minimax(
                    depth - 1, True, new_blocked, move, ai_pos, alpha, beta
                )
                
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval, best_move
    
    def get_all_special_cells(self):
        all_special = set()
        for zone in self.special_zones:
            all_special.update(zone)
        return all_special
    
    def is_game_over(self, blocked_cells):
        all_special = self.get_all_special_cells()
        return all(special in blocked_cells for special in all_special)
    
    def get_best_move(self, blocked_cells, player_pos, ai_pos):
        _, best_move = self.minimax(
            self.depth, True, blocked_cells, player_pos, ai_pos
        )
        return best_move