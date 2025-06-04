import pygame
import sys
import math
from ConfiguraciónMandos import gestor_jugadores  # INSTANCIA DETECCION TECLADO Y MANDO
# Diccionario temporal para guardar estado de mandos desconectados
temporizador_listos = {} # Diccionario para guardar si un jugador está listo
estado_mandos_desconectados = {}


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
        texto_render = fuente.render(texto, True, (0, 0, 0))
        texto_rect = texto_render.get_rect(center=(imagen_rect.centerx, imagen_rect.bottom + 50))
        screen.blit(texto_render, texto_rect)
    else:
        if tipo_jugador == "teclado":
            texto = "ENTER para empezar"
        elif tipo_jugador == "mando":
            texto = "OPTIONS para empezar"
        else:
            return
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
    pygame.joystick.quit()
    pygame.joystick.init()
    mandos = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for mando in mandos:
        mando.init()

    clock = pygame.time.Clock()
    pygame.display.set_caption("Pantalla Personajes")

    atras = pygame.transform.scale(pygame.image.load("imagenes/atras.png").convert_alpha(), (40, 40))
    atras_rect = atras.get_rect(topleft=(25, 25))
    siguiente = pygame.transform.scale(pygame.image.load("imagenes/siguiente.png").convert_alpha(), (40, 40))
    siguiente_rect = siguiente.get_rect(bottomright=(screen.get_width() - 25, screen.get_height() - 25))

    fondo = pygame.transform.scale(pygame.image.load("imagenes/fondobasico.png").convert_alpha(), (750, 450))
    fondo_rect = fondo.get_rect(midright=(screen.get_width(), screen.get_height() // 2))

    img_default = pygame.transform.scale(pygame.image.load("imagenes/selec_pers.png").convert_alpha(), (130, 130))
    img_teclado = pygame.transform.scale(pygame.image.load("imagenes/teclado.png").convert_alpha(), (160, 160))
    img_mando = pygame.transform.scale(pygame.image.load("imagenes/mando.png").convert_alpha(), (160, 160))

    flecha_izq = pygame.transform.scale(pygame.image.load("imagenes/flecha_izquierda.png").convert_alpha(), (20, 20))
    flecha_der = pygame.transform.scale(pygame.image.load("imagenes/flecha_derecha.png").convert_alpha(), (20, 20))

    personajes_disponibles = [
        pygame.transform.scale(pygame.image.load("Personajes/orco1.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Personajes/rojo.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Personajes/vampiro1.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Personajes/orco2.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Personajes/orco3.png").convert_alpha(), (90, 90)),
    ]

    nombres_personajes = ["Orco Verde", "Guerrero Rojo", "Vampiro", "Orco Azul", "Orco Marrón"]

    personajes_centros = []
    x_start = 160
    y_pos = 280
    gap = 70
    for i in range(4):
        x = x_start + i * (110 + gap)
        personajes_centros.append((x, y_pos))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if atras_rect.collidepoint(mouse_pos):
                    from PantallaMapas import pantalla_mapas
                    pantalla_mapas(screen, bg_anim)
                    return
                if siguiente_rect.collidepoint(mouse_pos):
                    from MainJoc import pantalla_partida
                    pantalla_partida(screen, bg_anim)
                    return

            if event.type == pygame.KEYDOWN:
                if gestor_jugadores.get_teclado() is None:
                    gestor_jugadores.unir_teclado()
                else:
                    jugador = gestor_jugadores.get_teclado()
                    if event.key == pygame.K_RETURN:
                        temporizador_listos["teclado"] = True
                    elif event.key == pygame.K_b:
                        temporizador_listos["teclado"] = False
                    elif not temporizador_listos.get("teclado"):
                        if event.key == pygame.K_LEFT:
                            jugador["indice"] = (jugador.get("indice", 0) - 1) % len(personajes_disponibles)
                        elif event.key == pygame.K_RIGHT:
                            jugador["indice"] = (jugador.get("indice", 0) + 1) % len(personajes_disponibles)

            if event.type == pygame.JOYBUTTONDOWN:
                joy_id = getattr(event, "instance_id", event.joy)
                if gestor_jugadores.get_jugador_por_joy(joy_id) is None:
                    if joy_id in estado_mandos_desconectados:
                        info = estado_mandos_desconectados.pop(joy_id)
                        gestor_jugadores.unir_mando(joy_id)
                        jugador = gestor_jugadores.get_jugador_por_joy(joy_id)
                        if jugador:
                            jugador["indice"] = info.get("indice", 0)
                    else:
                        gestor_jugadores.unir_mando(joy_id)
                else:
                    if event.button == 7:
                        temporizador_listos[joy_id] = True
                    elif event.button == 1:
                        temporizador_listos[joy_id] = False

            if event.type == pygame.JOYHATMOTION:
                joy_id = getattr(event, "instance_id", event.joy)
                jugador = gestor_jugadores.get_jugador_por_joy(joy_id)
                if jugador:
                    if temporizador_listos.get(joy_id):
                        continue
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
                if jugador["tipo"] == "teclado":
                    base_rect = img_teclado.get_rect(center=pos)
                    screen.blit(img_teclado, base_rect)
                elif jugador["tipo"] == "mando":
                    base_rect = img_mando.get_rect(center=pos)
                    screen.blit(img_mando, base_rect)
                draw_etiqueta_jugador(screen, f"J{i+1}", pos)
                personaje_img = personajes_disponibles[jugador["indice"]]
                nombre_personaje = nombres_personajes[jugador["indice"]]
                tipo_jugador = jugador["tipo"]
                id_jugador = "teclado" if tipo_jugador == "teclado" else jugador.get("id")
                listo = temporizador_listos.get(id_jugador, False)
                rect_img = draw_personaje_con_bombeo(screen, personaje_img, nombre_personaje, pos, flecha_izq, flecha_der, not listo, bombeo=False)
                draw_mensaje_inicio(screen, rect_img, tipo_jugador, listo)
            else:
                draw_personaje_con_bombeo(screen, img_default, "NINGUNO", pos, flecha_izq, flecha_der, False, bombeo=True)

        draw_texto_inferior_bombeo(screen, "Pulsa para unirte", (screen.get_width() // 2, screen.get_height() - 30))

        for img, rect in [(atras, atras_rect), (siguiente, siguiente_rect)]:
            if rect.collidepoint(mouse_pos):
                hover = pygame.transform.scale(img, (int(rect.width * 1.1), int(rect.height * 1.1)))
                rect_hover = hover.get_rect(center=rect.center)
                screen.blit(hover, rect_hover)
            else:
                screen.blit(img, rect)

        # Título
        font2 = pygame.font.Font(None, 36)
        title_surf = font2.render("PERSONAJES Y JUGADORES", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(537, 105))
        screen.blit(title_surf, title_rect)

        pygame.display.flip()
        clock.tick(60)
