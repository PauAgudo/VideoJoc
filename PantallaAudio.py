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

# Solo un tipo de volumen
TIPOS_DE_VOLUMEN = ["GENERAL"]


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


def dibujar_ui(screen, bg_anim, fondo_gris, rect_fondo_gris, boton_atras, rect_atras, sliders):
    font_titulo = pygame.font.SysFont(None, 30)
    font_opciones = pygame.font.SysFont(None, 20)
    titulo_surf = font_titulo.render("AJUSTES DE AUDIO Y CONTROLES", True, NEGRO)
    titulo_rect = titulo_surf.get_rect(center=(rect_fondo_gris.centerx, rect_fondo_gris.top + 30))

    # Crear casillas de opciones debajo del slider
    slider_rect = sliders[0].rect
    casilla_ancho = 250
    casilla_alto = 50
    espacio_horizontal = 40
    total_ancho = casilla_ancho * 2 + espacio_horizontal
    casillas_top = slider_rect.bottom + 80  # 40 píxeles debajo del slider
    casilla1_left = rect_fondo_gris.centerx - total_ancho // 2
    casilla2_left = rect_fondo_gris.centerx + espacio_horizontal // 2

    casilla1_rect = pygame.Rect(casilla1_left, casillas_top, casilla_ancho, casilla_alto)
    casilla2_rect = pygame.Rect(casilla2_left, casillas_top, casilla_ancho, casilla_alto)

    texto_casilla1 = font_opciones.render("APRENDE LOS CONTROLES", True, NEGRO)
    texto_casilla2 = font_opciones.render("GUÍA DEL JUEGO", True, NEGRO)

    texto1_rect = texto_casilla1.get_rect(center=casilla1_rect.center)
    texto2_rect = texto_casilla2.get_rect(center=casilla2_rect.center)
    font_titulo = pygame.font.SysFont(None, 30)
    titulo_surf = font_titulo.render("AJUSTES DE AUDIO Y CONTROLES", True, NEGRO)
    titulo_rect = titulo_surf.get_rect(center=(rect_fondo_gris.centerx, rect_fondo_gris.top + 30))
    bg_anim.update()
    bg_anim.draw(screen)

    # Dibujar marco gris personalizado
    pygame.draw.rect(screen, GRIS_MEDIO, rect_fondo_gris, border_radius=10)
    pygame.draw.rect(screen, GRIS_OSCURO, rect_fondo_gris, width=4, border_radius=10)
    screen.blit(titulo_surf, titulo_rect)

    # Dibujar casillas
    if casilla1_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, (210, 255, 210), casilla1_rect, border_radius=10)  # hover verde claro
    else:
        pygame.draw.rect(screen, (230, 230, 230), casilla1_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 200, 0), casilla1_rect, width=3, border_radius=10)
        pygame.draw.rect(screen, (0, 200, 0), casilla1_rect, width=3, border_radius=10)
    if casilla2_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, (210, 255, 210), casilla2_rect, border_radius=10)
    else:
        pygame.draw.rect(screen, (230, 230, 230), casilla2_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 200, 0), casilla2_rect, width=3, border_radius=10)


    screen.blit(texto_casilla1, texto1_rect)
    screen.blit(texto_casilla2, texto2_rect)

    # Dibujar nueva casilla roja debajo de las anteriores
    casilla_roja_top = casilla1_rect.bottom + 60
    casilla_roja_rect = pygame.Rect(rect_fondo_gris.centerx - 125, casilla_roja_top, 250, 50)
    if casilla_roja_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, (255, 200, 200), casilla_roja_rect, border_radius=10)
    else:
        pygame.draw.rect(screen, (255, 180, 180), casilla_roja_rect, border_radius=10)
        pygame.draw.rect(screen, (200, 0, 0), casilla_roja_rect, width=3, border_radius=10)

    texto_rojo = font_opciones.render("CERRAR EL JUEGO", True, NEGRO)
    texto_rojo_rect = texto_rojo.get_rect(center=casilla_roja_rect.center)
    screen.blit(texto_rojo, texto_rojo_rect)

    mouse_pos = pygame.mouse.get_pos()
    if rect_atras.collidepoint(mouse_pos):
        screen.blit(
            pygame.transform.scale(
                boton_atras,
                (int(rect_atras.width * 1.1), int(rect_atras.height * 1.1))
            ),
            rect_atras
        )
    else:
        screen.blit(boton_atras, rect_atras)

    font = pygame.font.SysFont(None, 16)
    etiqueta_font = pygame.font.SysFont(None, 20)
    for slider in sliders:
        # Dibujar fondo del slider
        etiqueta_font = pygame.font.SysFont(None, 20)
        etiqueta_surf = etiqueta_font.render("VOLUMEN DEL JUEGO", True, BLANCO)
        etiqueta_x = slider.rect.left - etiqueta_surf.get_width() - 10
        etiqueta_y = slider.rect.y + (slider.rect.height // 2 - etiqueta_surf.get_height() // 2)
        etiqueta_bg_rect = pygame.Rect(etiqueta_x - 5, etiqueta_y - 2, etiqueta_surf.get_width() + 10,
                                       etiqueta_surf.get_height() + 4)

        slider_bg_x = etiqueta_bg_rect.left - 10
        slider_bg_y = etiqueta_bg_rect.top - 15
        slider_bg_width = slider.rect.right + 35 - slider_bg_x + 10
        slider_bg_height = slider.rect.bottom + 15 - slider_bg_y
        slider_bg_rect = pygame.Rect(slider_bg_x, slider_bg_y, slider_bg_width, slider_bg_height)
        pygame.draw.rect(screen, GRIS_CLARO, slider_bg_rect, border_radius=8)
        pygame.draw.rect(screen, GRIS_OSCURO, slider_bg_rect, width=2, border_radius=8)

        slider.draw(screen)

        porcentaje = round(slider.value * 100)
        etiqueta_surf = etiqueta_font.render("VOLUMEN DEL JUEGO", True, BLANCO)
        etiqueta_x = slider.rect.left - etiqueta_surf.get_width() - 10
        etiqueta_y = slider.rect.y + (slider.rect.height // 2 - etiqueta_surf.get_height() // 2)
        etiqueta_bg_rect = pygame.Rect(etiqueta_x - 5, etiqueta_y - 2, etiqueta_surf.get_width() + 10,
                                       etiqueta_surf.get_height() + 4)
        pygame.draw.rect(screen, GRIS_OSCURO, etiqueta_bg_rect, border_radius=6)
        pygame.draw.rect(screen, NEGRO, etiqueta_bg_rect, width=2, border_radius=6)

        etiqueta_x = slider.rect.left - etiqueta_surf.get_width() - 10
        etiqueta_y = slider.rect.y + (slider.rect.height // 2 - etiqueta_surf.get_height() // 2)
        etiqueta_bg_rect = pygame.Rect(etiqueta_x - 5, etiqueta_y - 2, etiqueta_surf.get_width() + 10,
                                       etiqueta_surf.get_height() + 4)
        pygame.draw.rect(screen, GRIS_OSCURO, etiqueta_bg_rect, border_radius=6)
        pygame.draw.rect(screen, NEGRO, etiqueta_bg_rect, width=2, border_radius=6)
        screen.blit(etiqueta_surf, (etiqueta_x, etiqueta_y))

        valor_surf = font.render(f"{porcentaje}%", True, NEGRO)
        valor_x = slider.rect.right + 10
        valor_y = slider.rect.y + (slider.rect.height // 2 - valor_surf.get_height() // 2)
        screen.blit(valor_surf, (valor_x, valor_y))


def manejar_eventos(sliders, rect_atras, screen, bg_anim, volver_callback):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and rect_atras.collidepoint(mouse_pos):
            guardar_volumenes(sliders)
            volver_callback(screen, bg_anim)
            return "ATRAS"

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            guardar_volumenes(sliders)
            volver_callback(screen, bg_anim)
            return "ATRAS"

        if event.type == pygame.JOYBUTTONDOWN and event.button == 1:
            guardar_volumenes(sliders)
            volver_callback(screen, bg_anim)
            return "ATRAS"

        if event.type == pygame.JOYDEVICEADDED:
            nuevo_mando = pygame.joystick.Joystick(event.device_index)
            nuevo_mando.init()

    for slider in sliders:
        slider.update(mouse_pos, mouse_click)

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

    while True:
        resultado = manejar_eventos(sliders, rect_atras, screen, bg_anim, volver_callback)
        if resultado == "ATRAS":
            return

        dibujar_ui(screen, bg_anim, fondo_gris, rect_fondo_gris, boton_atras, rect_atras, sliders)
        pygame.display.flip()
        clock.tick(60)
