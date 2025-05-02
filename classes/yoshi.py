from settings import ROWS, COLS

def yoshi_moves(row, col, blocked_cells):
    offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
               (1, -2), (1, 2), (2, -1), (2, 1)]
    moves = []
    for dr, dc in offsets:
        nr, nc = row + dr, col + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            if (nr, nc) not in blocked_cells:
                moves.append((nr, nc))
    return moves
