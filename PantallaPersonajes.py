import pygame
import sys
import math
from Config import personajes

def draw_personaje_con_bombeo(screen, imagen, texto, center, bombeo=True):
    tiempo = pygame.time.get_ticks() / 300.0
    factor = 1 + 0.05 * math.sin(tiempo) if bombeo else 1.0

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
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pantalla 3")

    # BOTONES
    atras = pygame.image.load("imagenes/atras.png").convert_alpha()
    atras = pygame.transform.scale(atras, (40, 40))
    atras_rect = atras.get_rect(topleft=(25, 25))

    siguiente = pygame.image.load("imagenes/siguiente.png").convert_alpha()
    siguiente = pygame.transform.scale(siguiente, (40, 40))
    siguiente_rect = siguiente.get_rect(bottomright=(screen.get_width() - 25, screen.get_height() - 25))

    # FONDO
    fondo = pygame.transform.scale(pygame.image.load("imagenes/fondobasico.png").convert_alpha(), (750, 450))
    fondo_rect = fondo.get_rect(midright=(screen.get_width(), screen.get_height() // 2))

    # IMÁGENES
    img_default = pygame.image.load("imagenes/selec_pers.png").convert_alpha()
    img_default = pygame.transform.scale(img_default, (110, 110))

    personajes_disponibles = [
        pygame.transform.scale(pygame.image.load("Personajes/orco1.png").convert_alpha(), (110, 110)),
        pygame.transform.scale(pygame.image.load("Personajes/rojo.png").convert_alpha(), (110, 110)),
        pygame.transform.scale(pygame.image.load("Personajes/vampiro1.png").convert_alpha(), (110, 110)),
    ]

    nombre_personajes = ["orco1", "rojo", "vampiro1"]

    # POSICIONES
    personajes_centros = []
    x_start = 160
    y_pos = 280
    gap = 70
    for i in range(4):
        x = x_start + i * (110 + gap)
        personajes_centros.append((x, y_pos))

    jugador_1_unido = False
    indice_personaje_j1 = 0  # orco1 por defecto

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
                if not jugador_1_unido:
                    jugador_1_unido = True
                    indice_personaje_j1 = 0
                    personajes.set_personaje("jugador_1", "orco1")
                else:
                    if event.key == pygame.K_RIGHT:
                        indice_personaje_j1 = (indice_personaje_j1 + 1) % len(personajes_disponibles)
                    elif event.key == pygame.K_LEFT:
                        indice_personaje_j1 = (indice_personaje_j1 - 1) % len(personajes_disponibles)

                    personaje_nombre = nombre_personajes[indice_personaje_j1]
                    personajes.set_personaje("jugador_1", personaje_nombre)

        bg_anim.update()
        bg_anim.draw(screen)
        screen.blit(fondo, fondo_rect)

        # JUGADOR 1
        if jugador_1_unido:
            img_j1 = personajes_disponibles[indice_personaje_j1]
            texto_j1 = "¡JUGADOR 1!"
            draw_personaje_con_bombeo(screen, img_j1, texto_j1, personajes_centros[0], bombeo=False)
        else:
            draw_personaje_con_bombeo(screen, img_default, "Pulsa para unirte", personajes_centros[0], bombeo=True)

        # JUGADORES 2 A 4
        for i in range(1, 4):
            draw_personaje_con_bombeo(screen, img_default, "Pulsa para unirte", personajes_centros[i], bombeo=True)

        # BOTONES
        for img, rect in [(atras, atras_rect), (siguiente, siguiente_rect)]:
            if rect.collidepoint(mouse_pos):
                hover = pygame.transform.scale(img, (int(rect.width * 1.1), int(rect.height * 1.1)))
                rect_hover = hover.get_rect(center=rect.center)
                screen.blit(hover, rect_hover)
            else:
                screen.blit(img, rect)

        pygame.display.flip()
        clock.tick(60)
