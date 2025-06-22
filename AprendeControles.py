import pygame
import sys

def pantalla_controles(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    font_casilla = pygame.font.SysFont(None, 30)

    texto = font.render("Aprende los controles", True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 260))

    ancho_recuadro = 750
    alto_recuadro = 450
    rect_azul = pygame.Rect(
        (screen.get_width() - ancho_recuadro) // 2,
        (screen.get_height() - alto_recuadro) // 2,
        ancho_recuadro,
        alto_recuadro
    )

    flecha_original = pygame.image.load("Media/Menu/Botones/siguiente.png").convert_alpha()
    flecha_rotada = pygame.transform.rotate(flecha_original, 180)
    tamaño_base = (40, 40)
    tamaño_hover = (45, 45)
    flecha_img = pygame.transform.scale(flecha_rotada, tamaño_base)
    flecha_rect = flecha_img.get_rect()
    flecha_rect.bottomleft = (25, screen.get_height() - 25)

    img_izq = pygame.image.load("Media/Menu/Pantalla_configuracion_partida/izquierda.png").convert_alpha()
    img_der = pygame.image.load("Media/Menu/Pantalla_configuracion_partida/derecha.png").convert_alpha()
    img_izq_base = pygame.transform.scale(img_izq, tamaño_base)
    img_der_base = pygame.transform.scale(img_der, tamaño_base)
    img_izq_hover = pygame.transform.scale(img_izq, tamaño_hover)
    img_der_hover = pygame.transform.scale(img_der, tamaño_hover)

    rect_izq = img_izq_base.get_rect()
    rect_der = img_der_base.get_rect()

    img_mando = pygame.image.load("Media/Menu/mando.png").convert_alpha()
    img_teclado = pygame.image.load("Media/Menu/teclado.png").convert_alpha()

    textos_vista = ["Controles de mando", "Controles de teclado"]
    vista_actual = 0

    joystick_threshold = 0.5
    joystick_timer = 0
    joystick_cooldown = 200  # milisegundos

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        dt = clock.tick(60)
        joystick_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    vista_actual = (vista_actual - 1) % len(textos_vista)
                elif event.key == pygame.K_RIGHT:
                    vista_actual = (vista_actual + 1) % len(textos_vista)

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 1:
                    running = False

            elif event.type == pygame.JOYHATMOTION:
                if event.value[0] == -1:
                    vista_actual = (vista_actual - 1) % len(textos_vista)
                elif event.value[0] == 1:
                    vista_actual = (vista_actual + 1) % len(textos_vista)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True
                    if flecha_rect.collidepoint(mouse_pos):
                        running = False
                    elif rect_izq.collidepoint(mouse_pos):
                        vista_actual = (vista_actual - 1) % len(textos_vista)
                    elif rect_der.collidepoint(mouse_pos):
                        vista_actual = (vista_actual + 1) % len(textos_vista)

        # Gestión joystick analógico (eje horizontal del joystick izquierdo)
        if pygame.joystick.get_count() > 0:
            joystick = pygame.joystick.Joystick(0)
            axis = joystick.get_axis(0)
            if joystick_timer >= joystick_cooldown:
                if axis <= -joystick_threshold:
                    vista_actual = (vista_actual - 1) % len(textos_vista)
                    joystick_timer = 0
                elif axis >= joystick_threshold:
                    vista_actual = (vista_actual + 1) % len(textos_vista)
                    joystick_timer = 0

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (30, 30, 150), rect_azul, border_radius=20)

        casilla_width = 280
        casilla_height = 40
        casilla_x = rect_azul.centerx - casilla_width // 2
        casilla_y = rect_azul.y + 20
        casilla_rect = pygame.Rect(casilla_x, casilla_y, casilla_width, casilla_height)

        pygame.draw.rect(screen, (100, 120, 150), casilla_rect, border_radius=12)
        pygame.draw.rect(screen, (180, 180, 180), casilla_rect, width=2, border_radius=12)

        rect_izq = (img_izq_hover if rect_izq.collidepoint(mouse_pos) else img_izq_base).get_rect()
        rect_izq.centery = casilla_rect.centery
        rect_izq.right = casilla_rect.left - 5

        rect_der = (img_der_hover if rect_der.collidepoint(mouse_pos) else img_der_base).get_rect()
        rect_der.centery = casilla_rect.centery
        rect_der.left = casilla_rect.right + 5

        if rect_izq.collidepoint(mouse_pos):
            screen.blit(img_izq_hover, rect_izq)
        else:
            screen.blit(img_izq_base, rect_izq)

        if rect_der.collidepoint(mouse_pos):
            screen.blit(img_der_hover, rect_der)
        else:
            screen.blit(img_der_base, rect_der)

        texto_vista = font_casilla.render(textos_vista[vista_actual], True, (255, 255, 255))
        texto_vista_rect = texto_vista.get_rect(center=casilla_rect.center)
        screen.blit(texto_vista, texto_vista_rect)

        screen.blit(texto, texto_rect)

        # TAMAÑO IMAGEN CONTROLES
        if textos_vista[vista_actual] == "Controles de mando":
            imagen = pygame.transform.scale(img_mando, (350, 220))
        elif textos_vista[vista_actual] == "Controles de teclado":
            imagen = pygame.transform.scale(img_teclado, (400, 200))
        else:
            imagen = None

        if imagen:
            imagen_rect = imagen.get_rect(center=rect_azul.center)
            screen.blit(imagen, imagen_rect)

        if flecha_rect.collidepoint(mouse_pos):
            flecha_img = pygame.transform.scale(flecha_rotada, tamaño_hover)
            flecha_rect = flecha_img.get_rect(topleft=flecha_rect.topleft)
        else:
            flecha_img = pygame.transform.scale(flecha_rotada, tamaño_base)
            flecha_rect = flecha_img.get_rect(topleft=flecha_rect.topleft)

        screen.blit(flecha_img, flecha_rect)

        pygame.display.flip()

    return
