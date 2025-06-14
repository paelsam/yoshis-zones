import pygame

WIDTH, HEIGHT = 900, 900

BOARD_HEIGHT = int(HEIGHT * 0.80) 

ROWS, COLS = 8, 8
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = (BOARD_HEIGHT) // ROWS
FPS = 60


PLAYER_COLOR = (0, 200, 0)  

AI_COLOR = (200, 0, 0)       

HINT_COLOR = (248, 240, 28)  

pygame.init()
pygame.display.set_icon(pygame.image.load("./imgs/icon.png"))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yoshi's Zones")