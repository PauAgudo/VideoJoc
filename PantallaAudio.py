import pygame
import sys

class SliderRect:
    def __init__(self, x, y, width, height, initial=1.0):  # inicial en el extremo derecho
        # Rectángulo del control deslizante
        self.rect = pygame.Rect(x, y, width, height)
        # Valor de la tira: 0.0 (izquierda) a 1.0 (derecha)
        self.value = initial
        # Tamaño de la manecilla
        self.handle_size = 15

    def draw(self, screen):
        x, y, w, h = self.rect
        # Centro de la manecilla recorre el ancho w
        center_x = x + int(self.value * w)
        # Cálculo de la posición izquierda de la manecilla para centrarla sobre center_x
        handle_left = center_x - self.handle_size // 2
        # Ancho de la porción azul (desde el borde izquierdo hasta center_x)
        blue_width = center_x - x
        # Ancho de la porción blanca (desde center_x hasta el borde derecho)
        white_width = w - blue_width

        # Dibujar parte azul
        if blue_width > 0:
            blue_rect = pygame.Rect(x, y, blue_width, h)
            pygame.draw.rect(screen, (0, 0, 255), blue_rect)
        # Dibujar parte blanca
        if white_width > 0:
            white_rect = pygame.Rect(center_x, y, white_width, h)
            pygame.draw.rect(screen, (255, 255, 255), white_rect)

        # Dibujar borde del control
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)

        # Dibujar manecilla roja
        handle_rect = pygame.Rect(handle_left, y + (h - self.handle_size)//2,
                                  self.handle_size, self.handle_size)
        pygame.draw.rect(screen, (255, 0, 0), handle_rect)

    def update(self, mouse_pos, mouse_click):
        # Si se hace clic dentro del área del control
        if mouse_click and self.rect.collidepoint(mouse_pos):
            # Posición relativa del ratón sobre la tira
            rel_x = mouse_pos[0] - self.rect.left
            # Calcular valor normalizado entre 0 y 1
            self.value = max(0.0, min(1.0, rel_x / self.rect.width))


def pantalla_audio(screen, bg_anim):
    pygame.display.set_caption("Pantalla Audio")
    clock = pygame.time.Clock()

    # Botón ATRÁS
    atras = pygame.image.load("imagenes/atras.png").convert_alpha()
    atras = pygame.transform.scale(atras, (40, 40))
    atras_rect = atras.get_rect(topleft=(30, 30))

    # Fondo gris de la sección de audio
    gris = pygame.image.load("imagenes/gris.png").convert_alpha()
    gris = pygame.transform.scale(gris, (600, 400))
    gris_rect = gris.get_rect(center=(screen.get_width()//2, screen.get_height()//2))

    # Crear tres sliders dentro del recuadro gris
    sliders = []
    x_start = gris_rect.left + 200
    y_start = gris_rect.top + 90
    slider_w, slider_h = 300, 10
    gap = slider_h + 90
    # Todos inicializados a 1.0 (solo azul visible)
    for i in range(3):
        s = SliderRect(x_start, y_start + i * gap, slider_w, slider_h, initial=1.0)
        sliders.append(s)

    pygame.mixer.music.set_volume( sliders[0].value )   # volumen inicial

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if atras_rect.collidepoint(mouse_pos):
                    # Volver a la pantalla de configuración
                    from PantallaConfigPartida import pantalla2
                    pantalla2(screen, bg_anim)
                    return

        # Actualizar cada slider según interacción del ratón
        for slider in sliders:
            slider.update(mouse_pos, mouse_click)

        # Dibujar animación de fondo
        bg_anim.update()
        bg_anim.draw(screen)

        # Dibujar botón ATRÁS con efecto hover
        if atras_rect.collidepoint(mouse_pos):
            atras_h = pygame.transform.scale(atras, (55, 55))
            rect_h = atras_h.get_rect(center=atras_rect.center)
            screen.blit(atras_h, rect_h)
        else:
            screen.blit(atras, atras_rect)

        # Dibujar el recuadro gris
        screen.blit(gris, gris_rect)

        # AJUSTE TIEMPO REAL VOLUMEN MUSICA DE FONDO
        sliders[0].update(mouse_pos, mouse_click)
        pygame.mixer.music.set_volume(sliders[0].value)

        # Dibujar los sliders sobre el gris
        for slider in sliders:
            slider.draw(screen)

        pygame.display.flip()
        clock.tick(60)
