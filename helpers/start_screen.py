from settings import *

def show_start_screen():
    screen.fill((0, 0, 0))
    font_title = pygame.font.SysFont("Arial", 60)
    font_msg = pygame.font.SysFont("Arial", 30)

    title_surf = font_title.render("Yoshi's Zones", True, (255, 255, 255))
    msg_surf = font_msg.render("Presiona cualquier tecla para comenzar", True, (200, 200, 200))

    screen.blit(title_surf, (screen.get_width() // 2 - title_surf.get_width() // 2, 200))
    screen.blit(msg_surf, (screen.get_width() // 2 - msg_surf.get_width() // 2, 300))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False