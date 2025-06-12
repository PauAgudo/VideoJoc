import pygame
import sys
from Config import audio

# Constantes para los colores
AZUL = (0, 0, 255)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)

# Tipos de volumen que se pueden ajustar
TIPOS_DE_VOLUMEN = ["MÚSICA", "EFECTOS"]


class SliderRect:
    # CLASE PARA LOS SLIDERS
    def __init__(self, x, y, width, height, initial=1.0, tipo_volumen="MÚSICA"):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = initial
        self.handle_size = 15
        self.tipo_volumen = tipo_volumen

    def draw(self, screen):
        # DIBUJAR SLIDERS
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
    # Configuración del botón "Atrás"
    try:
        boton_atras = pygame.transform.scale(
            pygame.image.load("Media/Menu/Botones/siguiente.png"),
            (40, 40))
        boton_atras_rotate = pygame.transform.rotate(boton_atras, 180)
    except pygame.error:
        print("Error al cargar la imagen: siguiente.png")
        sys.exit(1)
    rect_atras = boton_atras_rotate.get_rect(topleft=(25, 25))

    # Fondo gris
    try:
        fondo_gris = pygame.transform.scale(
            pygame.image.load("Media/Menu/gris.png"),
            (750, 450)
        )
    except pygame.error:
        print("Error al cargar la imagen: gris.png")
        sys.exit(1)
    rect_fondo_gris = fondo_gris.get_rect(
        midright=(screen.get_width(), screen.get_height() // 2)
    )

    return boton_atras_rotate, rect_atras, fondo_gris, rect_fondo_gris


def crear_sliders(rect_fondo_gris):
    base_x, base_y = audio.slider_pos
    ancho_slider, alto_slider = audio.slider_size
    espacio = alto_slider + 90
    sliders = []

    for i, tipo_volumen in enumerate(TIPOS_DE_VOLUMEN):
        if tipo_volumen == "MÚSICA":
            valor_inicial = audio.volume
        elif tipo_volumen == "EFECTOS":
            valor_inicial = audio.volume_effects
        else:
            valor_inicial = 1.0

        slider = SliderRect(
            rect_fondo_gris.left + base_x,
            rect_fondo_gris.top + base_y + i * espacio,
            ancho_slider,
            alto_slider,
            initial=valor_inicial,
            tipo_volumen=tipo_volumen
        )
        sliders.append(slider)
    return sliders


def dibujar_ui(screen, bg_anim, fondo_gris, rect_fondo_gris, boton_atras, rect_atras, sliders):
    bg_anim.update()
    bg_anim.draw(screen)
    screen.blit(fondo_gris, rect_fondo_gris)

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
    for slider in sliders:
        slider.draw(screen)

        porcentaje = round(slider.value * 100)
        etiqueta_surf = font.render(f"{slider.tipo_volumen}: ", True, BLANCO)
        etiqueta_x = slider.rect.left - etiqueta_surf.get_width() - 10
        etiqueta_y = slider.rect.y + (slider.rect.height // 2 - etiqueta_surf.get_height() // 2)
        screen.blit(etiqueta_surf, (etiqueta_x, etiqueta_y))

        valor_surf = font.render(f"{porcentaje}%", True, BLANCO)
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
        if slider.tipo_volumen == "MÚSICA":
            pygame.mixer.music.set_volume(slider.value)
        elif slider.tipo_volumen == "EFECTOS":
            audio.volume_effects = slider.value
            for efecto in audio.efectos.values():
                efecto.set_volume(slider.value)


def guardar_volumenes(sliders):
    for slider in sliders:
        if slider.tipo_volumen == "MÚSICA":
            audio.volume = slider.value
        elif slider.tipo_volumen == "EFECTOS":
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
