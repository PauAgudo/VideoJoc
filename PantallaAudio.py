import pygame
import sys
from Config import audio

# Constantes para los colores
AZUL = (0, 0, 255)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)
GRIS_CLARO = (200, 200, 200)
GRIS_MEDIO = (150, 150, 150)
GRIS_OSCURO = (100, 100, 100)
VERDE_HOVER = (210, 255, 210)
ROJO_HOVER = (255, 200, 200)

# Solo un tipo de volumen
TIPOS_DE_VOLUMEN = ["GENERAL"]

last_input_method = "mouse"  # Puede ser "mouse" o "keyboard"
selected_element_index = 0  # Índice del elemento seleccionado (0 para slider, 1 para casilla1, etc.)
hover_casillas = [False] * 4  # Lista para controlar el hover de las casillas
ultimo_index_hover = 0  # Índice del último hover para evitar cambios innecesarios

class SliderRect:
    def __init__(self, x, y, width, height, initial=1.0, tipo_volumen="GENERAL"):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = initial
        self.handle_size = 15
        self.tipo_volumen = tipo_volumen

    def draw(self, screen):
        x, y, w, h = self.rect
        center_x = x + int(self.value * w)
        ancho_azul = center_x - x
        ancho_blanco = w - ancho_azul

        if ancho_azul > 0:
            pygame.draw.rect(screen, AZUL, (x, y, ancho_azul, h))
        if ancho_blanco > 0:
            pygame.draw.rect(screen, BLANCO, (center_x, y, ancho_blanco, h))
        pygame.draw.rect(screen, NEGRO, self.rect, 1)

        handle_left = center_x - self.handle_size // 2
        pygame.draw.rect(screen, ROJO, (handle_left,
                                        y + (h - self.handle_size) // 2,
                                        self.handle_size,
                                        self.handle_size))

    def update(self, mouse_pos, mouse_click):
        if mouse_click and self.rect.collidepoint(mouse_pos):
            rel_x = mouse_pos[0] - self.rect.left
            self.value = max(0.0, min(1.0, rel_x / self.rect.width))


def inicializar_componentes_ui(screen):
    try:
        boton_atras = pygame.transform.scale(
            pygame.image.load("Media/Menu/Botones/siguiente.png"),
            (40, 40))
        boton_atras_rotate = pygame.transform.rotate(boton_atras, 180)
    except pygame.error:
        print("Error al cargar la imagen: siguiente.png")
        sys.exit(1)
    rect_atras = boton_atras_rotate.get_rect(topleft=(25, 25))

    ancho = 750
    alto = 450
    fondo_gris = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    rect_fondo_gris = fondo_gris.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    return boton_atras_rotate, rect_atras, fondo_gris, rect_fondo_gris


def crear_sliders(rect_fondo_gris):
    base_x, base_y = audio.slider_pos
    ancho_slider, alto_slider = audio.slider_size
    sliders = []

    slider = SliderRect(
        rect_fondo_gris.left + base_x,
        rect_fondo_gris.top + base_y,
        ancho_slider,
        alto_slider,
        initial=audio.volume,
        tipo_volumen="GENERAL"
    )
    sliders.append(slider)
    return sliders


def dibujar_seleccion(screen, rect, seleccionado, color_hover, color_fondo, color_borde):
    if seleccionado:
        pygame.draw.rect(screen, color_hover, rect, border_radius=10)
    else:
        pygame.draw.rect(screen, color_fondo, rect, border_radius=10)
    pygame.draw.rect(screen, color_borde, rect, width=3, border_radius=10)

def cambiar_a_teclado():
    global last_input_method, hover_casillas
    last_input_method = "keyboard"
    hover_casillas = [False] * len(hover_casillas)


def cambiar_a_raton():
    global last_input_method
    last_input_method = "mouse"



