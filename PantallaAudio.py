import pygame
import sys

def pantalla_audio(screen, bg_anim):
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pantalla 3")

    # BOTON ATRAS
    atras = pygame.image.load("imagenes/atras.png").convert_alpha()
    atras = pygame.transform.scale(atras, (40, 40))
    # Posicion boton atras
    atras_rect = atras.get_rect(topleft=(30, 30))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Al pulsar boton atras se sale de pantalla2
            if event.type == pygame.MOUSEBUTTONDOWN:
                if atras_rect.collidepoint(mouse_pos):
                    from PantallaConfigPartida import pantalla2 #Se importa aqui para evitar importacion circular

                    pantalla2(screen, bg_anim)


        bg_anim.update()
        bg_anim.draw(screen)

        # Efecto hover para el botón "atrás"
        if atras_rect.collidepoint(mouse_pos):
            # Aumentar el tamaño del botón cuando el ratón esté encima
            atras_hover = pygame.transform.scale(atras, (55, 55))
            atras_rect_hover = atras_hover.get_rect(center=atras_rect.center)
            screen.blit(atras_hover, atras_rect_hover)
        else:
            # Dibujar el botón normal si no hay hover
            screen.blit(atras, atras_rect)

        pygame.display.flip()
        clock.tick(60)