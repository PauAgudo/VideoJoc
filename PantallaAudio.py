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
            pygame.image.load("Media/Menu/Botones/atras.png"),
            (40, 40)
        )
    except pygame.error:
        print("Error al cargar la imagen: atras.png")
        sys.exit(1)
    rect_atras = boton_atras.get_rect(topleft=(25, 25))

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

    return boton_atras, rect_atras, fondo_gris, rect_fondo_gris


def crear_sliders(rect_fondo_gris):
    base_x, base_y = audio.slider_pos
    ancho_slider, alto_slider = audio.slider_size
    # Ajustamos el espacio vertical para sólo dos sliders
    espacio = alto_slider + 90
    sliders = []

    for i, tipo_volumen in enumerate(TIPOS_DE_VOLUMEN):
        # Obtiene los valores iniciales para cada tipo de volumen desde Config
        if tipo_volumen == "MÚSICA":
            valor_inicial = audio.volume
        elif tipo_volumen == "EFECTOS":
            valor_inicial = audio.volume_effects
        else:
            valor_inicial = 1.0  # Por defecto, máximo

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

    # Dibuja el botón "Atrás" con efecto hover
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

    # Dibuja los sliders, sus etiquetas y valores porcentuales
    font = pygame.font.SysFont(None, 16)
    for slider in sliders:
        slider.draw(screen)

        porcentaje = round(slider.value * 100)

        # Etiqueta a la izquierda
        etiqueta_surf = font.render(f"{slider.tipo_volumen}: ", True, BLANCO)
        etiqueta_x = slider.rect.left - etiqueta_surf.get_width() - 10
        etiqueta_y = slider.rect.y + (slider.rect.height // 2 - etiqueta_surf.get_height() // 2)
        screen.blit(etiqueta_surf, (etiqueta_x, etiqueta_y))

        # Valor porcentual a la derecha
        valor_surf = font.render(f"{porcentaje}%", True, BLANCO)
        valor_x = slider.rect.right + 10
        valor_y = slider.rect.y + (slider.rect.height // 2 - valor_surf.get_height() // 2)
        screen.blit(valor_surf, (valor_x, valor_y))


def manejar_eventos(sliders, rect_atras, screen, bg_anim):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and rect_atras.collidepoint(mouse_pos):
            # Guarda los valores de volumen en Config
            for slider in sliders:
                if slider.tipo_volumen == "MÚSICA":
                    audio.volume = slider.value
                elif slider.tipo_volumen == "EFECTOS":
                    audio.volume_effects = slider.value

            audio.save()
            from PantallaConfigPartida import pantalla2_main
            pantalla2_main(screen, bg_anim)
            return "ATRAS"

    # Actualiza cada slider según el mouse
    for slider in sliders:
        slider.update(mouse_pos, mouse_click)

    # Aplica los ajustes de volumen en tiempo real
    for slider in sliders:
        if slider.tipo_volumen == "MÚSICA":
            pygame.mixer.music.set_volume(slider.value)
        elif slider.tipo_volumen == "EFECTOS":
            audio.volume_effects = slider.value


def pantalla_audio(screen, bg_anim):
    pygame.display.set_caption("Pantalla Audio")
    clock = pygame.time.Clock()

    boton_atras, rect_atras, fondo_gris, rect_fondo_gris = inicializar_componentes_ui(screen)
    sliders = crear_sliders(rect_fondo_gris)

    while True:
        resultado = manejar_eventos(sliders, rect_atras, screen, bg_anim)
        if resultado == "ATRAS":
            return

        dibujar_ui(screen, bg_anim, fondo_gris, rect_fondo_gris, boton_atras, rect_atras, sliders)
        pygame.display.flip()
        clock.tick(60)
