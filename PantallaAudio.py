import pygame
import sys
from Config import audio

class SliderRect:
    def __init__(self, x, y, width, height, initial=1.0):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = initial
        self.handle_size = 15

    def draw(self, screen):
        x, y, w, h = self.rect
        center_x = x + int(self.value * w)
        blue_width = center_x - x
        white_width = w - blue_width
        if blue_width > 0:
            pygame.draw.rect(screen, (0, 0, 255), (x, y, blue_width, h))
        if white_width > 0:
            pygame.draw.rect(screen, (255, 255, 255), (center_x, y, white_width, h))
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        handle_left = center_x - self.handle_size // 2
        pygame.draw.rect(screen, (255, 0, 0), (handle_left, y + (h - self.handle_size) // 2, self.handle_size, self.handle_size))

    def update(self, mouse_pos, mouse_click):
        if mouse_click and self.rect.collidepoint(mouse_pos):
            rel_x = mouse_pos[0] - self.rect.left
            self.value = max(0.0, min(1.0, rel_x / self.rect.width))


def pantalla_audio(screen, bg_anim):
    pygame.display.set_caption("Pantalla Audio")
    clock = pygame.time.Clock()

    # Botón ATRÁS
    atras = pygame.transform.scale(pygame.image.load("imagenes/atras.png"), (40, 40))
    atras_rect = atras.get_rect(topleft=(30, 30))

    # Fondo gris
    gris = pygame.transform.scale(pygame.image.load("imagenes/gris.png"), (600, 400))
    gris_rect = gris.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    # Configuración global de sliders
    base_x, base_y = audio.slider_pos
    slider_w, slider_h = audio.slider_size
    gap = slider_h + 90

    # Crear sliders usando valores globales
    sliders = []
    for i in range(3):
        init = audio.slider_values[i] if i < len(audio.slider_values) else 1.0
        s = SliderRect(gris_rect.left + base_x,
                       gris_rect.top + base_y + i * gap,
                       slider_w, slider_h,
                       initial=init)
        sliders.append(s)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and atras_rect.collidepoint(mouse_pos):
                # Guardar valores globales de sliders
                audio.slider_values = [s.value for s in sliders]
                audio.volume = sliders[0].value
                from PantallaConfigPartida import pantalla2_main
                pantalla2_main(screen, bg_anim)
                return

        # Actualizar todos los sliders
        for s in sliders:
            s.update(mouse_pos, mouse_click)

        # Aplicar volumen en tiempo real
        pygame.mixer.music.set_volume(sliders[0].value)

        # Dibujar fondo y controles
        bg_anim.update()
        bg_anim.draw(screen)
        screen.blit(gris, gris_rect)
        if atras_rect.collidepoint(mouse_pos):
            screen.blit(pygame.transform.scale(atras, (55, 55)), atras_rect)
        else:
            screen.blit(atras, atras_rect)

        # Dibujar sliders
        for s in sliders:
            s.draw(screen)

        pygame.display.flip()
        clock.tick(60)
