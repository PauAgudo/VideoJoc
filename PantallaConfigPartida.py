import pygame
import sys
from PantallaPrincipal import background_screen
from PantallaMapas import pantalla_mapas
from PantallaAudio import pantalla_audio

# CLASE PARA ALMACENAR OPCIONES DE PARTIDA
class ConfiguracionPartida:
    def __init__(self):
        # Valores por defecto
        self.current_number = 4  # Número de jugadores
        self.current_set_index = 1  # Índice para set_options (1,3,5) → inicialmente 3 sets
        self.current_minute = 3  # Número de minutos
        self.current_level_index = 1  # Nivel COM: 0:"Fácil", 1:"Intermedio", 2:"Avanzado"
        self.current_position_index = 0  # Posición inicial: 0:"Fija", 1:"Aleatoria"
        self.current_ultimas_index = {
            "aviones": 0,  # 0:"Sí", 1:"No"
            "Maldiciones": 0,
            "Bloques_final": 0
        }
        # Opciones fijas
        self.set_options = [1, 3, 5]
        self.level_options = ["Fácil", "Intermedio", "Avanzado"]
        self.position_options = ["Fija", "Aleatoria"]
        self.ultimas_opciones = ["Sí", "No"]



    def run(self, screen, bg_anim):
        clock = pygame.time.Clock()
        pygame.display.set_caption("Configuración de Partida")

        # CARGAR BOTONES Y POSICION DE BOTONES

        # BOTON ATRAS
        atras = pygame.image.load("imagenes/atras.png").convert_alpha()
        atras = pygame.transform.scale(atras, (40, 40))
        # Posicion boton atras
        atras_rect = atras.get_rect(topleft = (30,30))

        # BOTON SIGUIENTE
        siguiente = pygame.image.load("imagenes/siguiente.png").convert_alpha()
        siguiente = pygame.transform.scale(siguiente, (40, 40))
        # Posicion boton siguiente
        siguiente_rect = siguiente.get_rect(bottomright = (screen.get_width()-30,screen.get_height()-30))

        # BOTON SETTINGS
        audio = pygame.image.load("imagenes/settings.png").convert_alpha()
        audio = pygame.transform.scale(audio, (50, 40))
        # Posicion boton siguiente
        audio_rect = audio.get_rect(bottomright=(70, screen.get_height() - 30))

        # Cargar imágenes individuales para cada tira
        tiras = {
            "num_jugadores": pygame.image.load("imagenes/tira naranja.png").convert_alpha(),
            "sets": pygame.image.load("imagenes/tira naranja2.png").convert_alpha(),
            "minutos": pygame.image.load("imagenes/tira naranja3.png").convert_alpha(),
            "nivel_COM": pygame.image.load("imagenes/tira naranja4.png").convert_alpha(),
            "pos_inicial": pygame.image.load("imagenes/tira naranja5.png").convert_alpha(),
            "aviones": pygame.image.load("imagenes/tira naranja6.png").convert_alpha(),
            "Maldiciones": pygame.image.load("imagenes/tira naranja7.png").convert_alpha(),
            "Bloques_final": pygame.image.load("imagenes/tira naranja8.png").convert_alpha()
        }

        tamaño_tira = (550, 30)
        for key in tiras:
            tiras[key] = pygame.transform.scale(tiras[key], tamaño_tira)

        # Posiciones específicas para cada tira (los mismos que usas en tu código)
        posiciones = {
            "num_jugadores": (280, 150),
            "sets": (280, 190),
            "minutos": (280, 230),
            "nivel_COM": (280, 270),
            "pos_inicial": (280, 310),
            "aviones": (280, 350),
            "Maldiciones": (280, 390),
            "Bloques_final": (280, 430)
        }
        # Armar diccionario de botones: imagen y su rectángulo
        botones = {}
        for key, pos in posiciones.items():
            botones[key] = {"imagen": tiras[key], "rect": tiras[key].get_rect(topleft=pos)}

        # Cargar las imágenes de flechas
        izquierda = pygame.image.load("imagenes/izquierda.png").convert_alpha()
        izquierda = pygame.transform.scale(izquierda, (30, 30))
        derecha = pygame.image.load("imagenes/derecha.png").convert_alpha()
        derecha = pygame.transform.scale(derecha, (30, 30))
        # Definir las posiciones absolutas de cada flecha para cada tira
        flechas_pos = {
            "num_jugadores": {"izquierda": (520, 150), "derecha": (680, 150)},
            "sets": {"izquierda": (520, 190), "derecha": (680, 190)},
            "minutos": {"izquierda": (520, 230), "derecha": (680, 230)},
            "nivel_COM": {"izquierda": (520, 270), "derecha": (680, 270)},
            "pos_inicial": {"izquierda": (520, 310), "derecha": (680, 310)},
            "aviones": {"izquierda": (520, 350), "derecha": (680, 350)},
            "Maldiciones": {"izquierda": (520, 390), "derecha": (680, 390)},
            "Bloques_final": {"izquierda": (520, 430), "derecha": (680, 430)}
        }

        # Cargar imágenes de números (para mostrar opciones numéricas)
        numeros = {
            1: pygame.image.load("imagenes/1.png").convert_alpha(),
            2: pygame.image.load("imagenes/2.png").convert_alpha(),
            3: pygame.image.load("imagenes/3.png").convert_alpha(),
            4: pygame.image.load("imagenes/4.png").convert_alpha(),
            5: pygame.image.load("imagenes/5.png").convert_alpha(),
            6: pygame.image.load("imagenes/6.png").convert_alpha(),
            7: pygame.image.load("imagenes/7.png").convert_alpha(),
            8: pygame.image.load("imagenes/8.png").convert_alpha(),
            9: pygame.image.load("imagenes/9.png").convert_alpha()
        }
        tamaño_num = (30, 30)
        for key in numeros:
            numeros[key] = pygame.transform.scale(numeros[key], tamaño_num)

        # Posiciones donde se mostrará cada número en las respectivas tiras
        pos_num_jugadores = {1: (600, 150), 2: (600, 150), 3: (600, 150), 4: (600, 150)}
        pos_sets = {1: (600, 190), 3: (600, 190), 5: (600, 190)}
        pos_minuts = {
            1: (600, 230), 2: (600, 230), 3: (600, 230), 4: (600, 230),
            5: (600, 230), 6: (600, 230), 7: (600, 230), 8: (600, 230), 9: (600, 230)
        }
        # Fuente para textos en tiras de opciones no numéricas
        font = pygame.font.SysFont("Arial", 18)

        # Parámetro para el desplazamiento por hover
        shift_amount = 10

    # BUCLE DE LA PANTALLA
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Al pulsar boton atras se sale de pantalla2
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if atras_rect.collidepoint(mouse_pos):
                        background_screen(screen)
                        return

                    if siguiente_rect.collidepoint(mouse_pos):
                        pantalla_mapas(screen, bg_anim)
                    if audio_rect.collidepoint(mouse_pos):
                        pantalla_audio(screen, bg_anim)

                    if botones["num_jugadores"]["rect"].collidepoint(mouse_pos):
                        left_arrow_rect = izquierda.get_rect(
                            topleft=(flechas_pos["num_jugadores"]["izquierda"][0] - shift_amount,
                                     flechas_pos["num_jugadores"]["izquierda"][1])
                        )
                        right_arrow_rect = derecha.get_rect(
                            topleft=(flechas_pos["num_jugadores"]["derecha"][0] - shift_amount,
                                     flechas_pos["num_jugadores"]["derecha"][1])
                        )
                        if left_arrow_rect.collidepoint(mouse_pos):
                            if self.current_number > 1:
                                self.current_number -= 1
                        elif right_arrow_rect.collidepoint(mouse_pos):
                            if self.current_number < 4:
                                self.current_number += 1

                    # --- Segunda tira: Sets (opciones: 1, 3, 5) ---
                    if botones["sets"]["rect"].collidepoint(mouse_pos):
                        left_arrow_rect_sets = izquierda.get_rect(
                            topleft=(flechas_pos["sets"]["izquierda"][0] - shift_amount,
                                     flechas_pos["sets"]["izquierda"][1])
                        )
                        right_arrow_rect_sets = derecha.get_rect(
                            topleft=(flechas_pos["sets"]["derecha"][0] - shift_amount,
                                     flechas_pos["sets"]["derecha"][1])
                        )
                        if left_arrow_rect_sets.collidepoint(mouse_pos):
                            if self.current_set_index > 0:
                                self.current_set_index -= 1
                        elif right_arrow_rect_sets.collidepoint(mouse_pos):
                            if self.current_set_index < len(self.set_options) - 1:
                                self.current_set_index += 1

                    # --- Tercera tira: Minutos (de 1 a 9) ---
                    if botones["minutos"]["rect"].collidepoint(mouse_pos):
                        left_arrow_rect_min = izquierda.get_rect(
                            topleft=(flechas_pos["minutos"]["izquierda"][0] - shift_amount,
                                     flechas_pos["minutos"]["izquierda"][1])
                        )
                        right_arrow_rect_min = derecha.get_rect(
                            topleft=(flechas_pos["minutos"]["derecha"][0] - shift_amount,
                                     flechas_pos["minutos"]["derecha"][1])
                        )
                        if left_arrow_rect_min.collidepoint(mouse_pos):
                            if self.current_minute > 1:
                                self.current_minute -= 1
                        elif right_arrow_rect_min.collidepoint(mouse_pos):
                            if self.current_minute < 9:
                                self.current_minute += 1

                    # --- Cuarta tira: Nivel COM (opciones: "Fácil", "Intermedio", "Avanzado") ---
                    if botones["nivel_COM"]["rect"].collidepoint(mouse_pos):
                        left_arrow_rect_lvl = izquierda.get_rect(
                            topleft=(flechas_pos["nivel_COM"]["izquierda"][0] - shift_amount,
                                     flechas_pos["nivel_COM"]["izquierda"][1])
                        )
                        right_arrow_rect_lvl = derecha.get_rect(
                            topleft=(flechas_pos["nivel_COM"]["derecha"][0] - shift_amount,
                                     flechas_pos["nivel_COM"]["derecha"][1])
                        )
                        if left_arrow_rect_lvl.collidepoint(mouse_pos):
                            if self.current_level_index > 0:
                                self.current_level_index -= 1
                        elif right_arrow_rect_lvl.collidepoint(mouse_pos):
                            if self.current_level_index < len(self.level_options) - 1:
                                self.current_level_index += 1

                    # --- Quinta tira: Posición INICIAL (opciones: "Fija", "Aleatoria") ---
                    if botones["pos_inicial"]["rect"].collidepoint(mouse_pos):
                        left_arrow_rect_pos = izquierda.get_rect(
                            topleft=(flechas_pos["pos_inicial"]["izquierda"][0] - shift_amount,
                                     flechas_pos["pos_inicial"]["izquierda"][1])
                        )
                        right_arrow_rect_pos = derecha.get_rect(
                            topleft=(flechas_pos["pos_inicial"]["derecha"][0] - shift_amount,
                                     flechas_pos["pos_inicial"]["derecha"][1])
                        )
                        if left_arrow_rect_pos.collidepoint(mouse_pos):
                            if self.current_position_index > 0:
                                self.current_position_index -= 1
                        elif right_arrow_rect_pos.collidepoint(mouse_pos):
                            if self.current_position_index < len(self.position_options) - 1:
                                self.current_position_index += 1

                    # --- Últimas tres tiras: "aviones", "Maldiciones", "Bloques_final" (opciones: "Sí", "No") ---
                    for key in ["aviones", "Maldiciones", "Bloques_final"]:
                        if botones[key]["rect"].collidepoint(mouse_pos):
                            left_arrow_rect_bool = izquierda.get_rect(
                                topleft=(flechas_pos[key]["izquierda"][0] - shift_amount,
                                         flechas_pos[key]["izquierda"][1])
                            )
                            right_arrow_rect_bool = derecha.get_rect(
                                topleft=(flechas_pos[key]["derecha"][0] - shift_amount,
                                         flechas_pos[key]["derecha"][1])
                            )
                            if left_arrow_rect_bool.collidepoint(mouse_pos):
                                if self.current_ultimas_index[key] > 0:
                                    self.current_ultimas_index[key] -= 1
                            elif right_arrow_rect_bool.collidepoint(mouse_pos):
                                if self.current_ultimas_index[key] < len(self.ultimas_opciones) - 1:
                                    self.current_ultimas_index[key] += 1

            # Actualizar y dibujar el fondo animado
            bg_anim.update()
            bg_anim.draw(screen)

            # ––––––––––––––––––––––––––––––––––––––––––––––––––––––––
            # Dibujar los elementos en pantalla (las tiras, los textos, botones, etc.)
            # ––––––––––––––––––––––––––––––––––––––––––––––––––––––––
            for key, boton in botones.items():
                rect = boton["rect"]
                is_hover = rect.collidepoint(mouse_pos)
                if is_hover:
                    imagen_hover = pygame.transform.scale(boton["imagen"], (int(rect.width * 1.1), int(rect.height)))
                    rect_hover = imagen_hover.get_rect(center=rect.center)
                    rect_hover.x -= shift_amount
                    screen.blit(imagen_hover, rect_hover)
                    current_rect = rect_hover
                else:
                    screen.blit(boton["imagen"], rect)
                    current_rect = rect

                # Dependiendo de la clave "key", se dibujan los textos o números correspondientes
                if key == "num_jugadores":
                    num_pos = (pos_num_jugadores[self.current_number][0] - shift_amount,
                               pos_num_jugadores[self.current_number][1]) if is_hover else pos_num_jugadores[
                        self.current_number]
                    numero_rect = numeros[self.current_number].get_rect(topleft=num_pos)
                    screen.blit(numeros[self.current_number], numero_rect)
                if key == "sets":
                    set_value = self.set_options[self.current_set_index]
                    set_pos = (pos_sets[set_value][0] - shift_amount, pos_sets[set_value][1]) if is_hover else pos_sets[
                        set_value]
                    set_rect = numeros[set_value].get_rect(topleft=set_pos)
                    screen.blit(numeros[set_value], set_rect)
                if key == "minutos":
                    num_min = (pos_minuts[self.current_minute][0] - shift_amount,
                               pos_minuts[self.current_minute][1]) if is_hover else pos_minuts[self.current_minute]
                    numero_rect = numeros[self.current_minute].get_rect(topleft=num_min)
                    screen.blit(numeros[self.current_minute], numero_rect)
                if key == "nivel_COM":
                    level_text = self.level_options[self.current_level_index]
                    text_surface = font.render(level_text, True, (0, 0, 0))
                    if is_hover:
                        left_arrow_pos = (
                        flechas_pos[key]["izquierda"][0] - shift_amount, flechas_pos[key]["izquierda"][1])
                        right_arrow_pos = (
                        flechas_pos[key]["derecha"][0] - shift_amount, flechas_pos[key]["derecha"][1])
                    else:
                        left_arrow_pos = flechas_pos[key]["izquierda"]
                        right_arrow_pos = flechas_pos[key]["derecha"]
                    left_arrow_rect = izquierda.get_rect(topleft=left_arrow_pos)
                    right_arrow_rect = derecha.get_rect(topleft=right_arrow_pos)
                    center_x = (left_arrow_rect.right + right_arrow_rect.left) // 2
                    center_y = current_rect.centery
                    text_rect = text_surface.get_rect(center=(center_x, center_y))
                    screen.blit(text_surface, text_rect)
                if key == "pos_inicial":
                    pos_text = self.position_options[self.current_position_index]
                    text_surface = font.render(pos_text, True, (0, 0, 0))
                    if is_hover:
                        left_arrow_pos = (
                        flechas_pos[key]["izquierda"][0] - shift_amount, flechas_pos[key]["izquierda"][1])
                        right_arrow_pos = (
                        flechas_pos[key]["derecha"][0] - shift_amount, flechas_pos[key]["derecha"][1])
                    else:
                        left_arrow_pos = flechas_pos[key]["izquierda"]
                        right_arrow_pos = flechas_pos[key]["derecha"]
                    left_arrow_rect = izquierda.get_rect(topleft=left_arrow_pos)
                    right_arrow_rect = derecha.get_rect(topleft=right_arrow_pos)
                    center_x = (left_arrow_rect.right + right_arrow_rect.left) // 2
                    center_y = current_rect.centery
                    text_rect = text_surface.get_rect(center=(center_x, center_y))
                    screen.blit(text_surface, text_rect)
                if key in ["aviones", "Maldiciones", "Bloques_final"]:
                    bool_text = self.ultimas_opciones[self.current_ultimas_index[key]]
                    text_surface = font.render(bool_text, True, (0, 0, 0))
                    if is_hover:
                        left_arrow_pos = (
                        flechas_pos[key]["izquierda"][0] - shift_amount, flechas_pos[key]["izquierda"][1])
                        right_arrow_pos = (
                        flechas_pos[key]["derecha"][0] - shift_amount, flechas_pos[key]["derecha"][1])
                    else:
                        left_arrow_pos = flechas_pos[key]["izquierda"]
                        right_arrow_pos = flechas_pos[key]["derecha"]
                    left_arrow_rect = izquierda.get_rect(topleft=left_arrow_pos)
                    right_arrow_rect = derecha.get_rect(topleft=right_arrow_pos)
                    center_x = (left_arrow_rect.right + right_arrow_rect.left) // 2
                    center_y = current_rect.centery
                    text_rect = text_surface.get_rect(center=(center_x, center_y))
                    screen.blit(text_surface, text_rect)

                # Dibujar las flechas solo si el ratón está sobre la tira
                if is_hover:
                    left_pos = (flechas_pos[key]["izquierda"][0] - shift_amount, flechas_pos[key]["izquierda"][1])
                    right_pos = (flechas_pos[key]["derecha"][0] - shift_amount, flechas_pos[key]["derecha"][1])
                else:
                    left_pos = flechas_pos[key]["izquierda"]
                    right_pos = flechas_pos[key]["derecha"]
                left_arrow_rect = izquierda.get_rect(topleft=left_pos)
                right_arrow_rect = derecha.get_rect(topleft=right_pos)
                if is_hover:
                    if left_arrow_rect.collidepoint(mouse_pos):
                        izquierda_hover = pygame.transform.scale(izquierda, (
                        int(left_arrow_rect.width * 1.15), int(left_arrow_rect.height * 1.15)))
                        izquierda_hover_rect = izquierda_hover.get_rect(center=left_arrow_rect.center)
                        screen.blit(izquierda_hover, izquierda_hover_rect)
                    else:
                        screen.blit(izquierda, left_arrow_rect)
                    if right_arrow_rect.collidepoint(mouse_pos):
                        derecha_hover = pygame.transform.scale(derecha, (
                        int(right_arrow_rect.width * 1.15), int(right_arrow_rect.height * 1.15)))
                        derecha_hover_rect = derecha_hover.get_rect(center=right_arrow_rect.center)
                        screen.blit(derecha_hover, derecha_hover_rect)
                    else:
                        screen.blit(derecha, right_arrow_rect)
            # Fin de bucle for de botones

            # Dibujar botones fijos: ATRÁS, SIGUIENTE, AUDIO
            if atras_rect.collidepoint(mouse_pos):
                atras_hover = pygame.transform.scale(atras, (55, 55))
                atras_rect_hover = atras_hover.get_rect(center=atras_rect.center)
                screen.blit(atras_hover, atras_rect_hover)
            else:
                screen.blit(atras, atras_rect)

            if siguiente_rect.collidepoint(mouse_pos):
                siguiente_hover = pygame.transform.scale(siguiente, (55, 55))
                siguiente_rect_hover = siguiente_hover.get_rect(center=siguiente_rect.center)
                screen.blit(siguiente_hover, siguiente_rect_hover)
            else:
                screen.blit(siguiente, siguiente_rect)

            if audio_rect.collidepoint(mouse_pos):
                audio_hover = pygame.transform.scale(audio, (65, 55))
                audio_rect_hover = audio_hover.get_rect(center=audio_rect.center)
                screen.blit(audio_hover, audio_rect_hover)
            else:
                screen.blit(audio, audio_rect)

            pygame.display.flip()
            clock.tick(60)

# FUNCIÓN A LLAMAR EN MAIN MENU
def pantalla2_main(screen, bg_anim):
    config = ConfiguracionPartida()  # Nuevo objeto con valores por defecto
    config.run(screen, bg_anim)