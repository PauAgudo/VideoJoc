import pygame
import sys
import math
from ConfiguraciónMandos import gestor_jugadores  # INSTANCIA DETECCION TECLADO Y MANDO
pygame.init()
# AÑADE ESTA LÍNEA ANTES DE CARGAR mixer.Sound
if not pygame.mixer.get_init():
    pygame.mixer.init()
# Añadir justo tras los imports
import os
from Config import personajes
from pygame import mixer

# Inicializar sonidos de selección
SONIDOS_PERSONAJE = {
    "Mork": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Mork.mp3")),
    "Mortis": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Mortis.mp3")),
    "Calvo": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Calvo.mp3")),
    "Guerrero Negro": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Guerrero Negro.mp3")),
    "Guerrero Rojo": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Guerrero Rojo.mp3")),
    "Guerrero Blanco": mixer.Sound(os.path.join("Media", "Sonidos_juego", "Escoger_personaje", "Guerrero Blanco.mp3"))
}
# Opcional: ajustar volumen
for s in SONIDOS_PERSONAJE.values():
    s.set_volume(1.0)

# Diccionario temporal para guardar estado de mandos desconectados
temporizador_listos = {} # Diccionario para guardar si un jugador está listo
estado_mandos_desconectados = {}
recien_unidos = set()  # ← Añade esto fuera del bucle principal

