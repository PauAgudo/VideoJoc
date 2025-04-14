import pygame
import sys
from PantallaPrincipal import background_screen
from PantallaMapas import pantalla_mapas

def pantalla2(screen, bg_anim):
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pantalla 2")

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

    # Escalar todas las tiras al mismo tamaño
    tamaño_tira = (550, 30)
    for key in tiras:
        tiras[key] = pygame.transform.scale(tiras[key], tamaño_tira)

    # Posiciones específicas de cada tira
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

    # Diccionario para almacenar las tiras con su rectángulo
    botones = {}
    for key, pos in posiciones.items():
        botones[key] = {"imagen": tiras[key], "rect": tiras[key].get_rect(topleft=pos)}

    # Cargar imagen derecha izquierda
    izquierda = pygame.image.load("imagenes/izquierda.png").convert_alpha()
    izquierda = pygame.transform.scale(izquierda, (30, 30))
    derecha = pygame.image.load("imagenes/derecha.png").convert_alpha()
    derecha = pygame.transform.scale(derecha, (30, 30))

    # Diccionario para definir las posiciones absolutas de cada flecha en cada opción
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

    # Cargar numeros
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

    # Establecer mismo tamaño para todos
    tamaño_num = (30, 30)
    for key in numeros:
        numeros[key] = pygame.transform.scale(numeros[key], tamaño_num)

    # Posicion donde se colocaran los numeros que hacen referencia al numero de jugadores
    pos_num = {
        1: (600, 150),
        2: (600, 150),
        3: (600, 150),
        4: (600, 150)
    }

    # Posicion donde se colocaran los numeros que hacen referencia al numero de victorias/sets
    pos_sets = {
        1: (600, 190),
        3: (600, 190),
        5: (600, 190)
    }

    # Posicion donde se colocaran el numero de minutos por partida
    pos_minuts = {
        1: (600, 230),
        2: (600, 230),
        3: (600, 230),
        4: (600, 230),
        5: (600, 230),
        6: (600, 230),
        7: (600, 230),
        8: (600, 230),
        9: (600, 230)
    }

    # opciones de TEXTO en Nivel_COM
    font = pygame.font.SysFont("Arial", 18)

# Primera tira es Numero de jugadores
    primera_tira_key = "num_jugadores"
    current_number = 4 #Numero inicial


# Segunda tira es Numero de sets por partida
    set_options = [1, 3, 5]
    current_set_index = 1  # Valor inicial (3 sets)

# Tercera tira es Numero de minutos por ronda en partida
    tercera_tira_key = "minutos"
    current_minute = 3 # Numero inicial

# Cuarta tira es nivel COM
    level_options = ["Fácil", "Intermedio", "Avanzado"]
    current_level_index = 1 #posicion 1 dentro de la lista level_options

# Quinta tira es Posicion INICIAL
    position_options = ["Fija", "Aleatoria"]
    current_position_index = 0 #posicion inicial fija por defecto

