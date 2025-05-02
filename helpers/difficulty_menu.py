from settings import *

def show_difficulty_menu():
    difficulties = ["Principiante", "Amateur", "Experto"]
    selected = 0
    font = pygame.font.SysFont("Arial", 36)

    while True:
        screen.fill((0, 0, 0))

        for i, diff in enumerate(difficulties):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            text = font.render(diff, True, color)
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 200 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(difficulties)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(difficulties)
                elif event.key == pygame.K_RETURN:
                    return difficulties[selected]