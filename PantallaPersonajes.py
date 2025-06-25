import pygame
import sys
import math
from ConfiguraciónMandos import gestor_jugadores  # INSTANCIA DETECCION TECLADO Y MANDO
pygame.init()

if not pygame.mixer.get_init():
    pygame.mixer.init()
import os
from pygame import mixer

# Inicializar sonidos de selección
SONIDOS_PERSONAJE = {
    "Mork": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Yeeaah.mp3")),
    "Mortis": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Mortis.mp3")),
    "Calvo": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Calvo.mp3")),
    "Guerrero Negro": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Guerrero Negro.mp3")),
    "Guerrero Rojo": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Guerrero Rojo.mp3")),
    "Guerrero Blanco": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Guerrero Blanco.mp3")),
    "Vael": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Vael.mp3")),
    "Grimfang": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Grimfang.mp3")),
    "Guerrero Azul": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Sonido raro.mp3")),
    "Warlord": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Warlord.mp3")),
    "Ragnar": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Gladiador.mp3")),
    "Sarthus": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Gladiador.mp3")),

}
# Opcional: ajustar volumen
for s in SONIDOS_PERSONAJE.values():
    s.set_volume(1.0)

# Diccionario temporal para guardar estado de mandos desconectados
temporizador_listos = {}  # Diccionario para guardar si un jugador está listo
estado_mandos_desconectados = {}
recien_unidos = set()

mensaje_error = ""
mensaje_timer = 0

def reiniciar_estado_personajes():
    global temporizador_listos, estado_mandos_desconectados, recien_unidos, mensaje_error, mensaje_timer
    temporizador_listos.clear()
    estado_mandos_desconectados.clear()
    recien_unidos.clear()
    mensaje_error = ""
    mensaje_timer = 0
    print("[PANTALLA_PERSONAJES] Estado local reseteado.")


def draw_personaje_con_bombeo(screen, imagen, texto, center, flecha_izq, flecha_der, mostrar_flechas, bombeo=True):
    tiempo = pygame.time.get_ticks() / 300.0
    factor = 1 + 0.02 * math.sin(tiempo) if bombeo else 1.0

    ancho_original, alto_original = imagen.get_size()
    ancho_bombeo = int(ancho_original * factor)
    alto_bombeo = int(alto_original * factor)
    imagen_bombeada = pygame.transform.scale(imagen, (ancho_bombeo, alto_bombeo))
    imagen_rect = imagen_bombeada.get_rect(center=center)
    screen.blit(imagen_bombeada, imagen_rect)

    fuente = pygame.font.Font(None, size=20)
    texto_render = fuente.render(texto, True, (0, 0, 0))
    texto_rect = texto_render.get_rect(center=(center[0], imagen_rect.bottom + 10))
    screen.blit(texto_render, texto_rect)

    if mostrar_flechas:
        y_flechas = texto_rect.centery
        flecha_izq_rect = flecha_izq.get_rect(midright=(center[0] - 52, y_flechas))
        flecha_der_rect = flecha_der.get_rect(midleft=(center[0] + 52, y_flechas))
        screen.blit(flecha_izq, flecha_izq_rect)
        screen.blit(flecha_der, flecha_der_rect)

    return imagen_rect


def draw_mensaje_inicio(screen, imagen_rect, tipo_jugador, listo):
    fuente = pygame.font.Font(None, size=22)
    if listo:
        pygame.draw.rect(screen, (255, 255, 0), (imagen_rect.centerx - 60, imagen_rect.bottom + 35, 120, 30))
        texto = "LISTO"
    else:
        texto = "Enter para empezar" if tipo_jugador == "teclado" else "A para empezar"
    texto_render = fuente.render(texto, True, (0, 0, 0))
    texto_rect = texto_render.get_rect(center=(imagen_rect.centerx, imagen_rect.bottom + 50))
    screen.blit(texto_render, texto_rect)