mensaje_error = ""
mensaje_timer = 0

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
        texto = "L para empezar" if tipo_jugador == "teclado" else "Y para empezar"
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

    fondo = pygame.transform.scale(pygame.image.load("Media/Menu/fondobasico.png").convert_alpha(), (750, 450))
    fondo_rect = fondo.get_rect(midright=(screen.get_width(), screen.get_height() // 2))

    img_default = pygame.transform.scale(pygame.image.load("Media/Menu/Pantalla_personajes/selec_pers.png").convert_alpha(), (130, 130))
    img_teclado = pygame.transform.scale(pygame.image.load("Media/Menu/Pantalla_personajes/teclado.png").convert_alpha(), (160, 160))
    img_mando = pygame.transform.scale(pygame.image.load("Media/Menu/Pantalla_personajes/mando.png").convert_alpha(), (160, 160))

    flecha_izq = pygame.transform.scale(pygame.image.load("Media/Menu/Pantalla_personajes/flecha_izquierda.png").convert_alpha(), (20, 20))
    flecha_der = pygame.transform.scale(pygame.image.load("Media/Menu/Pantalla_personajes/flecha_derecha.png").convert_alpha(), (20, 20))

    personajes_disponibles = [
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/orco1.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/rojo.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/vampiro1.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/orco2.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/Warlord.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/vampiro2.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/vampiro3.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/azul.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/blanco.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/negro.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Media/Jugadores/Dibujos/calvo.png").convert_alpha(), (90, 90))
    ]

    nombres_personajes = ["Mork", "Guerrero Rojo", "Mortis", "Grimfang", "Warlord", "Vael", "Sarthus", "Guerrero Azul",
                          "Guerrero Blanco", "Guerrero Negro", "Calvo"]

    personajes_centros = [(160 + i * (110 + 70), 280) for i in range(4)]

    mostrar_mensaje_j1 = False

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

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
                            import Bomberman
                            Bomberman.main()
                            return
                        else:
                            mensaje_error = "Todos tus rivales no están listos"
                            mensaje_timer = pygame.time.get_ticks()
                    else:
                        mensaje_error = "¡Deben estar listos al menos 2 jugadores!"
                        mensaje_timer = pygame.time.get_ticks()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from PantallaMapas import pantalla_mapas
                    gestor_jugadores.reset()
                    temporizador_listos.clear()
                    estado_mandos_desconectados.clear()
                    recien_unidos.clear()
                    pantalla_mapas(screen, bg_anim)
                    return
                if event.key == pygame.K_RETURN:
                    jugador1 = gestor_jugadores.get(0)
                    if jugador1 and jugador1["tipo"] == "teclado":
                        listos = [j for j in temporizador_listos.values() if j]
                        total_conectados = len(gestor_jugadores.jugadores)
                        if len(listos) >= 2:
                            if len(listos) == total_conectados:
                                import Bomberman
                                Bomberman.main()
                                return
                            else:
                                mensaje_error = "Todos tus rivales no están listos"
                        else:
                            mensaje_error = "¡Deben estar listos al menos 2 jugadores!"
                        mensaje_timer = pygame.time.get_ticks()

                if event.key not in (pygame.K_ESCAPE, pygame.K_RETURN):
                    if gestor_jugadores.get_teclado() is None:
                        gestor_jugadores.unir_teclado()
                    else:
                        jugador = gestor_jugadores.get_teclado()
                        if event.key == pygame.K_l:
                            if not temporizador_listos.get("teclado", False):
                                temporizador_listos["teclado"] = True
                                personaje_idx = gestor_jugadores.get_teclado()["indice"]
                                nombre = nombres_personajes[personaje_idx]
                                if nombre in SONIDOS_PERSONAJE:
                                    SONIDOS_PERSONAJE[nombre].play()
                        elif event.key == pygame.K_b:
                            temporizador_listos["teclado"] = False
                        elif not temporizador_listos.get("teclado"):
                            if event.key == pygame.K_LEFT:
                                jugador["indice"] = (jugador.get("indice", 0) - 1) % len(personajes_disponibles)
                            elif event.key == pygame.K_RIGHT:
                                jugador["indice"] = (jugador.get("indice", 0) + 1) % len(personajes_disponibles)


            # Dentro del while running → justo en el manejo del evento
            if event.type == pygame.JOYBUTTONDOWN:

                joy_id = getattr(event, "instance_id", event.joy)
                jugador = gestor_jugadores.get_jugador_por_joy(joy_id)

                # Ignorar primer botón pulsado tras unirse
                if joy_id in recien_unidos:
                    recien_unidos.remove(joy_id)
                    continue  # Saltarse esta pulsación

                if jugador is None:
                    if joy_id in estado_mandos_desconectados:
                        info = estado_mandos_desconectados.pop(joy_id)
                        gestor_jugadores.unir_mando(joy_id)
                        jugador = gestor_jugadores.get_jugador_por_joy(joy_id)
                        if jugador:
                            jugador["indice"] = info.get("indice", 0)
                    else:
                        gestor_jugadores.unir_mando(joy_id)

                    recien_unidos.add(joy_id)  # ← Marcar como recién unido
                    jugador = gestor_jugadores.get_jugador_por_joy(joy_id)

                ## IGNORAR cualquier primer botón tras unirse
                if joy_id in recien_unidos:
                    recien_unidos.remove(joy_id)
                    continue  # ← Saltarse este evento de botón


                # Ahora ya procesamos normalmente
                if event.button == 3:  # Y
                    if not temporizador_listos.get(joy_id, False):
                        temporizador_listos[joy_id] = True
                        jugador = gestor_jugadores.get_jugador_por_joy(joy_id)
                        if jugador:
                            personaje_idx = jugador["indice"]
                            nombre = nombres_personajes[personaje_idx]
                            if nombre in SONIDOS_PERSONAJE:
                                SONIDOS_PERSONAJE[nombre].play()

                elif event.button == 7:  # OPTIONS
                    from PantallaAudio import pantalla_audio
                    pantalla_audio(screen, bg_anim, volver_callback=pantalla_personajes)

                elif event.button == 1:  # B
                    from PantallaMapas import pantalla_mapas
                    gestor_jugadores.reset()
                    temporizador_listos.clear()
                    estado_mandos_desconectados.clear()
                    recien_unidos.clear()
                    pantalla_mapas(screen, bg_anim)

                elif event.button == 2:  # X
                    temporizador_listos[joy_id] = False
                elif event.button == 0:  # A
                    jugador1 = gestor_jugadores.get(0)
                    if jugador1 and jugador1["tipo"] == "mando" and jugador1.get("id") == joy_id:
                        listos = [j for j in temporizador_listos.values() if j]
                        total_conectados = len(gestor_jugadores.jugadores)
                        if len(listos) >= 2:
                            if len(listos) == total_conectados:
                                import Bomberman
                                Bomberman.main()
                                return
                            else:
                                mensaje_error = "Todos tus rivales no están listos"
                        else:
                            mensaje_error = "¡Deben estar listos al menos 2 jugadores!"
                        mensaje_timer = pygame.time.get_ticks()

            if event.type == pygame.JOYHATMOTION:
                joy_id = getattr(event, "instance_id", event.joy)
                jugador = gestor_jugadores.get_jugador_por_joy(joy_id)
                if jugador and not temporizador_listos.get(joy_id):
                    x, _ = event.value
                    if x == -1:
                        jugador["indice"] = (jugador.get("indice", 0) - 1) % len(personajes_disponibles)
                    elif x == 1:
                        jugador["indice"] = (jugador.get("indice", 0) + 1) % len(personajes_disponibles)

            if event.type == pygame.JOYDEVICEREMOVED:
                joy_id = event.instance_id
                jugador = gestor_jugadores.get_jugador_por_joy(joy_id)
                if jugador:
                    estado_mandos_desconectados[joy_id] = jugador.copy()
                    gestor_jugadores.eliminar_jugador_por_joy(joy_id)

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
                draw_etiqueta_jugador(screen, f"J{i+1}", pos)
                personaje_img = personajes_disponibles[jugador["indice"]]
                nombre_personaje = nombres_personajes[jugador["indice"]]
                id_jugador = "teclado" if tipo_jugador == "teclado" else jugador.get("id")
                listo = temporizador_listos.get(id_jugador, False)
                rect_img = draw_personaje_con_bombeo(screen, personaje_img, nombre_personaje, pos, flecha_izq, flecha_der, not listo, bombeo=False)
                draw_mensaje_inicio(screen, rect_img, tipo_jugador, listo)
            else:
                draw_personaje_con_bombeo(screen, img_default, "NINGUNO", pos, flecha_izq, flecha_der, False, bombeo=True)

        draw_texto_inferior_bombeo(screen, "Pulsa para unirte", (screen.get_width() // 2, screen.get_height() - 30))

        for img, rect in [(atras_rotate, atras_rect), (siguiente, siguiente_rect), (audio, audio_rect)]:
            if rect.collidepoint(mouse_pos):
                hover = pygame.transform.scale(img, (int(rect.width * 1.1), int(rect.height * 1.1)))
                rect_hover = hover.get_rect(center=rect.center)
                screen.blit(hover, rect_hover)
            else:
                screen.blit(img, rect)

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

            # Dibujar resaltado ANTES del texto → debajo
            screen.blit(resaltado, (aviso_rect.left, aviso_rect.top + aviso_rect.height // 2 - 4))

            # Dibujar texto encima
            screen.blit(aviso_surf, aviso_rect)

        pygame.display.flip()
        clock.tick(60)
