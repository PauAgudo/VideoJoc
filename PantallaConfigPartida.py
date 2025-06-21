import pygame
import sys

from ConfiguraciónMandos import gestor_jugadores
from PantallaPrincipal import background_screen
from PantallaMapas import pantalla_mapas
from PantallaAudio import pantalla_audio, GRIS_CLARO
from Config import config

BLANCO = (255, 255, 255)
GRIS_OSCURO = (50, 50, 50)
ROJO = (255, 0, 0)


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

        # ACLARACIÓN VISUAL
        # Cargar imágenes (esto al inicio del archivo o en __init__)
        imagen_boton_b = pygame.image.load("Media/Menu/Botones/boton_B.png").convert_alpha()
        imagen_tecla_escape = pygame.image.load("Media/Menu/Botones/escape.png").convert_alpha()
        imagen_boton_options = pygame.image.load("Media/Menu/Botones/options.png").convert_alpha()
        imagen_boton_a = pygame.image.load("Media/Menu/Botones/boton_A.png").convert_alpha()
        imagen_tecla_s = pygame.image.load("Media/Menu/Botones/tecla_s.png").convert_alpha()
        imagen_tecla_enter = pygame.image.load("Media/Menu/Botones/enter.png").convert_alpha()

        # Redimensionar si es necesario
        imagen_boton_b = pygame.transform.scale(imagen_boton_b, (40, 40))
        imagen_boton_a = pygame.transform.scale(imagen_boton_a, (40, 40))
        imagen_boton_options = pygame.transform.scale(imagen_boton_options, (40, 40))
        imagen_tecla_escape = pygame.transform.scale(imagen_tecla_escape, (40, 40))
        imagen_tecla_s = pygame.transform.scale(imagen_tecla_s, (40, 40))
        imagen_tecla_enter = pygame.transform.scale(imagen_tecla_enter, (50, 40))

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
        izquierda = pygame.transform.scale(pygame.image.load("Media/Menu/Pantalla_configuracion_partida/izquierda.png"),
                                           (30, 30))
        derecha = pygame.transform.scale(pygame.image.load("Media/Menu/Pantalla_configuracion_partida/derecha.png"),
                                         (30, 30))
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

        # Inicializar variable de estado
        last_input_type = "teclado"  # Por defecto empezamos con teclado

        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # === CAMBIO 2: Actualizar la variable de estado con cada evento ===
                if event.type in [pygame.JOYAXISMOTION, pygame.JOYHATMOTION, pygame.JOYBUTTONDOWN]:
                    last_input_type = "mando"
                elif event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                    last_input_type = "teclado"

                # Entrada por joystick o cruceta
                tiempo_actual = pygame.time.get_ticks()
                if mandos and tiempo_actual - last_input_time > mando_delay:
                    joystick = mandos[0]  # Solo usamos el primer mando conectado

                    eje_y = joystick.get_axis(1)
                    eje_x = joystick.get_axis(0)

                    if eje_y < -0.5:  # Joystick arriba
                        last_input_type = "mando"
                        tira_activa_idx = (tira_activa_idx - 1) % len(keys)
                        last_input_time = tiempo_actual
                    elif eje_y > 0.5:  # Joystick abajo
                        last_input_type = "mando"
                        tira_activa_idx = (tira_activa_idx + 1) % len(keys)
                        last_input_time = tiempo_actual

                    elif eje_x < -0.5:  # Joystick izquierda
                        last_input_type = "mando"
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
                        last_input_type = "mando"
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
                        confirmar_salida(screen, bg_anim, fondo_anterior=screen.copy())
                    if event.key == pygame.K_RETURN:
                        ir_a_pantalla_mapas()

                    if event.key == pygame.K_s:
                        pantalla_audio(screen, bg_anim, volver_callback=pantalla2_main)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if atras_rect.collidepoint(mouse_pos):
                        config.__init__()
                        confirmar_salida(screen, bg_anim, fondo_anterior=screen.copy())

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
                                elif key in current_ultimas_index and current_ultimas_index[key] < len(
                                        config.ultimas_opciones) - 1:
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

                    elif event.button == 1:  # Botón B → confirmar salida
                        config.__init__()
                        confirmar_salida(screen, bg_anim, fondo_anterior=screen.copy())

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
                    screen.blit(
                        pygame.transform.scale(pygame.image.load(f"Media/Menu/Pantalla_configuracion_partida/{v}.png"),
                                               (30, 30)),
                        (600 - (shift_amount if hov else 0), posiciones[key][1]))
                if key == "minutos":
                    screen.blit(pygame.transform.scale(
                        pygame.image.load(f"Media/Menu/Pantalla_configuracion_partida/{current_minute}.png"), (30, 30)),
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
                        iz_hover = pygame.transform.scale(izquierda,
                                                          (int(left_rect.width * 1.1), int(left_rect.height * 1.1)))
                        iz_rect_h = iz_hover.get_rect(center=left_rect.center)
                        screen.blit(iz_hover, iz_rect_h)
                    else:
                        screen.blit(izquierda, left_rect)
                    if right_rect.collidepoint(mouse_pos):
                        dr_hover = pygame.transform.scale(derecha,
                                                          (int(right_rect.width * 1.1), int(right_rect.height * 1.1)))
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

            # Lógica de imagen simplificada
            # Ahora la imagen depende del último tipo de input, no de un parámetro fijo
            if last_input_type == "mando":
                imagen = imagen_boton_b
            else:
                imagen = imagen_tecla_escape

            pos_x = atras_rect.right + 10
            pos_y = atras_rect.centery - imagen.get_height() // 2
            screen.blit(imagen, (pos_x, pos_y))

            if last_input_type == "mando":
                imagen = imagen_boton_a
            else:
                imagen = imagen_tecla_enter

            pos_x = siguiente_rect.left - imagen.get_width() - 10
            pos_y = siguiente_rect.centery - imagen.get_height() // 2
            screen.blit(imagen, (pos_x, pos_y))

            if last_input_type == "mando":
                imagen = imagen_boton_options
            else:
                imagen = imagen_tecla_s

            pos_x = audio_rect.right + 10
            pos_y = audio_rect.centery - imagen.get_height() // 2
            screen.blit(imagen, (pos_x, pos_y))

            # Título
            font2 = pygame.font.Font(None, 36)
            title_surf = font2.render("CONFIGURACIÓN DE PARTIDA", True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(537, 105))
            screen.blit(title_surf, title_rect)

            pygame.display.flip()
            clock.tick(60)


def pantalla2_main(screen, bg_anim):
    ConfiguracionPartida().run(screen, bg_anim)


def confirmar_salida(screen, bg_anim, fondo_anterior):
    global last_input_method
    clock = pygame.time.Clock()
    seleccion = 0  # 0 = SI, 1 = NO
    font = pygame.font.SysFont(None, 30)
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        # Restaurar el fondo anterior
        screen.blit(fondo_anterior, (0, 0))

        # Capa translúcida suave
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 40))  # Muy tenue
        screen.blit(overlay, (0, 0))

        # Cuadro central
        ancho_ventana, alto_ventana = 400, 200
        ventana_rect = pygame.Rect(
            (screen.get_width() - ancho_ventana) // 2,
            (screen.get_height() - alto_ventana) // 2,
            ancho_ventana,
            alto_ventana
        )

        pygame.draw.rect(screen, (50, 50, 50), ventana_rect, border_radius=12)
        pygame.draw.rect(screen, BLANCO, ventana_rect, width=3, border_radius=12)

        texto = font.render("¿Desea salir del juego?", True, BLANCO)
        texto_rect = texto.get_rect(center=(ventana_rect.centerx, ventana_rect.top + 50))
        screen.blit(texto, texto_rect)

        # Botones SI y NO
        boton_ancho = 100
        boton_alto = 40
        espacio = 50

        si_rect = pygame.Rect(
            ventana_rect.centerx - boton_ancho - espacio // 2,
            ventana_rect.centery + 30,
            boton_ancho,
            boton_alto
        )
        no_rect = pygame.Rect(
            ventana_rect.centerx + espacio // 2,
            ventana_rect.centery + 30,
            boton_ancho,
            boton_alto
        )

        # Hover con ratón
        hover_si = si_rect.collidepoint(mouse_pos)
        hover_no = no_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                last_input_method = "mouse"
                if hover_si:
                    seleccion = 0
                elif hover_no:
                    seleccion = 1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                last_input_method = "mouse"
                if si_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif no_rect.collidepoint(mouse_pos):
                    return

            elif event.type == pygame.KEYDOWN:
                last_input_method = "keyboard"
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    seleccion = 0
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    seleccion = 1
                elif event.key == pygame.K_RETURN:
                    if seleccion == 0:
                        pygame.quit()
                        sys.exit()
                    else:
                        return

            elif event.type == pygame.JOYHATMOTION:
                last_input_method = "gamepad"
                hat_x, hat_y = event.value
                if hat_x < 0:
                    seleccion = 0
                elif hat_x > 0:
                    seleccion = 1

            elif event.type == pygame.JOYAXISMOTION:
                last_input_method = "gamepad"
                axis_x = event.axis
                axis_value = event.value
                if axis_x == 0:
                    if axis_value < -0.5:
                        seleccion = 0
                    elif axis_value > 0.5:
                        seleccion = 1

            elif event.type == pygame.JOYBUTTONDOWN:
                last_input_method = "gamepad"
                if event.button == 0:  # Botón A
                    if seleccion == 0:
                        pygame.quit()
                        sys.exit()
                    else:
                        return

        # Pintar botones con hover y selección
        for i, rect in enumerate([si_rect, no_rect]):
            if i == 0:
                hover = hover_si
                texto_btn = "SI"
            else:
                hover = hover_no
                texto_btn = "NO"

            if seleccion == i:
                color_fondo = (220, 255, 220)  # mismo color para teclado o ratón
            else:
                color_fondo = GRIS_OSCURO

            pygame.draw.rect(screen, color_fondo, rect, border_radius=6)
            pygame.draw.rect(screen, BLANCO, rect, width=2, border_radius=6)

            label = font.render(texto_btn, True, ROJO)
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)

        pygame.display.flip()
        clock.tick(60)