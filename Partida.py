import pygame
from Mapa import Mapa
from Config import config
from PantallaPrincipal import background_screen
from SpritesPersonajes import Personaje
from ConfiguraciónMandos import gestor_jugadores

def iniciar_partida(_):
    amplada_pantalla = 1235
    alcada_pantalla = 675
    screen = pygame.display.set_mode((amplada_pantalla, alcada_pantalla))

    pygame.joystick.init()
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        j = pygame.joystick.Joystick(i)
        j.init()
        joysticks.append(j)
        print(f"Joystick {i} nom: {j.get_name()}")

    clock = pygame.time.Clock()
    running = True

    mapa = Mapa(config.selected_map)
    nombres_personajes = ["Orco Verde", "Guerrero Rojo", "Vampiro", "Orco Azul", "Orco Marrón"]
    jugadors = Personaje.crear_des_de_gestor(mapa, nombres_personajes)

    teclat_controls = {
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0),
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
    }

    # Identificar el jugador que fa servir teclat (només un)
    jugador_teclat = None
    for pj in jugadors:
        if pj.tipus == "teclat":
            jugador_teclat = pj
            break

    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        for pj in jugadors:
            dx = dy = 0

            if pj == jugador_teclat:
                for tecla, (dx_val, dy_val) in teclat_controls.items():
                    if keys[tecla]:
                        dx, dy = dx_val, dy_val
                        break

            elif pj.tipus == "mando":
                if pj.id_mando is not None and pj.id_mando < len(joysticks):
                    joystick = joysticks[pj.id_mando]
                    if joystick.get_button(13):  # LEFT
                        dx = -1
                    elif joystick.get_button(14):  # RIGHT
                        dx = 1
                    elif joystick.get_button(11):  # UP
                        dy = -1
                    elif joystick.get_button(12):  # DOWN
                        dy = 1
                    else:
                        print(f"ID de mando no vàlid: {pj.id_mando}")
                    continue

            pj.moure(dx, dy)

        mapa.dibuixar(screen)
        for pj in jugadors:
            pj.update(dt)
            pj.dibuixar(screen)

        pygame.display.flip()

    print("Partida finalitzada")
    screen = pygame.display.set_mode((800, 600))
    background_screen(screen)
