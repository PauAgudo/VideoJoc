import pygame
import sys
import math
from ConfiguraciónMandos import gestor_jugadores  # INSTANCIA DETECCION TECLADO Y MANDO

def draw_personaje_con_bombeo(screen, imagen, texto, center, bombeo=True):
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

    return imagen_rect

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
    pygame.joystick.init()
    mandos = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for mando in mandos:
        mando.init()


    clock = pygame.time.Clock()
    pygame.display.set_caption("Pantalla 3")

    atras = pygame.transform.scale(pygame.image.load("imagenes/atras.png").convert_alpha(), (40, 40))
    atras_rect = atras.get_rect(topleft=(25, 25))
    siguiente = pygame.transform.scale(pygame.image.load("imagenes/siguiente.png").convert_alpha(), (40, 40))
    siguiente_rect = siguiente.get_rect(bottomright=(screen.get_width() - 25, screen.get_height() - 25))

    fondo = pygame.transform.scale(pygame.image.load("imagenes/fondobasico.png").convert_alpha(), (750, 450))
    fondo_rect = fondo.get_rect(midright=(screen.get_width(), screen.get_height() // 2))

    img_default = pygame.transform.scale(pygame.image.load("imagenes/selec_pers.png").convert_alpha(), (130, 130))
    img_teclado = pygame.transform.scale(pygame.image.load("imagenes/teclado.png").convert_alpha(), (160, 160))
    img_mando = pygame.transform.scale(pygame.image.load("imagenes/mando.png").convert_alpha(), (160, 160))

    personajes_disponibles = [
        pygame.transform.scale(pygame.image.load("Personajes/orco1.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Personajes/rojo.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Personajes/vampiro1.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Personajes/orco2.png").convert_alpha(), (90, 90)),
        pygame.transform.scale(pygame.image.load("Personajes/orco3.png").convert_alpha(), (90, 90)),
    ]

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
                    return

            if event.type == pygame.KEYDOWN:
                if gestor_jugadores.get_teclado() is None:
                    gestor_jugadores.unir_teclado()
                else:
                    jugador = gestor_jugadores.get_teclado()
                    if event.key == pygame.K_LEFT:
                        jugador["indice"] = (jugador.get("indice", 0) - 1) % len(personajes_disponibles)
                    elif event.key == pygame.K_RIGHT:
                        jugador["indice"] = (jugador.get("indice", 0) + 1) % len(personajes_disponibles)

            if event.type == pygame.JOYBUTTONDOWN:
                joy_id = getattr(event, "instance_id", event.joy)
                if gestor_jugadores.get_jugador_por_joy(joy_id) is None:
                    gestor_jugadores.unir_mando(joy_id)

            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    joy_id = getattr(event, "instance_id", event.joy)
                    jugador = gestor_jugadores.get_jugador_por_joy(joy_id)
                    if jugador:
                        if event.value < -0.5:
                            jugador["indice"] = (jugador.get("indice", 0) - 1) % len(personajes_disponibles)
                        elif event.value > 0.5:
                            jugador["indice"] = (jugador.get("indice", 0) + 1) % len(personajes_disponibles)

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
                draw_personaje_con_bombeo(screen, personaje_img, f"JUGADOR {i+1}", pos, bombeo=False)
            else:
                draw_personaje_con_bombeo(screen, img_default, "NINGUNO", pos, bombeo=True)

        draw_texto_inferior_bombeo(screen, "Pulsa para unirte", (screen.get_width() // 2, screen.get_height() - 30))

        for img, rect in [(atras, atras_rect), (siguiente, siguiente_rect)]:
            if rect.collidepoint(mouse_pos):
                hover = pygame.transform.scale(img, (int(rect.width * 1.1), int(rect.height * 1.1)))
                rect_hover = hover.get_rect(center=rect.center)
                screen.blit(hover, rect_hover)
            else:
                screen.blit(img, rect)

        pygame.display.flip()
        clock.tick(60)
