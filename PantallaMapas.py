import pygame
import sys

# Importar configuración global para guardar selección
from Config import config


def pantalla_mapas(screen, bg_anim):
    global current_time
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pantalla Mapas")

    # INICIALIZAR MANDOS
    pygame.joystick.init()
    mandos = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for mando in mandos:
        mando.init()

    # Cooldown per evitar repeticions contínues
    mando_delay = 200  # mil·lisegons
    last_input_time = pygame.time.get_ticks()

    # BOTON ATRAS
    atras = pygame.transform.scale(pygame.image.load("Media/Menu/Botones/siguiente.png"), (40, 40))
    atras_rotate = pygame.transform.rotate(atras, 180)
    atras_rect = atras_rotate.get_rect(bottomright=(70, screen.get_height() - 25))

    # BOTON SIGUIENTE
    siguiente = pygame.transform.scale(pygame.image.load("Media/Menu/Botones/siguiente.png"), (40, 40))
    siguiente_rect = siguiente.get_rect(bottomright=(screen.get_width() - 25, screen.get_height() - 25))

    # BOTON SETTINGS
    audio = pygame.transform.scale(pygame.image.load("Media/Menu/Botones/settings.png"), (50, 40))
    audio_rect = audio.get_rect(topleft=(25, 25))

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

    # indices para doble click de raton y seleccionar mapa
    last_click_time = 0
    double_click_delay = 300  # milisegundos

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            tiempo_actual = pygame.time.get_ticks()
            if mandos and tiempo_actual - last_input_time > mando_delay:
                joystick = mandos[0]  # Primer mando

                eje_y = joystick.get_axis(1)

                if eje_y < -0.5:  # Joystick amunt
                    selected_index = (selected_index - 1) % len(mapas)
                    config.selected_map = selected_index + 1
                    last_input_time = tiempo_actual

                elif eje_y > 0.5:  # Joystick avall
                    selected_index = (selected_index + 1) % len(mapas)
                    config.selected_map = selected_index + 1
                    last_input_time = tiempo_actual

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from PantallaConfigPartida import pantalla2_main
                    pantalla2_main(screen, bg_anim)
                    return

                elif event.key == pygame.K_RETURN and selected_index >= 0:
                    from PantallaPersonajes import pantalla_personajes
                    pantalla_personajes(screen, bg_anim)
                    return

                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(mapas)
                    config.selected_map = selected_index + 1

                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(mapas)
                    config.selected_map = selected_index + 1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Botón izquierdo del ratón
                current_time = pygame.time.get_ticks()
                mouse_pos = pygame.mouse.get_pos()

                # Botón ATRÁS
                if atras_rect.collidepoint(mouse_pos):
                    from PantallaConfigPartida import pantalla2_main
                    pantalla2_main(screen, bg_anim)
                    return

                # Botón SIGUIENTE
                if siguiente_rect.collidepoint(mouse_pos) and selected_index >= 0:
                    from PantallaPersonajes import pantalla_personajes
                    pantalla_personajes(screen, bg_anim)
                    return

                if audio_rect.collidepoint(mouse_pos):
                    from PantallaAudio import pantalla_audio
                    pantalla_audio(screen, bg_anim, volver_callback=pantalla_mapas)

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:  # A → següent pantalla
                    from PantallaPersonajes import pantalla_personajes
                    pantalla_personajes(screen, bg_anim)
                    return

                elif event.button == 1:  # B → enrere
                    from PantallaConfigPartida import pantalla2_main
                    pantalla2_main(screen, bg_anim)
                    return

                elif event.button == 7:  # OPTIONS → pantalla audio
                    from PantallaAudio import pantalla_audio
                    pantalla_audio(screen, bg_anim, volver_callback=pantalla_mapas)

            elif event.type == pygame.JOYDEVICEADDED:
                nuevo_mando = pygame.joystick.Joystick(event.device_index)
                nuevo_mando.init()
                mandos.append(nuevo_mando)
                print("Mando conectado:", nuevo_mando.get_name())

                # CLIC SOBRE MAPA
                for idx, (mini, big, rect, name_surf) in enumerate(mapas):
                    if rect.collidepoint(mouse_pos):
                        if idx == selected_index and current_time - last_click_time <= double_click_delay:
                            # Doble clic sobre el mapa ya seleccionado → avanzar pantalla
                            from PantallaPersonajes import pantalla_personajes
                            pantalla_personajes(screen, bg_anim)
                            return
                        else:
                            # Selección normal de mapa
                            selected_index = idx
                            config.selected_map = idx + 1
                            last_click_time = current_time
                        break  # Salimos del bucle después de encontrar un mapa

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

        # Botones fijos
        for img, rc in [(atras_rotate, atras_rect), (siguiente, siguiente_rect), (audio, audio_rect)]:
            if rc.collidepoint(mouse_pos):
                screen.blit(pygame.transform.scale(img, (int(rc.width * 1.1), int(rc.height * 1.1))), rc)
            else:
                screen.blit(img, rc)

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
