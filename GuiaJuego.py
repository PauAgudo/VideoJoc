import pygame
import sys

def pantalla_guia(screen, bg_anim):
    """
    Pantalla temporal para comprobar si se carga correctamente.
    """
    pygame.font.init()
    font = pygame.font.Font(None, 60)  # Fuente grande
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((0, 0, 0))  # Fondo negro

        # Texto centrado
        texto = font.render("GUIA DEL JUEGO", True, (255, 255, 255))
        texto_rect = texto.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(texto, texto_rect)

        pygame.display.flip()
        clock.tick(60)
