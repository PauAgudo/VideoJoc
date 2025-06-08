import pygame
import sys

# Importar configuración global para guardar selección
from Config import config

def pantalla_mapas(screen, bg_anim):
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pantalla 3")

    # BOTON ATRAS
    atras = pygame.transform.scale(pygame.image.load("Media/Menu/Botones/siguiente.png"), (40, 40))
    atras_rotated = pygame.transform.flip(atras, True, False)  # flip horizontal
    atras_rect = atras_rotated.get_rect(bottomleft=(25, screen.get_height() - 25))

    # BOTON SIGUIENTE
    siguiente = pygame.transform.scale(pygame.image.load("Media/Menu/Botones/siguiente.png"), (40, 40))
    siguiente_rect = siguiente.get_rect(bottomright=(screen.get_width() - 25, screen.get_height() - 25))

    # MARCO CENTRAL
    marco = pygame.transform.scale(pygame.image.load("Media/Menu/Pantalla_mapas/Mapselect.png"), (750, 450))
    marco_rect = marco.get_rect(midright=(screen.get_width(), screen.get_height() // 2))

    # Nombres de los mapas
    map_names = ["CLASSIC VINTAGE", "SOBEK OASIS", "GREEN VALLEY"]
    font = pygame.font.Font(None, 26)
    name_surfs = [font.render(name, True, (255,255,255)) for name in map_names]

    # MAPAS
    mapas = []  # lista de tuplas (mini, big, rect, name_surf)
    x = 185
    start_y = 220
    gap = 15
    for i in range(3):
        mini = pygame.image.load(f"Media/Menu/Pantalla_mapas/mapa{i+1}.png").convert_alpha()
        mini = pygame.transform.scale(mini, (120, 105))
        big = pygame.image.load(f"Media/Menu/Pantalla_mapas/mapa{i+1}big.png").convert_alpha()
        y = start_y + i * (100 + gap)
        rect = mini.get_rect(center=(x, y))
        mapas.append((mini, big, rect, name_surfs[i]))

    # Parámetros de contorno hover
    hover_color = (0, 255, 255)
    border_thickness = 4

    # Índice del mapa seleccionado (por defecto el primer mapa)
    selected_index = config.selected_map - 1

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
                    from PantallaConfigPartida import pantalla2_main
                    pantalla2_main(screen, bg_anim)
                    return
                # Seleccionar mapa al hacer click
                for idx, (mini, big, rect, name_surf) in enumerate(mapas):
                    if rect.collidepoint(mouse_pos):
                        selected_index = idx
                        # Guardar en config global
                        config.selected_map = idx + 1
                        break
                # Pulsar siguiente
                if siguiente_rect.collidepoint(mouse_pos) and selected_index >= 0:
                    from PantallaPersonajes import pantalla_personajes
                    pantalla_personajes(screen, bg_anim)
                    return
            if event.type == pygame.KEYDOWN:
                # Volver atrás
                if event.key == pygame.K_ESCAPE:
                    from PantallaConfigPartida import pantalla2_main
                    pantalla2_main(screen, bg_anim)
                    return
                # Seleccionar mapa al hacer click
                for idx, (mini, big, rect, name_surf) in enumerate(mapas):
                    if rect.collidepoint(mouse_pos):
                        selected_index = idx
                        # Guardar en config global
                        config.selected_map = idx + 1
                        break
                # Pulsar siguiente
                if event.key == pygame.K_RETURN and selected_index >= 0:
                    from PantallaPersonajes import pantalla_personajes
                    pantalla_personajes(screen, bg_anim)
                    return

        # Dibujar fondo y marco
        bg_anim.update()
        bg_anim.draw(screen)
        screen.blit(marco, marco_rect)

                # Dibujar mapas, hover y selección fija
        for idx, (mini, big, rect, name_surf) in enumerate(mapas):
            screen.blit(mini, rect)
            # Solo mostrar preview en hover cuando no hay selección,
            # o mostrar siempre el mapa seleccionado
            if (selected_index == -1 and rect.collidepoint(mouse_pos)) or idx == selected_index:
                # dibujar contorno celeste
                hover_rect = rect.inflate(border_thickness, border_thickness)
                pygame.draw.rect(screen, hover_color, hover_rect, border_thickness)
                # vista previa grande
                preview = pygame.transform.scale(big, (405, 345))
                preview_rect = preview.get_rect(midright=(screen.get_width() - 30, screen.get_height() // 2))
                screen.blit(preview, preview_rect)
                # mostrar nombre debajo de la preview
                name_rect = name_surf.get_rect(midtop=(preview_rect.centerx + 20, preview_rect.bottom + 22))
                screen.blit(name_surf, name_rect)

        # Hover botón ATRÁS
        if atras_rect.collidepoint(mouse_pos):
            atras_hover = pygame.transform.scale(atras_rotated, (int(atras_rect.width * 1.1), int(atras_rect.height * 1.1)))
            atras_rect_hover = atras_hover.get_rect(center=atras_rect.center)
            screen.blit(atras_hover, atras_rect_hover)
        else:
            screen.blit(atras_rotated, atras_rect)

        # Hover botón SIGUIENTE
        if siguiente_rect.collidepoint(mouse_pos):
            siguiente_hover = pygame.transform.scale(siguiente, (int(siguiente_rect.width * 1.1), int(siguiente_rect.height * 1.1)))
            siguiente_rect_hover = siguiente_hover.get_rect(center=siguiente_rect.center)
            screen.blit(siguiente_hover, siguiente_rect_hover)
        else:
            screen.blit(siguiente, siguiente_rect)

        # Mostrar título
        font = pygame.font.Font(None, 21)
        title_surf = font.render("SELECCIONA UNA FASE", True, (255,255,255))
        title_rect = title_surf.get_rect(center=(185, 130))
        screen.blit(title_surf, title_rect)

        # Mostrar título principal
        font2 = pygame.font.Font(None, 36)
        title_surf = font2.render("CAMPOS DE BATALLA", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(537, 98))
        screen.blit(title_surf, title_rect)

        pygame.display.flip()
        clock.tick(60)