def draw_texto_inferior_bombeo(screen, texto, pos_centro):
    tiempo = pygame.time.get_ticks() / 300.0
    factor = 1 + 0.02 * math.sin(tiempo)
    fuente = pygame.font.Font(None, size=26)
    texto_render = fuente.render(texto, True, (255, 255, 255))
    ancho = int(texto_render.get_width() * factor)
    alto = int(texto_render.get_height() * factor)
    texto_escalado = pygame.transform.scale(texto_render, (ancho, alto))
    rect = texto_escalado.get_rect(center=pos_centro)
    screen.blit(texto_escalado, rect)


def draw_etiqueta_jugador(screen, texto, posicion):
    fuente = pygame.font.Font(None, size=24)
    texto_render = fuente.render(texto, True, (0, 0, 0))
    texto_rect = texto_render.get_rect()
    texto_rect.topright = (posicion[0] + 70, posicion[1] - 70)
    screen.blit(texto_render, texto_rect)


def pantalla_personajes(screen, bg_anim):
    global mensaje_error, mensaje_timer

    pygame.joystick.init()
    mandos = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for mando in mandos:
        mando.init()

    clock = pygame.time.Clock()
    pygame.display.set_caption("Pantalla Personajes")

    # BOTON ATRAS
    atras = pygame.transform.scale(pygame.image.load("Media/Menu/Botones/siguiente.png"), (40, 40))
    atras_rotate = pygame.transform.rotate(atras, 180)
    atras_rect = atras_rotate.get_rect(bottomright=(70, screen.get_height() - 25))

    # BOTON SIGUIENTE
    siguiente = pygame.transform.scale(pygame.image.load("Media/Menu/Botones/siguiente.png").convert_alpha(), (40, 40))
    siguiente_rect = siguiente.get_rect(bottomright=(screen.get_width() - 25, screen.get_height() - 25))

    # BOTON SETTINGS
    audio = pygame.transform.scale(pygame.image.load("Media/Menu/Botones/settings.png"), (50, 40))
    audio_rect = audio.get_rect(topleft=(25, 25))

    # ACLARACIÓN VISUAL
    # Cargar imágenes (esto al inicio del archivo o en __init__)
    imagen_boton_b = pygame.image.load("Media/Menu/Botones/boton_B.png").convert_alpha()
    imagen_tecla_escape = pygame.image.load("Media/Menu/Botones/escape.png").convert_alpha()
    imagen_boton_options = pygame.image.load("Media/Menu/Botones/options.png").convert_alpha()
    imagen_boton_a = pygame.image.load("Media/Menu/Botones/boton_A.png").convert_alpha()
    imagen_tecla_control = pygame.image.load("Media/Menu/Botones/tecla_control.png").convert_alpha()
    imagen_tecla_enter = pygame.image.load("Media/Menu/Botones/enter.png").convert_alpha()

    # Redimensionar si es necesario
    imagen_boton_b = pygame.transform.scale(imagen_boton_b, (50, 50))
    imagen_boton_a = pygame.transform.scale(imagen_boton_a, (50, 50))
    imagen_boton_options = pygame.transform.scale(imagen_boton_options, (40, 40))
    imagen_tecla_escape = pygame.transform.scale(imagen_tecla_escape, (40, 40))
    imagen_tecla_control = pygame.transform.scale(imagen_tecla_control, (50, 40))
    imagen_tecla_enter = pygame.transform.scale(imagen_tecla_enter, (50, 40))

    # FONDO
    fondo = pygame.transform.scale(pygame.image.load("Media/Menu/fondobasico.png").convert_alpha(), (750, 450))
    fondo_rect = fondo.get_rect(midright=(screen.get_width(), screen.get_height() // 2))

    img_default = pygame.transform.scale(
        pygame.image.load("Media/Menu/Pantalla_personajes/selec_pers.png").convert_alpha(), (130, 130))
    img_teclado = pygame.transform.scale(
        pygame.image.load("Media/Menu/Pantalla_personajes/teclado.png").convert_alpha(), (160, 160))
    img_mando = pygame.transform.scale(pygame.image.load("Media/Menu/Pantalla_personajes/mando.png").convert_alpha(),
                                       (160, 160))

    flecha_izq = pygame.transform.scale(
        pygame.image.load("Media/Menu/Pantalla_personajes/flecha_izquierda.png").convert_alpha(), (20, 20))
    flecha_der = pygame.transform.scale(
        pygame.image.load("Media/Menu/Pantalla_personajes/flecha_derecha.png").convert_alpha(), (20, 20))

    personajes_disponibles = [
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/Mork.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/Guerrero Rojo.png").convert_alpha(),
                               (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/Mortis.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/Grimfang.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/Warlord.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/Vael.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/Sarthus.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/Guerrero Azul.png").convert_alpha(),
                               (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/Guerrero Blanco.png").convert_alpha(),
                               (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/Guerrero Negro.png").convert_alpha(),
                               (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/calvo.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/ragnar.png").convert_alpha(), (90, 90))
    ]

    nombres_personajes = ["Mork", "Guerrero Rojo", "Mortis", "Grimfang", "Warlord", "Vael", "Sarthus", "Guerrero Azul",
                          "Guerrero Blanco", "Guerrero Negro", "Calvo", "Ragnar"]

    personajes_centros = [(160 + i * (110 + 70), 280) for i in range(4)]

    mostrar_mensaje_j1 = False

    THRESHOLD = 0.6
    DEADZONE = 0.3
    joystick_ready = {}

    last_input_type = "teclado"

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --------- DETECCIÓN DE TIPO DE INPUT ------------
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]:
                last_input_type = "teclado"
            elif event.type in [pygame.JOYBUTTONDOWN, pygame.JOYAXISMOTION, pygame.JOYHATMOTION]:
                last_input_type = "mando"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if atras_rect.collidepoint(mouse_pos):
                    from PantallaMapas import pantalla_mapas
                    gestor_jugadores.reset()
                    temporizador_listos.clear()
                    estado_mandos_desconectados.clear()
                    recien_unidos.clear()
                    pantalla_mapas(screen, bg_anim)
                    return

                if siguiente_rect.collidepoint(mouse_pos):
                    listos = [j for j in temporizador_listos.values() if j]
                    total_conectados = len(gestor_jugadores.jugadores)
                    total_listos = len(listos)

                if audio_rect.collidepoint(mouse_pos):
                    from PantallaAudio import pantalla_audio
                    pantalla_audio(screen, bg_anim, volver_callback=pantalla_personajes)

                    if total_listos >= 2:
                        if total_listos == total_conectados:
                            from Bomberman import iniciar_partida
                            iniciar_partida(screen)
                            return
                        else:
                            mensaje_error = "Todos tus rivales no están listos"
                            mensaje_timer = pygame.time.get_ticks()
                    else:
                        mensaje_error = "¡Deben estar listos al menos 2 jugadores!"
                        mensaje_timer = pygame.time.get_ticks()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    jugador_teclado = gestor_jugadores.get_teclado()

                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    from PantallaAudio import pantalla_audio
                    pantalla_audio(screen, bg_anim, volver_callback=pantalla_personajes)

                    # Si no hay un jugador con teclado asignado, vuelve a mapas.
                    if jugador_teclado is None:
                        from PantallaMapas import pantalla_mapas
                        gestor_jugadores.reset()
                        temporizador_listos.clear()
                        estado_mandos_desconectados.clear()
                        recien_unidos.clear()
                        pantalla_mapas(screen, bg_anim)
                        return

                    # Si el jugador con teclado existe, aplicamos la nueva lógica.
                    id_jugador = "teclado"
                    # Regla 1: Si está "LISTO", solo se le quita el estado.
                    if temporizador_listos.get(id_jugador, False):
                        temporizador_listos[id_jugador] = False
                    # Regla 2: Si NO está "LISTO"...
                    else:
                        if gestor_jugadores.get(0) == jugador_teclado:
                            from PantallaMapas import pantalla_mapas
                            gestor_jugadores.reset()
                            temporizador_listos.clear()
                            estado_mandos_desconectados.clear()
                            recien_unidos.clear()
                            pantalla_mapas(screen, bg_anim)
                            return
                        else:
                            if id_jugador in temporizador_listos:
                                del temporizador_listos[id_jugador]
                            gestor_jugadores.eliminar_teclado()

                # Si el teclado no participa, se une con cualquier tecla y se detiene.
                if gestor_jugadores.get_teclado() is None:
                    # La primera pulsación de cualquier tecla (excepto ESC) solo une al jugador.
                    gestor_jugadores.unir_teclado()
                    # 'continue' salta al siguiente evento, ignorando el código de abajo en esta pulsación.
                    continue

                # Si el teclado YA participa, se procesan las acciones.
                jugador = gestor_jugadores.get_teclado()
                if jugador:
                    if event.key == pygame.K_RETURN:
                        # Si ya está listo (2da pulsación), y es J1, intenta empezar (3ra pulsación).
                        if temporizador_listos.get("teclado", False):
                            jugador1 = gestor_jugadores.get(0)
                            if jugador1 and jugador1["tipo"] == "teclado":
                                listos = [j for j in temporizador_listos.values() if j]
                                total_conectados = len(gestor_jugadores.jugadores)
                                if len(listos) >= 2:
                                    if len(listos) == total_conectados:
                                        from Bomberman import iniciar_partida
                                        iniciar_partida(screen)
                                        return
                                    else:
                                        mensaje_error = "Todos tus rivales no están listos"
                                else:
                                    mensaje_error = "¡Deben estar listos al menos 2 jugadores!"
                                mensaje_timer = pygame.time.get_ticks()
                        # Si no está listo (1ra pulsación después de unirse), se pone listo.
                        else:
                            temporizador_listos["teclado"] = True
                            personaje_idx = jugador["indice"]
                            nombre = nombres_personajes[personaje_idx]
                            if nombre in SONIDOS_PERSONAJE:
                                SONIDOS_PERSONAJE[nombre].play()

                    elif not temporizador_listos.get("teclado"):
                        if event.key == pygame.K_LEFT:
                            jugador["indice"] = (jugador.get("indice", 0) - 1) % len(personajes_disponibles)
                        elif event.key == pygame.K_RIGHT:
                            jugador["indice"] = (jugador.get("indice", 0) + 1) % len(personajes_disponibles)

            if event.type == pygame.JOYBUTTONDOWN:
                instance_id = event.instance_id
                jugador = gestor_jugadores.get_jugador_por_joy(instance_id)

                # Si el mando no participa, se une con cualquier botón y se detiene.
                if jugador is None:
                    gestor_jugadores.unir_mando(event.joy)
                    continue

                # Si el mando YA participa, se procesan las acciones.
                if event.button == 0:  # Botón A
                    if temporizador_listos.get(instance_id, False):
                        jugador1 = gestor_jugadores.get(0)
                        if jugador1 and jugador1["tipo"] == "mando" and jugador1.get("instance_id") == instance_id:
                            listos = [j for j in temporizador_listos.values() if j]
                            total_conectados = len(gestor_jugadores.jugadores)
                            if len(listos) >= 2:
                                if len(listos) == total_conectados:
                                    from Bomberman import iniciar_partida
                                    iniciar_partida(screen)
                                    return
                                else:
                                    mensaje_error = "Todos tus rivales no están listos"
                            else:
                                mensaje_error = "¡Deben estar listos al menos 2 jugadores!"
                            mensaje_timer = pygame.time.get_ticks()
                    else:
                        temporizador_listos[instance_id] = True
                        personaje_idx = jugador["indice"]
                        nombre = nombres_personajes[personaje_idx]
                        if nombre in SONIDOS_PERSONAJE:
                            SONIDOS_PERSONAJE[nombre].play()

                elif event.button in (7, 9):  # OPTIONS
                    from PantallaAudio import pantalla_audio
                    pantalla_audio(screen, bg_anim, volver_callback=pantalla_personajes)

                elif event.button == 1:  # B (Atrás)
                    # La lógica se aplica al jugador que pulsó el botón.
                    # Regla 1: Si está "LISTO", solo se le quita el estado.
                    if temporizador_listos.get(instance_id, False):
                        temporizador_listos[instance_id] = False
                    # Regla 2: Si NO está "LISTO"...
                    else:
                        if gestor_jugadores.get(0) == jugador:
                            from PantallaMapas import pantalla_mapas
                            gestor_jugadores.reset()
                            temporizador_listos.clear()
                            estado_mandos_desconectados.clear()
                            recien_unidos.clear()
                            pantalla_mapas(screen, bg_anim)
                            return
                        else:
                            if instance_id in temporizador_listos:
                                del temporizador_listos[instance_id]
                            gestor_jugadores.eliminar_jugador_por_joy(instance_id)

                elif event.button == 0:  # A (Botón de acción principal)
                    # Si el jugador ya está listo, y es el Jugador 1, intenta iniciar la partida
                    if temporizador_listos.get(instance_id, False):
                        jugador1 = gestor_jugadores.get(0)
                        if jugador1 and jugador1["tipo"] == "mando" and jugador1.get("id") == instance_id:
                            listos = [j for j in temporizador_listos.values() if j]
                            total_conectados = len(gestor_jugadores.jugadores)
                            if len(listos) >= 2:
                                if len(listos) == total_conectados:
                                    from Bomberman import iniciar_partida
                                    iniciar_partida(screen)
                                    return
                                else:
                                    mensaje_error = "Todos tus rivales no están listos"
                            else:
                                mensaje_error = "¡Deben estar listos al menos 2 jugadores!"
                            mensaje_timer = pygame.time.get_ticks()
                    # Si el jugador no está listo, lo marca como "LISTO"
                    else:
                        temporizador_listos[instance_id] = True
                        if jugador:
                            personaje_idx = jugador["indice"]
                            nombre = nombres_personajes[personaje_idx]
                            if nombre in SONIDOS_PERSONAJE:
                                SONIDOS_PERSONAJE[nombre].play()
            if event.type == pygame.JOYHATMOTION:
                instance_id = event.instance_id
                jugador = gestor_jugadores.get_jugador_por_joy(instance_id)
                if jugador and not temporizador_listos.get(instance_id):
                    x, _ = event.value
                    if x == -1:
                        jugador["indice"] = (jugador.get("indice", 0) - 1) % len(personajes_disponibles)
                    elif x == 1:
                        jugador["indice"] = (jugador.get("indice", 0) + 1) % len(personajes_disponibles)

            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:  # Eje horizontal del joystick izquierdo
                    instance_id = event.instance_id
                    jugador = gestor_jugadores.get_jugador_por_joy(instance_id)

                    if jugador and not temporizador_listos.get(instance_id):
                        # Solo ejecutar si el jugador no está marcado como listo
                        if abs(event.value) > THRESHOLD and joystick_ready.get(instance_id, True):
                            if event.value > 0:
                                jugador["indice"] = (jugador.get("indice", 0) + 1) % len(personajes_disponibles)
                            else:
                                jugador["indice"] = (jugador.get("indice", 0) - 1) % len(personajes_disponibles)

                            joystick_ready[instance_id] = False
                        elif abs(event.value) < DEADZONE:
                            joystick_ready[instance_id] = True  # Rearme

            if event.type == pygame.JOYDEVICEREMOVED:
                instance_id = event.instance_id
                jugador = gestor_jugadores.get_jugador_por_joy(instance_id)
                if jugador:
                    if instance_id in temporizador_listos:
                        del temporizador_listos[instance_id]

                    if instance_id in joystick_ready:
                        del joystick_ready[instance_id]
                    gestor_jugadores.eliminar_jugador_por_joy(instance_id)

            if event.type == pygame.JOYDEVICEADDED:
                nuevo_mando = pygame.joystick.Joystick(event.device_index)
                nuevo_mando.init()

        bg_anim.update()
        bg_anim.draw(screen)
        screen.blit(fondo, fondo_rect)

        for i in range(4):
            pos = personajes_centros[i]
            jugador = gestor_jugadores.get(i)
            if jugador and "indice" in jugador:
                tipo_jugador = jugador["tipo"]
                base_rect = (img_teclado if tipo_jugador == "teclado" else img_mando).get_rect(center=pos)
                screen.blit(img_teclado if tipo_jugador == "teclado" else img_mando, base_rect)
                draw_etiqueta_jugador(screen, f"J{i + 1}", pos)
                personaje_img = personajes_disponibles[jugador["indice"]]
                nombre_personaje = nombres_personajes[jugador["indice"]]
                id_jugador = "teclado" if tipo_jugador == "teclado" else jugador.get("instance_id")
                listo = temporizador_listos.get(id_jugador, False)
                rect_img = draw_personaje_con_bombeo(screen, personaje_img, nombre_personaje, pos, flecha_izq,
                                                     flecha_der, not listo, bombeo=False)
                draw_mensaje_inicio(screen, rect_img, tipo_jugador, listo)
            else:
                draw_personaje_con_bombeo(screen, img_default, "NINGUNO", pos, flecha_izq, flecha_der, False,
                                          bombeo=True)

        draw_texto_inferior_bombeo(screen, "Pulsa para unirte", (screen.get_width() // 2, screen.get_height() - 30))

        for img, rect in [(atras_rotate, atras_rect), (siguiente, siguiente_rect), (audio, audio_rect)]:
            if rect.collidepoint(mouse_pos):
                hover = pygame.transform.scale(img, (int(rect.width * 1.1), int(rect.height * 1.1)))
                rect_hover = hover.get_rect(center=rect.center)
                screen.blit(hover, rect_hover)
            else:
                screen.blit(img, rect)

        # logica ayuda visual botones
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
            imagen = imagen_tecla_control

        pos_x = audio_rect.right + 10
        pos_y = audio_rect.centery - imagen.get_height() // 2
        screen.blit(imagen, (pos_x, pos_y))

        font2 = pygame.font.Font(None, 36)
        title_surf = font2.render("PERSONAJES Y JUGADORES", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(537, 105))
        screen.blit(title_surf, title_rect)

        # Mostrar mensaje "Jugador 1 puedes iniciar partida"
        listos = [j for j in temporizador_listos.values() if j]
        total_conectados = len(gestor_jugadores.jugadores)
        mostrar_mensaje_j1 = len(listos) >= 2 and len(listos) == total_conectados

        if mensaje_error and pygame.time.get_ticks() - mensaje_timer < 3000:
            font = pygame.font.Font(None, 30)
            error_surf = font.render(mensaje_error, True, (255, 0, 0))
            error_rect = error_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() - 100))
            screen.blit(error_surf, error_rect)

        if mostrar_mensaje_j1:
            font = pygame.font.Font(None, 28)
            aviso_surf = font.render("Jugador 1 puedes iniciar partida", True, (0, 100, 0))  # Texto verde oscuro
            aviso_rect = aviso_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() - 130))

            # Crear superficie de resaltado semitransparente debajo del texto
            resaltado = pygame.Surface((aviso_rect.width, aviso_rect.height // 2), pygame.SRCALPHA)
            resaltado.fill((180, 255, 180, 120))  # Verde fosforito con alfa (transparente)

            # Dibujar resaltado ANTES del texto
            screen.blit(resaltado, (aviso_rect.left, aviso_rect.top + aviso_rect.height // 2 - 4))

            # Dibujar texto encima
            screen.blit(aviso_surf, aviso_rect)

        pygame.display.flip()
        clock.tick(60)
