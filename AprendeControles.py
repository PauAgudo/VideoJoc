import pygame
import sys

def pantalla_controles(screen):
    """
    Muestra la pantalla de guía del juego y vuelve al menú de pausa al salir.
    """
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    texto = font.render("Aprende los controles", True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 1:  # Botón B del mando
                    running = False

        # PINTAR FONDO GUARDADO (de la partida pausada)
        screen.fill((0, 0, 0))
        # PINTAR TEXTO
        screen.blit(texto, texto_rect)

        pygame.display.flip()
        clock.tick(60)

    return