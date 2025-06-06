import pygame
from Mapa import Mapa
from Config import config
from PantallaPrincipal import background_screen
from SpritesPersonajes import Personaje
from GestorGlobal import gestor_jugadores

def iniciar_partida(_):
    amplada_pantalla = 1235
    alcada_pantalla = 675
    screen = pygame.display.set_mode((amplada_pantalla, alcada_pantalla))

    pygame.mixer.music.stop()  # Detener cualquier música previa

    pygame.mixer.init()
    pygame.mixer.music.load("assets/Banda Sonora/banda_sonora_juego.mp3")
    pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen de la música
    pygame.mixer.music.play(-1)  # Reproduce la música en bucle

    pygame.joystick.init()
    mandos = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for mando in mandos:
        mando.init()

    joysticks = {mando.get_instance_id(): mando for mando in mandos}

    clock = pygame.time.Clock()
    running = True

    mapa = Mapa(config.selected_map)
    print("Jugadors registrats en gestor_jugadores:")
    for j in gestor_jugadores.jugadores:
        print(f" - tipus: {j['tipo']}, id: {j['id']}, indice: {j['indice']}")
    nombres_personajes = ["Orco Verde", "Guerrero Rojo", "Vampiro", "Orco Azul", "Orco Marrón"]
    jugadors = Personaje.crear_des_de_gestor(mapa, nombres_personajes)

    print("Personatges creats:")
    for p in jugadors:
        print(f" - tipus: {p.tipus}, id_mando: {p.id_mando}")

    teclat_controls = {
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0),
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
    }

    llista_bombes = []
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        for i, pj in enumerate(jugadors):
            dx = dy = 0

            if pj.tipus == "teclado":
                for tecla, (dx_val, dy_val) in teclat_controls.items():
                    if keys[tecla]:
                        dx, dy = dx_val, dy_val
                        break
                pj.moure(dx, dy)

            elif pj.tipus == "mando":
                jugador_info = gestor_jugadores.get_jugador_por_joy(pj.id_mando)
                if not jugador_info:
                    print(f"No trobat jugador registrat per joystick amb id {pj.id_mando}")
                    continue

                joystick = joysticks.get(pj.id_mando)
                if not joystick:
                    print(f"No trobat dispositiu joystick amb id {pj.id_mando}")
                    continue

                axis_x = joystick.get_axis(0)
                axis_y = joystick.get_axis(1)
                umbral = 0.5
                if axis_x < -umbral:
                    dx = -1
                elif axis_x > umbral:
                    dx = 1
                if axis_y < -umbral:
                    dy = -1
                elif axis_y > umbral:
                    dy = 1

                if dx != 0 or dy != 0:
                    pj.moure(dx, dy)

            if pj.tipus == "teclado" and keys[pygame.K_RETURN]:
                pj.colocar_bomba(llista_bombes)
            elif pj.tipus == "mando" and joystick.get_button(0):
                pj.colocar_bomba(llista_bombes)

        mapa.dibuixar(screen)
        for pj in jugadors:
            pj.update(dt)
            pj.dibuixar(screen)

        # Update i dibuix de bombes
        for bomba in llista_bombes:
            bomba.update()
            bomba.dibuixar(screen)

        pygame.display.flip()

    print("Partida finalitzada")
    pygame.mixer.music.stop()  # Detener la música al finalizar la partida
    screen = pygame.display.set_mode((800, 600))
    background_screen(screen)
