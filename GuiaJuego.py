import pygame
import sys

def pantalla_guia_juego(screen, jugador_controlador_id):
    clock = pygame.time.Clock()
    ejecutando = True
    while ejecutando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                ejecutando = False
            if isinstance(jugador_controlador_id, int):
                if event.type == pygame.JOYBUTTONDOWN and event.instance_id == jugador_controlador_id:
                    if event.button == 1:  # Botón B
                        ejecutando = False

        screen.fill((0, 0, 0))  # Pantalla completamente negra
        pygame.display.flip()
        clock.tick(60)