import pygame

WIDTH, HEIGHT = 800, 750 
ROWS, COLS = 8, 8
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = (HEIGHT - 100) // ROWS
FPS = 60


PLAYER_COLOR = (0, 200, 0)  

AI_COLOR = (200, 0, 0)       

HINT_COLOR = (248, 240, 28)  

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yoshi's Zones")