# Ulitmas tres tiras "Aviones, Maldiciones,
    ultimas_opciones = ["Sí", "No"]
    current_ultimas_index = {
        "aviones": 0,
        "Maldiciones":0,
        "Bloques_final":0
    }


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
                if siguiente_rect.collidepoint(mouse_pos):
                    pantalla_mapas(screen, bg_anim)

                # Actualización del numero de jugadores (primera tira naranja)
                if primera_tira_key in botones:
                        # Determinar si la tira está en hover para aplicar el desplazamiento
                        is_hover_first = botones[primera_tira_key]["rect"].collidepoint(mouse_pos)
                        if is_hover_first:
                            left_arrow_pos = (flechas_pos[primera_tira_key]["izquierda"][0] - shift_amount,
                                              flechas_pos[primera_tira_key]["izquierda"][1])
                            right_arrow_pos = (flechas_pos[primera_tira_key]["derecha"][0] - shift_amount,
                                               flechas_pos[primera_tira_key]["derecha"][1])
                        else:
                            left_arrow_pos = flechas_pos[primera_tira_key]["izquierda"]
                            right_arrow_pos = flechas_pos[primera_tira_key]["derecha"]

                        # Crear rectángulos de las flechas con la posición calculada
                        left_arrow_rect = izquierda.get_rect(topleft=left_arrow_pos)
                        right_arrow_rect = derecha.get_rect(topleft=right_arrow_pos)

                        # Si se pulsa la flecha izquierda, se decrementa el número (cíclicamente)
                        if left_arrow_rect.collidepoint(mouse_pos):
                            if current_number > 1:
                                current_number -= 1
                            else:
                                current_number = current_number

                        # Si se pulsa la flecha derecha, se incrementa el número (cíclicamente)
                        elif right_arrow_rect.collidepoint(mouse_pos):
                            if current_number < 4:
                                current_number += 1
                            else:
                                current_number = current_number

                # Actualización del número de sets (segunda tira "sets")
                if "sets" in botones:
                    # Determinar si la tira "sets" está en hover para aplicar el desplazamiento
                    is_hover_sets = botones["sets"]["rect"].collidepoint(mouse_pos)
                    if is_hover_sets:
                        left_arrow_pos_sets = (flechas_pos["sets"]["izquierda"][0] - shift_amount,
                                               flechas_pos["sets"]["izquierda"][1])
                        right_arrow_pos_sets = (flechas_pos["sets"]["derecha"][0] - shift_amount,
                                                flechas_pos["sets"]["derecha"][1])
                    else:
                        left_arrow_pos_sets = flechas_pos["sets"]["izquierda"]
                        right_arrow_pos_sets = flechas_pos["sets"]["derecha"]

                    # Crear rectángulos de las flechas para la tira "sets"
                    left_arrow_rect_sets = izquierda.get_rect(topleft=left_arrow_pos_sets)
                    right_arrow_rect_sets = derecha.get_rect(topleft=right_arrow_pos_sets)

                    # Si se pulsa la flecha izquierda, se retrocede cíclicamente en las opciones de sets (1,3,5)
                    if left_arrow_rect_sets.collidepoint(mouse_pos):
                        if current_set_index > 0:
                            current_set_index -= 1
                        else:
                            current_set_index = current_set_index
                    # Si se pulsa la flecha derecha, se avanza cíclicamente en las opciones de sets (1,3,5)
                    elif right_arrow_rect_sets.collidepoint(mouse_pos):
                        if current_set_index < len(set_options) - 1:
                            current_set_index += 1
                        else:
                            current_set_index = current_set_index

                # Actualización del numero de minutos (tercera tira naranja)
                if tercera_tira_key in botones:
                    # Determinar si la tira está en hover para aplicar el desplazamiento
                    is_hover_third = botones[tercera_tira_key]["rect"].collidepoint(mouse_pos)
                    if is_hover_third:
                        left_minute_arrow_pos = (flechas_pos[tercera_tira_key]["izquierda"][0] - shift_amount,
                                          flechas_pos[tercera_tira_key]["izquierda"][1])
                        right_minute_arrow_pos = (flechas_pos[tercera_tira_key]["derecha"][0] - shift_amount,
                                           flechas_pos[tercera_tira_key]["derecha"][1])
                    else:
                        left_minute_arrow_pos = flechas_pos[tercera_tira_key]["izquierda"]
                        right_minute_arrow_pos = flechas_pos[tercera_tira_key]["derecha"]

                    # Crear rectángulos de las flechas con la posición calculada
                    left_minute_arrow_rect = izquierda.get_rect(topleft=left_minute_arrow_pos)
                    right_minute_arrow_rect = derecha.get_rect(topleft=right_minute_arrow_pos)

                    # Si se pulsa la flecha izquierda, se decrementa el número (cíclicamente)
                    if left_minute_arrow_rect.collidepoint(mouse_pos):
                        if current_minute > 1:
                            current_minute -= 1
                        else:
                            current_minute = current_minute

                    # Si se pulsa la flecha derecha, se incrementa el número (cíclicamente)
                    elif right_minute_arrow_rect.collidepoint(mouse_pos):
                        if current_minute < 9:
                            current_minute += 1
                        else:
                            current_minute = current_minute

                # Cuarta tira, nivel COM
                if "nivel_COM" in botones:
                    # Calcular posición de las flechas para la tira "nivel_COM"
                    is_hover_level = botones["nivel_COM"]["rect"].collidepoint(mouse_pos)
                    if is_hover_level:
                        left_arrow_pos_level = (flechas_pos["nivel_COM"]["izquierda"][0] - shift_amount,
                                                flechas_pos["nivel_COM"]["izquierda"][1])
                        right_arrow_pos_level = (flechas_pos["nivel_COM"]["derecha"][0] - shift_amount,
                                                 flechas_pos["nivel_COM"]["derecha"][1])
                    else:
                        left_arrow_pos_level = flechas_pos["nivel_COM"]["izquierda"]
                        right_arrow_pos_level = flechas_pos["nivel_COM"]["derecha"]

                    left_arrow_rect_level = izquierda.get_rect(topleft=left_arrow_pos_level)
                    right_arrow_rect_level = derecha.get_rect(topleft=right_arrow_pos_level)

                    # Actualizar el nivel: si se pulsa la flecha izquierda, se selecciona "Fácil";
                    # si se pulsa la flecha derecha, se selecciona "Avanzado".
                    if left_arrow_rect_level.collidepoint(mouse_pos):
                        if current_level_index > 0:
                            current_level_index -= 1
                    elif right_arrow_rect_level.collidepoint(mouse_pos):
                        if current_level_index < len(level_options) - 1:
                            current_level_index += 1

                # Quinta tira Posicion inicial
                if "pos_inicial" in botones:
                    is_hover_pos = botones["pos_inicial"]["rect"].collidepoint(mouse_pos)

                    if is_hover_pos:
                        left_arrow_pos = (flechas_pos["pos_inicial"]["izquierda"][0] - shift_amount,
                                          flechas_pos["pos_inicial"]["izquierda"][1])
                        right_arrow_pos = (flechas_pos["pos_inicial"]["derecha"][0] - shift_amount,
                                           flechas_pos["pos_inicial"]["derecha"][1])
                    else:
                        left_arrow_pos = flechas_pos["pos_inicial"]["izquierda"]
                        right_arrow_pos = flechas_pos["pos_inicial"]["derecha"]

                    left_arrow_rect = izquierda.get_rect(topleft=left_arrow_pos)
                    right_arrow_rect = derecha.get_rect(topleft=right_arrow_pos)

                    # Cambiar la opción si se pulsa una flecha
                    if left_arrow_rect.collidepoint(mouse_pos):
                        if current_position_index > 0:
                            current_position_index -= 1
                    elif right_arrow_rect.collidepoint(mouse_pos):
                        if current_position_index < len(position_options) - 1:
                            current_position_index += 1

                # Ultimas tres tiras
                for key in ["aviones", "Maldiciones", "Bloques_final"]:
                    if key in botones:
                        is_hover_bool = botones[key]["rect"].collidepoint(mouse_pos)

                        if is_hover_bool:
                            left_arrow_pos = (
                            flechas_pos[key]["izquierda"][0] - shift_amount, flechas_pos[key]["izquierda"][1])
                            right_arrow_pos = (
                            flechas_pos[key]["derecha"][0] - shift_amount, flechas_pos[key]["derecha"][1])
                        else:
                            left_arrow_pos = flechas_pos[key]["izquierda"]
                            right_arrow_pos = flechas_pos[key]["derecha"]

                        left_arrow_rect = izquierda.get_rect(topleft=left_arrow_pos)
                        right_arrow_rect = derecha.get_rect(topleft=right_arrow_pos)

                        # Cambiar valor según la flecha pulsada
                        if left_arrow_rect.collidepoint(mouse_pos):
                            if current_ultimas_index[key] > 0:
                                current_ultimas_index[key] -= 1
                        elif right_arrow_rect.collidepoint(mouse_pos):
                            if current_ultimas_index[key] < len(ultimas_opciones) - 1:
                                current_ultimas_index[key] += 1

        # Actualizar y dibujar el fondo animado
        bg_anim.update()
        bg_anim.draw(screen)


        shift_amount = 10  # cantidad de píxeles para mover a la izquierda

        for key, boton in botones.items():
            rect = boton["rect"]
            is_hover = rect.collidepoint(mouse_pos)

            # Dibujar la tira con efecto hover y movimiento
            if is_hover:
                imagen_hover = pygame.transform.scale(boton["imagen"],
                                                      (int(rect.width * 1.1), int(rect.height)))
                rect_hover = imagen_hover.get_rect(center=rect.center)
                rect_hover.x -= shift_amount  # mover hacia la izquierda
                screen.blit(imagen_hover, rect_hover)
                current_rect = rect_hover
            else:
                screen.blit(boton["imagen"], rect)
                current_rect = rect

            # Para la primera tira, dibujar el número actualizado
            if key == primera_tira_key:
                # Ajustar la posición del número según el estado hover
                if is_hover:
                    num_pos = (pos_num[current_number][0] - shift_amount, pos_num[current_number][1])
                else:
                    num_pos = pos_num[current_number]
                numero_rect = numeros[current_number].get_rect(topleft=num_pos)
                screen.blit(numeros[current_number], numero_rect)

            # Mostrar numero de sets
            if key == "sets":
                set_value = set_options[current_set_index]  # Obtiene 1, 3 o 5 según la opción actual
                if is_hover:
                    set_pos = (pos_sets[set_value][0] - shift_amount, pos_sets[set_value][1])
                else:
                    set_pos = pos_sets[set_value]
                set_rect = numeros[set_value].get_rect(topleft=set_pos)
                screen.blit(numeros[set_value], set_rect)

            # Para la tercera tira, dibujar el número actualizado
            if key == tercera_tira_key:
                # Ajustar la posición del número según el estado hover
                if is_hover:
                    num_min = (pos_minuts[current_minute][0] - shift_amount, pos_minuts[current_minute][1])
                else:
                    num_min = pos_minuts[current_minute]
                numero_rect = numeros[current_minute].get_rect(topleft=num_min)
                screen.blit(numeros[current_minute], numero_rect)

            # Para la cuarta tira nivel COM
            if key == "nivel_COM":
                level_text = level_options[current_level_index]
                text_surface = font.render(level_text, True, (0, 0, 0))  # Color del texto

                # Si la tira está en hover, aplicamos el shift_amount para las posiciones de las flechas
                if is_hover:
                    left_arrow_pos = (flechas_pos[key]["izquierda"][0] - shift_amount, flechas_pos[key]["izquierda"][1])
                    right_arrow_pos = (flechas_pos[key]["derecha"][0] - shift_amount, flechas_pos[key]["derecha"][1])
                else:
                    left_arrow_pos = flechas_pos[key]["izquierda"]
                    right_arrow_pos = flechas_pos[key]["derecha"]

                # Crear los rectángulos de las flechas con la posición calculada
                left_arrow_rect = izquierda.get_rect(topleft=left_arrow_pos)
                right_arrow_rect = derecha.get_rect(topleft=right_arrow_pos)

                # Calcular el centro entre el borde derecho de la flecha izquierda y el borde izquierdo de la flecha derecha
                center_x = (left_arrow_rect.right + right_arrow_rect.left) // 2
                # Usar el centro vertical de la tira (current_rect es el rectángulo ya modificado con hover)
                center_y = current_rect.centery

                # Obtener el rectángulo del texto centrado en ese punto
                text_rect = text_surface.get_rect(center=(center_x, center_y))
                screen.blit(text_surface, text_rect)

            # Mostrar texto para la quinta tira
            if key == "pos_inicial":
                pos_text = position_options[current_position_index]
                text_surface = font.render(pos_text, True, (0, 0, 0))  # texto negro

                # Calcular la posición de las flechas con o sin hover
                if is_hover:
                    left_arrow_pos = (flechas_pos[key]["izquierda"][0] - shift_amount, flechas_pos[key]["izquierda"][1])
                    right_arrow_pos = (flechas_pos[key]["derecha"][0] - shift_amount, flechas_pos[key]["derecha"][1])
                else:
                    left_arrow_pos = flechas_pos[key]["izquierda"]
                    right_arrow_pos = flechas_pos[key]["derecha"]

                # Crear rectángulos de flechas
                left_arrow_rect = izquierda.get_rect(topleft=left_arrow_pos)
                right_arrow_rect = derecha.get_rect(topleft=right_arrow_pos)

                # Calcular el centro entre flechas y centrar verticalmente
                center_x = (left_arrow_rect.right + right_arrow_rect.left) // 2
                center_y = current_rect.centery

                # Dibujar el texto centrado
                text_rect = text_surface.get_rect(center=(center_x, center_y))
                screen.blit(text_surface, text_rect)

            # Dibujar las opciones de las tres ultimas tiras
            if key in ["aviones", "Maldiciones", "Bloques_final"]:
                bool_text = ultimas_opciones[current_ultimas_index[key]]
                text_surface = font.render(bool_text, True, (0, 0, 0))  # negro

                if is_hover:
                    left_arrow_pos = (flechas_pos[key]["izquierda"][0] - shift_amount, flechas_pos[key]["izquierda"][1])
                    right_arrow_pos = (flechas_pos[key]["derecha"][0] - shift_amount, flechas_pos[key]["derecha"][1])
                else:
                    left_arrow_pos = flechas_pos[key]["izquierda"]
                    right_arrow_pos = flechas_pos[key]["derecha"]

                left_arrow_rect = izquierda.get_rect(topleft=left_arrow_pos)
                right_arrow_rect = derecha.get_rect(topleft=right_arrow_pos)

                center_x = (left_arrow_rect.right + right_arrow_rect.left) // 2
                center_y = current_rect.centery

                text_rect = text_surface.get_rect(center=(center_x, center_y))
                screen.blit(text_surface, text_rect)

            # Dibujar flechas y marcar su movimiento cuando el raton esta encima de la tira naranja
            if is_hover:
                left_pos = (flechas_pos[key]["izquierda"][0] - shift_amount, flechas_pos[key]["izquierda"][1])
                right_pos = (flechas_pos[key]["derecha"][0] - shift_amount, flechas_pos[key]["derecha"][1])
            else:
                left_pos = flechas_pos[key]["izquierda"]
                right_pos = flechas_pos[key]["derecha"]

            # Crear rectángulos para las flechas en sus posiciones
            left_arrow_rect = izquierda.get_rect(topleft=left_pos)
            right_arrow_rect = derecha.get_rect(topleft=right_pos)

            # DIBUJAR LAS FLECHAS SOLO SI EL RATÓN ESTÁ SOBRE LA TIRA (is_hover == True)
            if is_hover:
                left_pos = (flechas_pos[key]["izquierda"][0] - shift_amount, flechas_pos[key]["izquierda"][1])
                right_pos = (flechas_pos[key]["derecha"][0] - shift_amount, flechas_pos[key]["derecha"][1])
                left_arrow_rect = izquierda.get_rect(topleft=left_pos)
                right_arrow_rect = derecha.get_rect(topleft=right_pos)
                if left_arrow_rect.collidepoint(mouse_pos):
                    izquierda_hover = pygame.transform.scale(izquierda,
                                                             (int(left_arrow_rect.width * 1.15),
                                                              int(left_arrow_rect.height * 1.15)))
                    izquierda_hover_rect = izquierda_hover.get_rect(center=left_arrow_rect.center)
                    screen.blit(izquierda_hover, izquierda_hover_rect)
                else:
                    screen.blit(izquierda, left_arrow_rect)
                if right_arrow_rect.collidepoint(mouse_pos):
                    derecha_hover = pygame.transform.scale(derecha,
                                                           (int(right_arrow_rect.width * 1.15),
                                                            int(right_arrow_rect.height * 1.15)))
                    derecha_hover_rect = derecha_hover.get_rect(center=right_arrow_rect.center)
                    screen.blit(derecha_hover, derecha_hover_rect)
                else:
                    screen.blit(derecha, right_arrow_rect)

        # Efecto hover para el botón "atrás"
        if atras_rect.collidepoint(mouse_pos):
           # Aumentar el tamaño del botón cuando el ratón esté encima
           atras_hover = pygame.transform.scale(atras, (55, 55))
           atras_rect_hover = atras_hover.get_rect(center=atras_rect.center)
           screen.blit(atras_hover, atras_rect_hover)
        else:
           # Dibujar el botón normal si no hay hover
           screen.blit(atras, atras_rect)

        # Efecto hover para el botón "siguiente"
        if siguiente_rect.collidepoint(mouse_pos):
           # Aumentar el tamaño del botón cuando el ratón esté encima
           siguiente_hover = pygame.transform.scale(siguiente, (55, 55))
           siguiente_rect_hover = siguiente_hover.get_rect(center=siguiente_rect.center)
           screen.blit(siguiente_hover, siguiente_rect_hover)
        else:
           # Dibujar el botón normal si no hay hover
           screen.blit(siguiente, siguiente_rect)

        pygame.display.flip()
        clock.tick(60)