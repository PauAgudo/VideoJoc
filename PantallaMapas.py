import pygame
import sys

def pantalla_mapas(screen, bg_anim):
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pantalla 3")

    # BOTON ATRAS
    atras = pygame.image.load("imagenes/atras.png").convert_alpha()
    atras = pygame.transform.scale(atras, (40, 40))
    atras_rect = atras.get_rect(topleft=(25, 25))

    # BOTON SIGUIENTE
    siguiente = pygame.transform.scale(pygame.image.load("imagenes/siguiente.png"), (40, 40))
    siguiente_rect = siguiente.get_rect(bottomright=(screen.get_width() - 25, screen.get_height() - 25))

    # MARCO CENTRAL
    marco = pygame.image.load("imagenes/mapselect.png").convert_alpha()
    marco = pygame.transform.scale(marco, (750, 480))
    marco_rect = marco.get_rect(midright=(screen.get_width(), screen.get_height()//2))

    # TEXTO MAPA
    font = pygame.font.Font(None, 21)  # None=fuente por defecto, 48pt
    text_surf = font.render("SELECCIONA UNA FASE", True, (255, 255, 255))  # color blanco
    text_rect = text_surf.get_rect(center=(185, 118))  # centrar en (400,300)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and atras_rect.collidepoint(mouse_pos):
                from PantallaConfigPartida import pantalla2_main
                pantalla2_main(screen, bg_anim)
                return

        # Actualizar y dibujar fondo animado
        bg_anim.update()
        bg_anim.draw(screen)

        # Dibujar marco centrado
        screen.blit(marco, marco_rect)



        # Efecto hover para el botón "atrás"
        if atras_rect.collidepoint(mouse_pos):
            atras_hover = pygame.transform.scale(atras, (int(atras_rect.width*1.1),int(atras_rect.height*1.1)))
            atras_rect_hover = atras_hover.get_rect(center=atras_rect.center)
            screen.blit(atras_hover, atras_rect_hover)
        else:
            screen.blit(atras, atras_rect)

        # Efecto hover para el botón "siguiente"
        if siguiente_rect.collidepoint(mouse_pos):
            siguiente_hover = pygame.transform.scale(siguiente, (int(siguiente_rect.width*1.1),int(siguiente_rect.height*1.1)))
            siguiente_rect_hover = siguiente_hover.get_rect(center=siguiente_rect.center)
            screen.blit(siguiente_hover, siguiente_rect_hover)
        else:
            screen.blit(siguiente, siguiente_rect)

        screen.blit(text_surf, text_rect)
        pygame.display.flip()
        clock.tick(60)
