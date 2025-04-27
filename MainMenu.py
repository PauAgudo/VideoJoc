import pygame
import sys
from PantallaPrincipal import background_screen
from PantallaPrincipal import BackgroundAnimation
from PantallaConfigPartida import pantalla2_main, ConfiguracionPartida
from PantallaMapas import pantalla_mapas
from PantallaAudio import pantalla_audio



def main():
    pygame.init()

    # Inicializar el mixer y reproducir la banda sonora de fondo
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    pygame.mixer.music.load("media/retrogame.mp3")  # Asegúrate de que la ruta y el nombre sean correctos
    pygame.mixer.music.set_volume(1.0)  # volumen al 100%
    pygame.mixer.music.play(-1)  # -1 para reproducir en bucle indefinido

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Mi Juego")

    # Cargar o crear elementos compartidos
    bg_anim = BackgroundAnimation(screen_width, screen_height)  # Asumiendo que está en un módulo común

    # Mostrar la pantalla principal y luego la pantalla 2
    background_screen(screen)
    pantalla2_main(screen, bg_anim)
    pantalla_mapas(screen, bg_anim)
    pantalla_audio(screen, bg_anim)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()