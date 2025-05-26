import pygame
import sys
import math
from Config import personajes
from Config import gestor_jugadores

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

def pantalla_personajes(screen, bg_anim):
    pygame.joystick.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pantalla 3")

    # BOTONES
    atras = pygame.transform.scale(pygame.image.load("imagenes/atras.png").convert_alpha(), (40, 40))
    atras_rect = atras.get_rect(topleft=(25, 25))
    siguiente = pygame.transform.scale(pygame.image.load("imagenes/siguiente.png").convert_alpha(), (40, 40))
    siguiente_rect = siguiente.get_rect(bottomright=(screen.get_width() - 25, screen.get_height() - 25))

    # FONDO
    fondo = pygame.transform.scale(pygame.image.load("imagenes/fondobasico.png").convert_alpha(), (750, 450))
    fondo_rect = fondo.get_rect(midright=(screen.get_width(), screen.get_height() // 2))

    # IMÁGENES
    img_default = pygame.transform.scale(pygame.image.load("imagenes/selec_pers.png").convert_alpha(), (110, 110))
    personajes_disponibles = [
        pygame.transform.scale(pygame.image.load("Personajes/orco1.png").convert_alpha(), (110, 110)),
        pygame.transform.scale(pygame.image.load("Personajes/rojo.png").convert_alpha(), (110, 110)),
        pygame.transform.scale(pygame.image.load("Personajes/vampiro1.png").convert_alpha(), (110, 110)),
        pygame.transform.scale(pygame.image.load("Personajes/orco2.png").convert_alpha(), (110, 110)),
        pygame.transform.scale(pygame.image.load("Personajes/orco3.png").convert_alpha(), (110, 110)),

    ]
    nombre_personajes = ["orco1", "rojo", "vampiro1","orco2", "orco3"]

    # POSICIONES
    personajes_centros = []
    x_start = 160
    y_pos = 280
    gap = 70
    for i in range(4):
        x = x_start + i * (110 + gap)
        personajes_centros.append((x, y_pos))

    # INICIALIZAR MANDOS DETECTADOS
    mandos_detectados = {}
    for i in range(pygame.joystick.get_count()):
        joy = pygame.joystick.Joystick(i)
        joy.init()
        mandos_detectados[i] = joy

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
                    num = gestor_jugadores.unir_teclado()
                    if num is not None:
                        personajes.set_personaje(f"jugador_{num}", nombre_personajes[0])
                else:
                    jugador = gestor_jugadores.get_teclado()
                    if event.key == pygame.K_LEFT:
                        jugador["indice"] = (jugador["indice"] - 1) % len(personajes_disponibles)
                    elif event.key == pygame.K_RIGHT:
                        jugador["indice"] = (jugador["indice"] + 1) % len(personajes_disponibles)
                    idx = gestor_jugadores.todos().index(jugador)
                    personajes.set_personaje(f"jugador_{idx+1}", nombre_personajes[jugador["indice"]])

            if event.type == pygame.JOYBUTTONDOWN:
                joy_id = event.joy
                if gestor_jugadores.get_jugador_por_joy(joy_id) is None:
                    num = gestor_jugadores.unir_mando(joy_id)
                    if num is not None:
                        personajes.set_personaje(f"jugador_{num}", nombre_personajes[0])

            if event.type == pygame.JOYHATMOTION:
                joy_id = event.joy
                jugador = gestor_jugadores.get_jugador_por_joy(joy_id)
                if jugador:
                    x, _ = event.value
                    if x != 0:
                        jugador["indice"] = (jugador["indice"] + x) % len(personajes_disponibles)
                        idx = gestor_jugadores.todos().index(jugador)
                        personajes.set_personaje(f"jugador_{idx+1}", nombre_personajes[jugador["indice"]])

        # DIBUJAR
        bg_anim.update()
        bg_anim.draw(screen)
        screen.blit(fondo, fondo_rect)

        for i in range(4):
            jugador = gestor_jugadores.get(i)
            if jugador:
                personaje_img = personajes_disponibles[jugador["indice"]]
                texto = f"JUGADOR {i+1}"
                draw_personaje_con_bombeo(screen, personaje_img, texto, personajes_centros[i], bombeo=False)
            else:
                draw_personaje_con_bombeo(screen, img_default, "Pulsa para unirte", personajes_centros[i], bombeo=True)

        for img, rect in [(atras, atras_rect), (siguiente, siguiente_rect)]:
            if rect.collidepoint(mouse_pos):
                hover = pygame.transform.scale(img, (int(rect.width * 1.1), int(rect.height * 1.1)))
                rect_hover = hover.get_rect(center=rect.center)
                screen.blit(hover, rect_hover)
            else:
                screen.blit(img, rect)

        pygame.display.flip()
        clock.tick(60)
