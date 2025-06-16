import pygame
import sys
from PantallaPrincipal import background_screen
from PantallaMapas import pantalla_mapas
from PantallaAudio import pantalla_audio
from Config import config

class ConfiguracionPartida:
    def run(self, screen, bg_anim):
        clock = pygame.time.Clock()
        pygame.display.set_caption("Configuración de Partida")

        # Valores iniciales desde config
        current_set_index = config.current_set_index
        current_minute = config.current_minute
        current_level_index = config.current_level_index
        current_position_index = config.current_position_index
        current_ultimas_index = current_ultimas_index = config.current_ultimas_index.copy()

        # Fondo
        fondo = pygame.transform.scale(pygame.image.load("Media/Menu/fondobasico.png"), (750, 450))
        fondo_rect = fondo.get_rect(midright=(screen.get_width(), screen.get_height() // 2))

        # Botones fijos
        atras = pygame.transform.scale(pygame.image.load("Media/Menu/Botones/siguiente.png"), (40, 40))
        atras_rotate = pygame.transform.rotate(atras, 180)
        atras_rect = atras_rotate.get_rect(bottomright=(70, screen.get_height() - 25))
        siguiente = pygame.transform.scale(pygame.image.load("Media/Menu/Botones/siguiente.png"), (40, 40))
        siguiente_rect = siguiente.get_rect(bottomright=(screen.get_width() - 25, screen.get_height() - 25))
        audio = pygame.transform.scale(pygame.image.load("Media/Menu/Botones/settings.png"), (50, 40))
        audio_rect = audio.get_rect(topleft=(25, 25))

        # Tiras
        tira_activa_idx = 0  # Índice de la tira activa

        # Definición de las claves y sus respectivas imágenes
        keys = ["sets", "minutos", "nivel_COM", "pos_inicial", "Fantasmas", "Maldiciones", "Bloques_final"]

        tira_files = {
            "sets": "Media/Menu/Pantalla_configuracion_partida/tira_sets.png",
            "minutos": "Media/Menu/Pantalla_configuracion_partida/tiempo.png",
            "nivel_COM": "Media/Menu/Pantalla_configuracion_partida/tira_COM.png",
            "pos_inicial": "Media/Menu/Pantalla_configuracion_partida/tira_posicion.png",
            "Fantasmas": "Media/Menu/Pantalla_configuracion_partida/tira_fantasmas.png",
            "Maldiciones": "Media/Menu/Pantalla_configuracion_partida/tira_maldiciones.png",
            "Bloques_final": "Media/Menu/Pantalla_configuracion_partida/tira_bloques.png"
        }

        # Carga cada imagen individual y la guarda en el diccionario tiras
        tiras = {
            k: pygame.transform.scale(pygame.image.load(tira_files[k]), (550, 30))
            for k in keys
        }

        # Desplazamiento vertical
        vertical_shift = 50
        posiciones = {
            "sets": (280, 120 + vertical_shift),
            "minutos": (280, 160 + vertical_shift),
            "nivel_COM": (280, 200 + vertical_shift),
            "pos_inicial": (280, 240 + vertical_shift),
            "Fantasmas": (280, 280 + vertical_shift),
            "Maldiciones": (280, 320 + vertical_shift),
            "Bloques_final": (280, 360 + vertical_shift)
        }
        botones = {k: {"imagen": tiras[k], "rect": tiras[k].get_rect(topleft=posiciones[k])} for k in keys}

        # Flechas
        izquierda = pygame.transform.scale(pygame.image.load("Media/Menu/Pantalla_configuracion_partida/izquierda.png"), (30, 30))
        derecha = pygame.transform.scale(pygame.image.load("Media/Menu/Pantalla_configuracion_partida/derecha.png"), (30, 30))
        flechas_pos = {k: {"izquierda": (520, posiciones[k][1]), "derecha": (680, posiciones[k][1])} for k in keys}

        font = pygame.font.SysFont(None, 23)
        shift_amount = 10

        def ir_a_pantalla_mapas():
            config.current_set_index = current_set_index
            config.current_minute = current_minute
            config.current_level_index = current_level_index
            config.current_position_index = current_position_index
            config.current_ultimas_index = current_ultimas_index.copy()
            pantalla_mapas(screen, bg_anim)

        # Inicializar sistema de mandos
        pygame.joystick.init()
        mandos = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for mando in mandos:
            mando.init()

        # Cooldowns para entradas del mando
        mando_delay = 200  # ms
        last_input_time = pygame.time.get_ticks()

        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Entrada por joystick o cruceta
                tiempo_actual = pygame.time.get_ticks()
                if mandos and tiempo_actual - last_input_time > mando_delay:
                    joystick = mandos[0]  # Solo usamos el primer mando conectado

                    eje_y = joystick.get_axis(1)
                    eje_x = joystick.get_axis(0)

                    if eje_y < -0.5:  # Joystick arriba
                        tira_activa_idx = (tira_activa_idx - 1) % len(keys)
                        last_input_time = tiempo_actual
                    elif eje_y > 0.5:  # Joystick abajo
                        tira_activa_idx = (tira_activa_idx + 1) % len(keys)
                        last_input_time = tiempo_actual

                    elif eje_x < -0.5:  # Joystick izquierda
                        key = keys[tira_activa_idx]
                        if key == "sets" and current_set_index > 0:
                            current_set_index -= 1
                        elif key == "minutos" and current_minute > 1:
                            current_minute -= 1
                        elif key == "nivel_COM" and current_level_index > 0:
                            current_level_index -= 1
                        elif key == "pos_inicial" and current_position_index > 0:
                            current_position_index -= 1
                        elif key in current_ultimas_index and current_ultimas_index[key] > 0:
                            current_ultimas_index[key] -= 1
                        last_input_time = tiempo_actual

                    elif eje_x > 0.5:  # Joystick derecha
                        key = keys[tira_activa_idx]
                        if key == "sets" and current_set_index < len(config.set_options) - 1:
                            current_set_index += 1
                        elif key == "minutos" and current_minute < 9:
                            current_minute += 1
                        elif key == "nivel_COM" and current_level_index < len(config.level_options) - 1:
                            current_level_index += 1
                        elif key == "pos_inicial" and current_position_index < len(config.position_options) - 1:
                            current_position_index += 1
                        elif key in current_ultimas_index and current_ultimas_index[key] < len(
                                config.ultimas_opciones) - 1:
                            current_ultimas_index[key] += 1
                        last_input_time = tiempo_actual

                    elif event.type == pygame.JOYHATMOTION:
                        tiempo_actual = pygame.time.get_ticks()
                        if mandos and tiempo_actual - last_input_time > mando_delay:
                            x, y = event.value  # D-Pad (x: izq/dcha, y: arriba/abajo)

                            if y == 1:  # Flecha arriba
                                tira_activa_idx = (tira_activa_idx - 1) % len(keys)
                                last_input_time = tiempo_actual

                            elif y == -1:  # Flecha abajo
                                tira_activa_idx = (tira_activa_idx + 1) % len(keys)
                                last_input_time = tiempo_actual

                            elif x == -1:  # Flecha izquierda
                                key = keys[tira_activa_idx]
                                if key == "sets" and current_set_index > 0:
                                    current_set_index -= 1
                                elif key == "minutos" and current_minute > 1:
                                    current_minute -= 1
                                elif key == "nivel_COM" and current_level_index > 0:
                                    current_level_index -= 1
                                elif key == "pos_inicial" and current_position_index > 0:
                                    current_position_index -= 1
                                elif key in current_ultimas_index and current_ultimas_index[key] > 0:
                                    current_ultimas_index[key] -= 1
                                last_input_time = tiempo_actual

                            elif x == 1:  # Flecha derecha
                                key = keys[tira_activa_idx]
                                if key == "sets" and current_set_index < len(config.set_options) - 1:
                                    current_set_index += 1
                                elif key == "minutos" and current_minute < 9:
                                    current_minute += 1
                                elif key == "nivel_COM" and current_level_index < len(config.level_options) - 1:
                                    current_level_index += 1
                                elif key == "pos_inicial" and current_position_index < len(config.position_options) - 1:
                                    current_position_index += 1
                                elif key in current_ultimas_index and current_ultimas_index[key] < len(
                                        config.ultimas_opciones) - 1:
                                    current_ultimas_index[key] += 1
                                last_input_time = tiempo_actual


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        config.__init__()
                        background_screen(screen)
                    if event.key == pygame.K_RETURN:
                        ir_a_pantalla_mapas()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if atras_rect.collidepoint(mouse_pos):
                        config.__init__()
                        background_screen(screen)

                    if siguiente_rect.collidepoint(mouse_pos):
                        ir_a_pantalla_mapas()


                    if audio_rect.collidepoint(mouse_pos):
                        pantalla_audio(screen, bg_anim, volver_callback=pantalla2_main)

                    for key, btn in botones.items():
                        if btn["rect"].collidepoint(mouse_pos):
                            la = izquierda.get_rect(topleft=flechas_pos[key]["izquierda"])
                            ra = derecha.get_rect(topleft=flechas_pos[key]["derecha"])
                            if la.collidepoint(mouse_pos):
                                if key == "sets" and current_set_index > 0:
                                    current_set_index -= 1
                                elif key == "minutos" and current_minute > 1:
                                    current_minute -= 1
                                elif key == "nivel_COM" and current_level_index > 0:
                                    current_level_index -= 1
                                elif key == "pos_inicial" and current_position_index > 0:
                                    current_position_index -= 1
                                elif key in current_ultimas_index and current_ultimas_index[key] > 0:
                                    current_ultimas_index[key] -= 1
                            elif ra.collidepoint(mouse_pos):
                                if key == "sets" and current_set_index < len(config.set_options) - 1:
                                    current_set_index += 1
                                elif key == "minutos" and current_minute < 9:
                                    current_minute += 1
                                elif key == "nivel_COM" and current_level_index < len(config.level_options) - 1:
                                    current_level_index += 1
                                elif key == "pos_inicial" and current_position_index < len(config.position_options) - 1:
                                    current_position_index += 1
                                elif key in current_ultimas_index and current_ultimas_index[key] < len(config.ultimas_opciones) - 1:
                                    current_ultimas_index[key] += 1

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        tira_activa_idx = (tira_activa_idx - 1) % len(keys)
                    elif event.key == pygame.K_DOWN:
                        tira_activa_idx = (tira_activa_idx + 1) % len(keys)

                    elif event.key == pygame.K_LEFT:
                        key = keys[tira_activa_idx]
                        if key == "sets" and current_set_index > 0:
                            current_set_index -= 1
                        elif key == "minutos" and current_minute > 1:
                            current_minute -= 1
                        elif key == "nivel_COM" and current_level_index > 0:
                            current_level_index -= 1
                        elif key == "pos_inicial" and current_position_index > 0:
                            current_position_index -= 1
                        elif key in current_ultimas_index and current_ultimas_index[key] > 0:
                            current_ultimas_index[key] -= 1

                    elif event.key == pygame.K_RIGHT:
                        key = keys[tira_activa_idx]
                        if key == "sets" and current_set_index < len(config.set_options) - 1:
                            current_set_index += 1
                        elif key == "minutos" and current_minute < 9:
                            current_minute += 1
                        elif key == "nivel_COM" and current_level_index < len(config.level_options) - 1:
                            current_level_index += 1
                        elif key == "pos_inicial" and current_position_index < len(config.position_options) - 1:
                            current_position_index += 1
                        elif key in current_ultimas_index and current_ultimas_index[key] < len(
                                config.ultimas_opciones) - 1:
                            current_ultimas_index[key] += 1

                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:  # Botón A → siguiente pantalla
                        ir_a_pantalla_mapas()

                    elif event.button == 1:  # Botón B → volver atrás
                        config.__init__()
                        background_screen(screen)

                    elif event.button == 7:  # Botón OPTIONS/Start → ajustes
                        pantalla_audio(screen, bg_anim, volver_callback=pantalla2_main)

                elif event.type == pygame.JOYDEVICEADDED:
                    nuevo_mando = pygame.joystick.Joystick(event.device_index)
                    nuevo_mando.init()
                    mandos.append(nuevo_mando)
                    print("Mando conectado:", nuevo_mando.get_name())

            # Dibujar
            bg_anim.update()
            bg_anim.draw(screen)
            screen.blit(fondo, fondo_rect)

            # Detectar si el ratón está sobre alguna tira: actualizar tira_activa_idx
            for idx, key in enumerate(keys):
                rect = botones[key]["rect"]
                if rect.collidepoint(mouse_pos):
                    tira_activa_idx = idx
                    break

            for key, btn in botones.items():
                rect = btn["rect"]
                es_activa = (keys.index(key) == tira_activa_idx)
                hov = rect.collidepoint(mouse_pos) or es_activa

                img = btn["imagen"]
                if hov:
                    hi = pygame.transform.scale(img, (int(rect.width * 1.1), rect.height))
                    hr = hi.get_rect(center=rect.center)
                    hr.x -= shift_amount
                    screen.blit(hi, hr)
                    cur_rect = hr
                else:
                    screen.blit(img, rect)
                    cur_rect = rect

                # Mostrar valor actual
                if key == "sets":
                    v = config.set_options[current_set_index]
                    screen.blit(pygame.transform.scale(pygame.image.load(f"Media/Menu/Pantalla_configuracion_partida/{v}.png"), (30, 30)),
                                (600 - (shift_amount if hov else 0), posiciones[key][1]))
                if key == "minutos":
                    screen.blit(pygame.transform.scale(pygame.image.load(f"Media/Menu/Pantalla_configuracion_partida/{current_minute}.png"), (30, 30)),
                                (600 - (shift_amount if hov else 0), posiciones[key][1]))
                if key == "nivel_COM":
                    txt = config.level_options[current_level_index]
                    surf = font.render(txt, True, (255, 255, 255))
                    lx = flechas_pos[key]["izquierda"][0] - (shift_amount if hov else 0)
                    rx = flechas_pos[key]["derecha"][0] - (shift_amount if hov else 0)
                    cx = (lx + 30 + rx) // 2
                    cy = cur_rect.centery
                    screen.blit(surf, (cx - surf.get_width() // 2, cy - surf.get_height() // 2))
                if key == "pos_inicial":
                    txt = config.position_options[current_position_index]
                    surf = font.render(txt, True, (255, 255, 255))
                    lx = flechas_pos[key]["izquierda"][0] - (shift_amount if hov else 0)
                    rx = flechas_pos[key]["derecha"][0] - (shift_amount if hov else 0)
                    cx = (lx + 30 + rx) // 2
                    cy = cur_rect.centery
                    screen.blit(surf, (cx - surf.get_width() // 2, cy - surf.get_height() // 2))
                if key in ["Fantasmas", "Maldiciones", "Bloques_final"]:
                    txt = config.ultimas_opciones[current_ultimas_index[key]]
                    surf = font.render(txt, True, (255, 255, 255))
                    lx = flechas_pos[key]["izquierda"][0] - (shift_amount if hov else 0)
                    rx = flechas_pos[key]["derecha"][0] - (shift_amount if hov else 0)
                    cx = (lx + 30 + rx) // 2
                    cy = cur_rect.centery
                    screen.blit(surf, (cx - surf.get_width() // 2, cy - surf.get_height() // 2))

                if hov:
                    left_pos = (flechas_pos[key]["izquierda"][0] - shift_amount, flechas_pos[key]["izquierda"][1])
                    right_pos = (flechas_pos[key]["derecha"][0] - shift_amount, flechas_pos[key]["derecha"][1])
                    left_rect = izquierda.get_rect(topleft=left_pos)
                    right_rect = derecha.get_rect(topleft=right_pos)
                    if left_rect.collidepoint(mouse_pos):
                        iz_hover = pygame.transform.scale(izquierda, (int(left_rect.width * 1.1), int(left_rect.height * 1.1)))
                        iz_rect_h = iz_hover.get_rect(center=left_rect.center)
                        screen.blit(iz_hover, iz_rect_h)
                    else:
                        screen.blit(izquierda, left_rect)
                    if right_rect.collidepoint(mouse_pos):
                        dr_hover = pygame.transform.scale(derecha, (int(right_rect.width * 1.1), int(right_rect.height * 1.1)))
                        dr_rect_h = dr_hover.get_rect(center=right_rect.center)
                        screen.blit(dr_hover, dr_rect_h)
                    else:
                        screen.blit(derecha, right_rect)

            # Botones fijos
            for img, rc in [(atras_rotate, atras_rect), (siguiente, siguiente_rect), (audio, audio_rect)]:
                if rc.collidepoint(mouse_pos):
                    screen.blit(pygame.transform.scale(img, (int(rc.width * 1.1), int(rc.height * 1.1))), rc)
                else:
                    screen.blit(img, rc)

            # Título
            font2 = pygame.font.Font(None, 36)
            title_surf = font2.render("CONFIGURACIÓN DE PARTIDA", True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(537, 105))
            screen.blit(title_surf, title_rect)

            pygame.display.flip()
            clock.tick(60)

def pantalla2_main(screen, bg_anim):
    ConfiguracionPartida().run(screen, bg_anim)
