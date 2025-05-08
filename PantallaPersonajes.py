import pygame
import sys
def pantalla_personajes(screen, bg_anim):
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pantalla 3")

    # BOTON ATRAS
    atras = pygame.image.load("imagenes/atras.png").convert_alpha()
    atras = pygame.transform.scale(atras, (40, 40))
    atras_rect = atras.get_rect(topleft=(25, 25))

    # BOTON SIGUIENTE
    siguiente = pygame.transform.scale(pygame.image.load("imagenes/siguiente.png"), (40, 40))
    siguiente_rect = siguiente.get_rect(bottomright=(screen.get_width() - 25, screen.get_height() - 25))

    # FONDO
    fondo = pygame.transform.scale(pygame.image.load("imagenes/fondobasico.png"), (750, 450))
    fondo_rect = fondo.get_rect(midright=(screen.get_width(), screen.get_height() // 2))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Volver atrás
                if atras_rect.collidepoint(mouse_pos):
                    from PantallaMapas import pantalla_mapas
                    pantalla_mapas(screen, bg_anim)
                    return
                # Pulsar siguiente
                if siguiente_rect.collidepoint(mouse_pos):
                    # Aquí podrías pasar config a la siguiente pantalla
                    # e.g. pantalla_siguiente(screen, bg_anim, config)
                    return

        # Dibujar fondo y marco
        bg_anim.update()
        bg_anim.draw(screen)

        screen.blit(fondo, fondo_rect)

        # Hover botón ATRÁS
        if atras_rect.collidepoint(mouse_pos):
            atras_hover = pygame.transform.scale(atras, (int(atras_rect.width * 1.1), int(atras_rect.height * 1.1)))
            atras_rect_hover = atras_hover.get_rect(center=atras_rect.center)
            screen.blit(atras_hover, atras_rect_hover)
        else:
            screen.blit(atras, atras_rect)

        # Hover botón SIGUIENTE
        if siguiente_rect.collidepoint(mouse_pos):
            siguiente_hover = pygame.transform.scale(siguiente, (
            int(siguiente_rect.width * 1.1), int(siguiente_rect.height * 1.1)))
            siguiente_rect_hover = siguiente_hover.get_rect(center=siguiente_rect.center)
            screen.blit(siguiente_hover, siguiente_rect_hover)
        else:
            screen.blit(siguiente, siguiente_rect)

        pygame.display.flip()
        clock.tick(60)