def dibujar_ui(screen, bg_anim, fondo_gris, rect_fondo_gris, boton_atras, rect_atras, sliders):
    global hover_casillas, casillas_rects, last_input_method, ultimo_hover_index

    font_titulo = pygame.font.SysFont(None, 30)
    font_opciones = pygame.font.SysFont(None, 20)

    titulo_surf = font_titulo.render("AJUSTES DE AUDIO Y CONTROLES", True, NEGRO)
    titulo_rect = titulo_surf.get_rect(center=(rect_fondo_gris.centerx, rect_fondo_gris.top + 30))

    slider_rect = sliders[0].rect
    casilla_ancho = 250
    casilla_alto = 50
    espacio_horizontal = 40
    total_ancho = casilla_ancho * 2 + espacio_horizontal
    casillas_top = slider_rect.bottom + 80
    casilla1_left = rect_fondo_gris.centerx - total_ancho // 2
    casilla2_left = rect_fondo_gris.centerx + espacio_horizontal // 2

    casilla1_rect = pygame.Rect(casilla1_left, casillas_top, casilla_ancho, casilla_alto)
    casilla2_rect = pygame.Rect(casilla2_left, casillas_top, casilla_ancho, casilla_alto)
    casilla_roja_top = casilla1_rect.bottom + 60
    casilla_roja_rect = pygame.Rect(rect_fondo_gris.centerx - 125, casilla_roja_top, 250, 50)

    casillas_rects = [sliders[0].rect, casilla1_rect, casilla2_rect, casilla_roja_rect]

    mouse_pos = pygame.mouse.get_pos()
    bg_anim.update()
    bg_anim.draw(screen)

    pygame.draw.rect(screen, GRIS_MEDIO, rect_fondo_gris, border_radius=10)
    pygame.draw.rect(screen, GRIS_OSCURO, rect_fondo_gris, width=4, border_radius=10)
    screen.blit(titulo_surf, titulo_rect)

    mouse_pos = pygame.mouse.get_pos()

    if last_input_method == "mouse":
        # Asegurar que 'ultimo_hover_index' esté definido y válido
        if 'ultimo_hover_index' not in globals():
            ultimo_hover_index = 0  # fallback por si aún no se ha definido

        nueva_hover_casilla = -1
        for i, rect in enumerate(casillas_rects):
            if rect.collidepoint(mouse_pos):
                nueva_hover_casilla = i
                break

        if nueva_hover_casilla != -1:
            hover_casillas = [j == nueva_hover_casilla for j in range(len(casillas_rects))]
            ultimo_hover_index = nueva_hover_casilla
        else:
            # Mantener la última casilla hover conocida
            hover_casillas = [j == ultimo_hover_index for j in range(len(casillas_rects))]
    else:
        hover_casillas = [False] * len(casillas_rects)

    if last_input_method == "mouse":
        seleccionados = hover_casillas
    else:
        seleccionados = [selected_element_index == i for i in range(4)]

    dibujar_seleccion(screen, casilla1_rect, seleccionados[1], VERDE_HOVER, (230, 230, 230), (0, 200, 0))
    dibujar_seleccion(screen, casilla2_rect, seleccionados[2], VERDE_HOVER, (230, 230, 230), (0, 200, 0))
    dibujar_seleccion(screen, casilla_roja_rect, seleccionados[3], ROJO_HOVER, (255, 180, 180), (200, 0, 0))

    texto_casilla1 = font_opciones.render("APRENDE LOS CONTROLES", True, NEGRO)
    texto_casilla2 = font_opciones.render("GUÍA DEL JUEGO", True, NEGRO)
    texto_rojo = font_opciones.render("CERRAR EL JUEGO", True, NEGRO)

    screen.blit(texto_casilla1, texto_casilla1.get_rect(center=casilla1_rect.center))
    screen.blit(texto_casilla2, texto_casilla2.get_rect(center=casilla2_rect.center))
    screen.blit(texto_rojo, texto_rojo.get_rect(center=casilla_roja_rect.center))

    if rect_atras.collidepoint(mouse_pos):
        screen.blit(pygame.transform.scale(boton_atras, (int(rect_atras.width * 1.1), int(rect_atras.height * 1.1))), rect_atras)
    else:
        screen.blit(boton_atras, rect_atras)

    font = pygame.font.SysFont(None, 16)
    etiqueta_font = pygame.font.SysFont(None, 20)

    for i, slider in enumerate(sliders):
        etiqueta_surf = etiqueta_font.render("VOLUMEN DEL JUEGO", True, BLANCO)
        etiqueta_x = slider.rect.left - etiqueta_surf.get_width() - 10
        etiqueta_y = slider.rect.y + (slider.rect.height // 2 - etiqueta_surf.get_height() // 2)
        etiqueta_bg_rect = pygame.Rect(etiqueta_x - 5, etiqueta_y - 2, etiqueta_surf.get_width() + 10, etiqueta_surf.get_height() + 4)

        slider_bg_x = etiqueta_bg_rect.left - 10
        slider_bg_y = etiqueta_bg_rect.top - 15
        slider_bg_width = slider.rect.right + 35 - slider_bg_x + 10
        slider_bg_height = slider.rect.bottom + 15 - slider_bg_y
        slider_bg_rect = pygame.Rect(slider_bg_x, slider_bg_y, slider_bg_width, slider_bg_height)

        if seleccionados[0]:
            pygame.draw.rect(screen, (220, 220, 220), slider_bg_rect, border_radius=8)
        else:
            pygame.draw.rect(screen, GRIS_CLARO, slider_bg_rect, border_radius=8)
        pygame.draw.rect(screen, GRIS_OSCURO, slider_bg_rect, width=2, border_radius=8)

        slider.draw(screen)
        porcentaje = round(slider.value * 100)
        pygame.draw.rect(screen, GRIS_OSCURO, etiqueta_bg_rect, border_radius=6)
        pygame.draw.rect(screen, NEGRO, etiqueta_bg_rect, width=2, border_radius=6)
        screen.blit(etiqueta_surf, (etiqueta_x, etiqueta_y))

        valor_surf = font.render(f"{porcentaje}%", True, NEGRO)
        valor_x = slider.rect.right + 10
        valor_y = slider.rect.y + (slider.rect.height // 2 - valor_surf.get_height() // 2)
        screen.blit(valor_surf, (valor_x, valor_y))



def manejar_eventos(sliders, rect_atras, screen, bg_anim, volver_callback):
    global selected_element_index
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            cambiar_a_raton()

        # Verificar si ha hecho clic en alguna casilla
        for i, rect in enumerate(casillas_rects):
            if rect.collidepoint(mouse_pos):
                selected_element_index = i
                break

        if event.type == pygame.MOUSEBUTTONDOWN:
            cambiar_a_raton()
            if rect_atras.collidepoint(mouse_pos):
                guardar_volumenes(sliders)
                volver_callback(screen, bg_anim)
                return "ATRAS"
            for i, rect in enumerate(casillas_rects):
                if rect.collidepoint(mouse_pos):
                    selected_element_index = i  # Actualizar selección con clic

                    if i == 1:
                        from AprendeControles import pantalla_controles
                        guardar_volumenes(sliders)
                        pantalla_controles(screen, bg_anim)
                        return
                    elif i == 2:
                        from GuiaJuego import pantalla_guia
                        guardar_volumenes(sliders)
                        pantalla_guia(screen, bg_anim)
                        return
                    elif i == 3:
                        guardar_volumenes(sliders)
                        confirmar_salida(screen, bg_anim, fondo_anterior=screen.copy())
                        return

        if event.type == pygame.KEYDOWN:
            cambiar_a_teclado()
            if event.key == pygame.K_ESCAPE:
                guardar_volumenes(sliders)
                volver_callback(screen, bg_anim)
                return "ATRAS"
            elif event.key == pygame.K_DOWN:
                selected_element_index = (selected_element_index + 1) % 4
            elif event.key == pygame.K_UP:
                selected_element_index = (selected_element_index - 1) % 4
            elif selected_element_index == 0:
                if event.key == pygame.K_RIGHT:
                    sliders[0].value = min(1.0, sliders[0].value + 0.01)
                elif event.key == pygame.K_LEFT:
                    sliders[0].value = max(0.0, sliders[0].value - 0.01)

            elif event.key == pygame.K_RETURN:
                if selected_element_index == 1:
                    # Acción: ir a controles
                    from AprendeControles import pantalla_controles
                    guardar_volumenes(sliders)
                    pantalla_controles(screen, bg_anim)
                    return
                elif selected_element_index == 2:
                    # Acción: ir a guía del juego
                    from GuiaJuego import pantalla_guia
                    guardar_volumenes(sliders)
                    pantalla_guia(screen, bg_anim)
                    return
                elif selected_element_index == 3:
                    # Acción: cerrar el juego
                    guardar_volumenes(sliders)
                    confirmar_salida(screen, bg_anim, fondo_anterior=screen.copy())
                    return

        if event.type == pygame.JOYBUTTONDOWN and event.button == 1:
            guardar_volumenes(sliders)
            volver_callback(screen, bg_anim)
            return "ATRAS"

        if event.type == pygame.JOYDEVICEADDED:
            nuevo_mando = pygame.joystick.Joystick(event.device_index)
            nuevo_mando.init()

    # Interacción con sliders por ratón
    for slider in sliders:
        slider.update(mouse_pos, mouse_click)

    # Actualizar volumen
    for slider in sliders:
        if slider.tipo_volumen == "GENERAL":
            pygame.mixer.music.set_volume(slider.value)
            audio.volume = slider.value
            audio.volume_effects = slider.value
            for efecto in audio.efectos.values():
                efecto.set_volume(slider.value)



def guardar_volumenes(sliders):
    for slider in sliders:
        if slider.tipo_volumen == "GENERAL":
            audio.volume = slider.value
            audio.volume_effects = slider.value
            for efecto in audio.efectos.values():
                efecto.set_volume(slider.value)
    audio.save()



def pantalla_audio(screen, bg_anim, volver_callback):
    global selected_element_index, last_input_method, hover_casillas, ultimo_hover_index
    selected_element_index = 0
    last_input_method = "keyboard"
    hover_casillas = [False] * 4
    ultimo_hover_index = 0

    pygame.display.set_caption("Pantalla Audio")
    clock = pygame.time.Clock()

    if bg_anim is None:
        class DummyBG:
            def update(self): pass
            def draw(self, s): pass
        bg_anim = DummyBG()

    pygame.joystick.init()
    mandos = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for mando in mandos:
        mando.init()

    boton_atras, rect_atras, fondo_gris, rect_fondo_gris = inicializar_componentes_ui(screen)
    sliders = crear_sliders(rect_fondo_gris)

    # FORZAMOS ESTADO INICIAL
    selected_element_index = 0
    last_input_method = "keyboard"
    hover_casillas = [False, False, False, False]

    while True:
        resultado = manejar_eventos(sliders, rect_atras, screen, bg_anim, volver_callback)
        if resultado == "ATRAS":
            return

        dibujar_ui(screen, bg_anim, fondo_gris, rect_fondo_gris, boton_atras, rect_atras, sliders)
        pygame.display.flip()
        clock.tick(60)


# CONFIRMAR CIERRE DEL JUEGO
def confirmar_salida(screen, bg_anim, fondo_anterior):
    global last_input_method
    clock = pygame.time.Clock()
    seleccion = 0  # 0 = SI, 1 = NO
    font = pygame.font.SysFont(None, 30)
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        # Restaurar el fondo anterior
        screen.blit(fondo_anterior, (0, 0))

        # Capa translúcida suave
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 40))  # Muy tenue
        screen.blit(overlay, (0, 0))

        # Cuadro central
        ancho_ventana, alto_ventana = 400, 200
        ventana_rect = pygame.Rect(
            (screen.get_width() - ancho_ventana) // 2,
            (screen.get_height() - alto_ventana) // 2,
            ancho_ventana,
            alto_ventana
        )

        pygame.draw.rect(screen, (50, 50, 50), ventana_rect, border_radius=12)
        pygame.draw.rect(screen, BLANCO, ventana_rect, width=3, border_radius=12)

        texto = font.render("¿Desea salir del juego?", True, BLANCO)
        texto_rect = texto.get_rect(center=(ventana_rect.centerx, ventana_rect.top + 50))
        screen.blit(texto, texto_rect)

        # Botones SI y NO
        boton_ancho = 100
        boton_alto = 40
        espacio = 50

        si_rect = pygame.Rect(
            ventana_rect.centerx - boton_ancho - espacio // 2,
            ventana_rect.centery + 30,
            boton_ancho,
            boton_alto
        )
        no_rect = pygame.Rect(
            ventana_rect.centerx + espacio // 2,
            ventana_rect.centery + 30,
            boton_ancho,
            boton_alto
        )

        # Hover con ratón
        hover_si = si_rect.collidepoint(mouse_pos)
        hover_no = no_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                last_input_method = "mouse"
                if hover_si:
                    seleccion = 0
                elif hover_no:
                    seleccion = 1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                last_input_method = "mouse"
                if si_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif no_rect.collidepoint(mouse_pos):
                    return

            elif event.type == pygame.KEYDOWN:
                last_input_method = "keyboard"
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    seleccion = 0
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    seleccion = 1
                elif event.key == pygame.K_RETURN:
                    if seleccion == 0:
                        pygame.quit()
                        sys.exit()
                    else:
                        return

        # Pintar botones con hover y selección
        for i, rect in enumerate([si_rect, no_rect]):
            if i == 0:
                hover = hover_si
                texto_btn = "SI"
            else:
                hover = hover_no
                texto_btn = "NO"

            if seleccion == i:
                color_fondo = (220, 255, 220)  # mismo color para teclado o ratón
            else:
                color_fondo = GRIS_OSCURO

            pygame.draw.rect(screen, color_fondo, rect, border_radius=6)
            pygame.draw.rect(screen, BLANCO, rect, width=2, border_radius=6)

            label = font.render(texto_btn, True, ROJO)
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)

        pygame.display.flip()
        clock.tick(60)

