import pygame
import sys
from PantallaPrincipal import background_screen
from PantallaMapas import pantalla_mapas
from PantallaAudio import pantalla_audio
from Config import config

class ConfiguracionPartida:
    def run(self, screen, bg_anim):
        clock = pygame.time.Clock()
        pygame.display.set_caption("Configuración de Partida")

        # Valores iniciales desde config
        current_set_index = config.current_set_index
        current_minute = config.current_minute
        current_level_index = config.current_level_index
        current_position_index = config.current_position_index
        current_ultimas_index = current_ultimas_index = config.current_ultimas_index.copy()

        # Fondo
        fondo = pygame.transform.scale(pygame.image.load("imagenes/fondobasico.png"), (750, 450))
        fondo_rect = fondo.get_rect(midright=(screen.get_width(), screen.get_height() // 2))

        # Botones fijos
        atras = pygame.transform.scale(pygame.image.load("imagenes/atras.png"), (40, 40))
        atras_rect = atras.get_rect(topleft=(25, 25))
        siguiente = pygame.transform.scale(pygame.image.load("imagenes/siguiente.png"), (40, 40))
        siguiente_rect = siguiente.get_rect(bottomright=(screen.get_width() - 25, screen.get_height() - 25))
        audio = pygame.transform.scale(pygame.image.load("imagenes/settings.png"), (50, 40))
        audio_rect = audio.get_rect(bottomright=(70, screen.get_height() - 30))

        # Tiras

        # Definición de las claves y sus respectivas imágenes
        keys = ["sets", "minutos", "nivel_COM", "pos_inicial", "aviones", "Maldiciones", "Bloques_final"]

        tira_files = {
            "sets": "imagenes/tira_sets.png",
            "minutos": "imagenes/tiempo.png",
            "nivel_COM": "imagenes/tira_COM.png",
            "pos_inicial": "imagenes/tira_posicion.png",
            "aviones": "imagenes/tira_aviones.png",
            "Maldiciones": "imagenes/tira_maldiciones.png",
            "Bloques_final": "imagenes/tira_bloques.png"
        }

        # Carga cada imagen individual y la guarda en el diccionario tiras
        tiras = {
            k: pygame.transform.scale(pygame.image.load(tira_files[k]), (550, 30))
            for k in keys
        }

        # Desplazamiento vertical
        vertical_shift = 50
        posiciones = {
            "sets": (280, 120 + vertical_shift),
            "minutos": (280, 160 + vertical_shift),
            "nivel_COM": (280, 200 + vertical_shift),
            "pos_inicial": (280, 240 + vertical_shift),
            "aviones": (280, 280 + vertical_shift),
            "Maldiciones": (280, 320 + vertical_shift),
            "Bloques_final": (280, 360 + vertical_shift)
        }
        botones = {k: {"imagen": tiras[k], "rect": tiras[k].get_rect(topleft=posiciones[k])} for k in keys}

        # Flechas
        izquierda = pygame.transform.scale(pygame.image.load("imagenes/izquierda.png"), (30, 30))
        derecha = pygame.transform.scale(pygame.image.load("imagenes/derecha.png"), (30, 30))
        flechas_pos = {k: {"izquierda": (520, posiciones[k][1]), "derecha": (680, posiciones[k][1])} for k in keys}

        font = pygame.font.SysFont(None, 23)
        shift_amount = 10

        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if atras_rect.collidepoint(mouse_pos):
                        config.__init__()
                        background_screen(screen)

                    if siguiente_rect.collidepoint(mouse_pos):
                        config.current_set_index = current_set_index
                        config.current_minute = current_minute
                        config.current_level_index = current_level_index
                        config.current_position_index = current_position_index
                        config.current_ultimas_index = current_ultimas_index.copy()
                        pantalla_mapas(screen, bg_anim)

                    if audio_rect.collidepoint(mouse_pos):
                        pantalla_audio(screen, bg_anim)

                    for key, btn in botones.items():
                        if btn["rect"].collidepoint(mouse_pos):
                            la = izquierda.get_rect(topleft=flechas_pos[key]["izquierda"])
                            ra = derecha.get_rect(topleft=flechas_pos[key]["derecha"])
                            if la.collidepoint(mouse_pos):
                                if key == "sets" and current_set_index > 0:
                                    current_set_index -= 1
                                elif key == "minutos" and current_minute > 1:
                                    current_minute -= 1
                                elif key == "nivel_COM" and current_level_index > 0:
                                    current_level_index -= 1
                                elif key == "pos_inicial" and current_position_index > 0:
                                    current_position_index -= 1
                                elif key in current_ultimas_index and current_ultimas_index[key] > 0:
                                    current_ultimas_index[key] -= 1
                            elif ra.collidepoint(mouse_pos):
                                if key == "sets" and current_set_index < len(config.set_options) - 1:
                                    current_set_index += 1
                                elif key == "minutos" and current_minute < 9:
                                    current_minute += 1
                                elif key == "nivel_COM" and current_level_index < len(config.level_options) - 1:
                                    current_level_index += 1
                                elif key == "pos_inicial" and current_position_index < len(config.position_options) - 1:
                                    current_position_index += 1
                                elif key in current_ultimas_index and current_ultimas_index[key] < len(config.ultimas_opciones) - 1:
                                    current_ultimas_index[key] += 1

            # Dibujar
            bg_anim.update()
            bg_anim.draw(screen)
            screen.blit(fondo, fondo_rect)

            for key, btn in botones.items():
                rect = btn["rect"]
                hov = rect.collidepoint(mouse_pos)
                img = btn["imagen"]
                if hov:
                    hi = pygame.transform.scale(img, (int(rect.width * 1.1), rect.height))
                    hr = hi.get_rect(center=rect.center)
                    hr.x -= shift_amount
                    screen.blit(hi, hr)
                    cur_rect = hr
                else:
                    screen.blit(img, rect)
                    cur_rect = rect

                # Mostrar valor actual
                if key == "sets":
                    v = config.set_options[current_set_index]
                    screen.blit(pygame.transform.scale(pygame.image.load(f"imagenes/{v}.png"), (30, 30)),
                                (600 - (shift_amount if hov else 0), posiciones[key][1]))
                if key == "minutos":
                    screen.blit(pygame.transform.scale(pygame.image.load(f"imagenes/{current_minute}.png"), (30, 30)),
                                (600 - (shift_amount if hov else 0), posiciones[key][1]))
                if key == "nivel_COM":
                    txt = config.level_options[current_level_index]
                    surf = font.render(txt, True, (255, 255, 255))
                    lx = flechas_pos[key]["izquierda"][0] - (shift_amount if hov else 0)
                    rx = flechas_pos[key]["derecha"][0] - (shift_amount if hov else 0)
                    cx = (lx + 30 + rx) // 2
                    cy = cur_rect.centery
                    screen.blit(surf, (cx - surf.get_width() // 2, cy - surf.get_height() // 2))
                if key == "pos_inicial":
                    txt = config.position_options[current_position_index]
                    surf = font.render(txt, True, (255, 255, 255))
                    lx = flechas_pos[key]["izquierda"][0] - (shift_amount if hov else 0)
                    rx = flechas_pos[key]["derecha"][0] - (shift_amount if hov else 0)
                    cx = (lx + 30 + rx) // 2
                    cy = cur_rect.centery
                    screen.blit(surf, (cx - surf.get_width() // 2, cy - surf.get_height() // 2))
                if key in ["aviones", "Maldiciones", "Bloques_final"]:
                    txt = config.ultimas_opciones[current_ultimas_index[key]]
                    surf = font.render(txt, True, (255, 255, 255))
                    lx = flechas_pos[key]["izquierda"][0] - (shift_amount if hov else 0)
                    rx = flechas_pos[key]["derecha"][0] - (shift_amount if hov else 0)
                    cx = (lx + 30 + rx) // 2
                    cy = cur_rect.centery
                    screen.blit(surf, (cx - surf.get_width() // 2, cy - surf.get_height() // 2))

                if hov:
                    left_pos = (flechas_pos[key]["izquierda"][0] - shift_amount, flechas_pos[key]["izquierda"][1])
                    right_pos = (flechas_pos[key]["derecha"][0] - shift_amount, flechas_pos[key]["derecha"][1])
                    left_rect = izquierda.get_rect(topleft=left_pos)
                    right_rect = derecha.get_rect(topleft=right_pos)
                    if left_rect.collidepoint(mouse_pos):
                        iz_hover = pygame.transform.scale(izquierda, (int(left_rect.width * 1.1), int(left_rect.height * 1.1)))
                        iz_rect_h = iz_hover.get_rect(center=left_rect.center)
                        screen.blit(iz_hover, iz_rect_h)
                    else:
                        screen.blit(izquierda, left_rect)
                    if right_rect.collidepoint(mouse_pos):
                        dr_hover = pygame.transform.scale(derecha, (int(right_rect.width * 1.1), int(right_rect.height * 1.1)))
                        dr_rect_h = dr_hover.get_rect(center=right_rect.center)
                        screen.blit(dr_hover, dr_rect_h)
                    else:
                        screen.blit(derecha, right_rect)

            # Botones fijos
            for img, rc in [(atras, atras_rect), (siguiente, siguiente_rect), (audio, audio_rect)]:
                if rc.collidepoint(mouse_pos):
                    screen.blit(pygame.transform.scale(img, (int(rc.width * 1.1), int(rc.height * 1.1))), rc)
                else:
                    screen.blit(img, rc)

            # Título
            font2 = pygame.font.Font(None, 36)
            title_surf = font2.render("CONFIGURACIÓN DE PARTIDA", True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(537, 105))
            screen.blit(title_surf, title_rect)

            pygame.display.flip()
            clock.tick(60)

def pantalla2_main(screen, bg_anim):
    ConfiguracionPartida().run(screen, bg_anim)
