import pygame
import sys


def menu_pausa(screen, jugador_controlador="teclado"):
    fuente = pygame.font.Font(None, 40)
    opciones = ["Reanudar", "Reiniciar ronda", "Salir al menú"]
    seleccionada = 0

    # Boton settings
    settings = pygame.image.load("Media/Menu/Botones/settings.png").convert_alpha()
    settings = pygame.transform.scale(settings, (40, 40))
    settings_hover = pygame.transform.scale(settings, (48, 48))

    clock = pygame.time.Clock()
    ancho_caja = 400
    alto_caja = 300
    caja_rect = pygame.Rect(
        (screen.get_width() - ancho_caja) // 2,
        (screen.get_height() - alto_caja) // 2,
        ancho_caja,
        alto_caja
    )

    while True:

        # Superponer fondo semitransparente sobre la pantalla de juego
        overlay = pygame.Surface((ancho_caja, alto_caja), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # negro semitransparente
        screen.blit(overlay, caja_rect.topleft)

        # DIBUJAR MARCO BLANCO
        pygame.draw.rect(screen, (255, 255, 255), caja_rect, border_radius=10)

        # DIBUJAR BORDE GRIS
        pygame.draw.rect(screen, (100, 100, 100), caja_rect, width=4, border_radius=10)

        # Obtener posición del ratón
        mouse_pos = pygame.mouse.get_pos()
        icon_rect = settings.get_rect()
        icon_rect.bottomleft = (caja_rect.left + 15, caja_rect.bottom - 15)

        # Detectar si el ratón está sobre alguna opción
        for i, opcion in enumerate(opciones):
            texto_rect = pygame.Rect(
                caja_rect.centerx - 150, caja_rect.top + 60 + i * 60,
                300, 50
            )
            if texto_rect.collidepoint(mouse_pos):
                seleccionada = i

        # Dibujar las opciones
        for i, opcion in enumerate(opciones):
            color = (255, 255, 0) if i == seleccionada else (0, 0, 0)
            texto = fuente.render(opcion, True, color)
            rect = texto.get_rect(center=(caja_rect.centerx, caja_rect.top + 80 + i * 60))
            screen.blit(texto, rect)

        # Hover efecto
        if icon_rect.collidepoint(mouse_pos):
            icon_hover_rect = settings_hover.get_rect(center=icon_rect.center)
            screen.blit(settings_hover, icon_hover_rect)
        else:
            screen.blit(settings, icon_rect)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and jugador_controlador == "teclado":
                if event.key in [pygame.K_UP, pygame.K_w]:
                    seleccionada = (seleccionada - 1) % len(opciones)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    seleccionada = (seleccionada + 1) % len(opciones)
                elif event.key == pygame.K_RETURN:
                    if seleccionada == 0:
                        return "reanudar"
                    elif seleccionada == 1:
                        return "reiniciar"
                    elif seleccionada == 2:
                        return "salir"

            elif event.type == pygame.MOUSEBUTTONDOWN and jugador_controlador == "teclado":
                if event.button == 1:
                    # Clic sobre una opción
                    for i, opcion in enumerate(opciones):
                        texto_rect = pygame.Rect(
                            caja_rect.centerx - 150, caja_rect.top + 60 + i * 60,
                            300, 50
                        )
                        if texto_rect.collidepoint(event.pos):
                            if i == 0:
                                return "reanudar"
                            elif i == 1:
                                return "reiniciar"
                            elif i == 2:
                                return "salir"

                    # Clic en ajustes
                    if icon_rect.collidepoint(event.pos):
                        print("Abrir ajustes")  # O llamar a pantalla de ajustes

