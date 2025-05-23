from settings import *

def show_start_screen():
    screen.fill((0, 0, 0))
    font_title = pygame.font.SysFont("Arial", 60)
    font_msg = pygame.font.SysFont("Arial", 30)

    title_surf = font_title.render("Yoshi's Zones", True, (255, 255, 255))
    msg_surf = font_msg.render("Presiona cualquier tecla para comenzar", True, (200, 200, 200))

    # Coordenadas centradas
    title_x = screen.get_width() // 2 - title_surf.get_width() // 2
    title_y = screen.get_height() // 2 - title_surf.get_height()

    msg_x = screen.get_width() // 2 - msg_surf.get_width() // 2
    msg_y = screen.get_height() // 2 + 10  # un poco debajo del título

    screen.blit(title_surf, (title_x, title_y))
    screen.blit(msg_surf, (msg_x, msg_y))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False
