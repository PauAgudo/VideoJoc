import pygame
import sys

from PantallaPrincipal import background_screen
from PantallaPrincipal import BackgroundAnimation
from PantallaConfigPartida import pantalla2_main
from PantallaMapas import pantalla_mapas
from PantallaAudio import pantalla_audio
from PantallaPersonajes import pantalla_personajes
from AprendeControles import pantalla_controles

def main():
    pygame.init()

    # Inicializar el mixer y reproducir la banda sonora de fondo
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    # CARGAR EFECTOS DE SONIDO
    # musica de fondo
    pygame.mixer.music.load("Media/Sonidos_juego/musica_fondo/menu.mp3")  #
    pygame.mixer.music.set_volume(1.0)  # volumen al 100%
    pygame.mixer.music.play(-1)  # -1 para reproducir en bucle indefinido

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Mi Juego")

    # Cargar o crear elementos compartidos
    bg_anim = BackgroundAnimation(screen_width, screen_height)  # Asumiendo que está en un módulo común

    # Mostrar pantalles només si l’usuari les va confirmant
    if not background_screen(screen):
        return
    if not pantalla2_main(screen, bg_anim):
        return
    if not pantalla_mapas(screen, bg_anim):
        return
    if not pantalla_audio(screen, bg_anim, pygame.mixer):
        return
    if not pantalla_controles(screen, bg_anim):
        return
    if not pantalla_personajes(screen, bg_anim):
        return
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()