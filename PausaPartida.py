import pygame
import sys

def menu_pausa(screen, jugador_controlador_id, jugador_nombre="J1"):
    clock = pygame.time.Clock()
    fuente = pygame.font.Font(None, 40)
    opciones = ["Reanudar partida", "Ajustar volumen", "Aprender controles", "Guía de juego", "Salir de la partida"]
    seleccionada = 0

    ancho_caja = 500
    alto_caja = 400
    caja_rect = pygame.Rect(
        (screen.get_width() - ancho_caja) // 2,
        (screen.get_height() - alto_caja) // 2,
        ancho_caja,
        alto_caja
    )

    axis_cooldown = 0  # Para evitar múltiples eventos rápidos

    while True:
        # Capa translúcida de fondo
        capa_negra = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        capa_negra.fill((80, 80, 80, 20))  # gris más visible pero translúcido
        screen.blit(capa_negra, (0, 0))

        # Marco gris
        pygame.draw.rect(screen, (150, 150, 150), caja_rect, border_radius=10)  # fondo gris medio
        pygame.draw.rect(screen, (100, 100, 100), caja_rect, width=4, border_radius=10)  # borde más oscuro

        # Mostrar las opciones
        for i, opcion in enumerate(opciones):
            color = (255, 255, 0) if i == seleccionada else (30, 30, 30)
            texto = fuente.render(opcion, True, color)
            rect = texto.get_rect(center=(caja_rect.centerx, caja_rect.top + 60 + i * 55))
            screen.blit(texto, rect)

        # Mostrar J1, J2... en la esquina superior derecha
        etiqueta = pygame.font.Font(None, 32).render(jugador_nombre, True, (255, 255, 255))
        screen.blit(etiqueta, (screen.get_width() - 70, 20))

        pygame.display.flip()
        clock.tick(30)

        if axis_cooldown > 0:
            axis_cooldown -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Teclado (si quien abrió es teclado)
            elif jugador_controlador_id == "teclado":
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        seleccionada = (seleccionada - 1) % len(opciones)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        seleccionada = (seleccionada + 1) % len(opciones)
                    elif event.key in [pygame.K_RETURN, pygame.K_a]:
                        return opciones[seleccionada]
                    elif event.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                        return "Reanudar partida"

            # Mando (si quien abrió fue un mando con instance_id)
            elif isinstance(jugador_controlador_id, int):
                if event.type == pygame.JOYBUTTONDOWN and event.instance_id == jugador_controlador_id:
                    if event.button == 0:  # Botón A
                        return opciones[seleccionada]
                    elif event.button == 7:  # Botón START → cerrar
                        return "Reanudar partida"

                elif event.type == pygame.JOYHATMOTION and event.instance_id == jugador_controlador_id:
                    hat_x, hat_y = event.value
                    if hat_y == 1:
                        seleccionada = (seleccionada - 1) % len(opciones)
                    elif hat_y == -1:
                        seleccionada = (seleccionada + 1) % len(opciones)

                elif event.type == pygame.JOYAXISMOTION and event.instance_id == jugador_controlador_id:
                    if axis_cooldown == 0:
                        if event.axis == 1:  # Eje vertical del joystick izquierdo o cruceta
                            if event.value < -0.5:
                                seleccionada = (seleccionada - 1) % len(opciones)
                                axis_cooldown = 5
                            elif event.value > 0.5:
                                seleccionada = (seleccionada + 1) % len(opciones)
                                axis_cooldown = 5
