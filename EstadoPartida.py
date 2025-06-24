import pygame
import sys
# Importamos directamente las instancias globales de Config.py y ConfiguraciónMandos.py
from Config import config, personajes, audio
from ConfiguraciónMandos import gestor_jugadores
from PantallaPersonajes import reiniciar_estado_personajes

# Este módulo centraliza la limpieza del estado del juego para un reinicio completo
def reiniciar_estado():
    print("[ESTADO] Reiniciando estado de la partida...")

    # 1. Resetear las configuraciones de la partida a valores por defecto
    """ AHORA MISMO ESTA COMENTADO, DE MODO QUE CUANDO SALES DE LA PARTIDA SE QUEDA LA CONFIGURACION
    DE LA ULTIMA PARTIDA JUGADA"""
    #config.reset()
    #print("[ESTADO] Configuración de partida reseteada.")

    # 2. Resetear la selección de personajes
    personajes.reset()
    print("[ESTADO] Selección de personajes reseteada.")

    # 3. Resetear el gestor de jugadores (mandos/teclado)
    gestor_jugadores.reset()
    print("[ESTADO] Gestor de jugadores reseteado.")

    # Resetear jugadores/dispositivos connectados
    reiniciar_estado_personajes()


    # 4. Detener la música del juego si está sonando y reproducir la música del menú
    pygame.mixer.music.stop()
    try:
        pygame.mixer.music.load("Media/Sonidos_juego/musica_fondo/menu.mp3")
        pygame.mixer.music.set_volume(audio.volume) # Usa el volumen global
        pygame.mixer.music.play(-1)
        print("[ESTADO] Música del menú iniciada.")
    except Exception as e:
        print(f"[ESTADO] Error al cargar o reproducir música del menú: {e}")

    print("[ESTADO] Todos los datos han sido reseteados.")
    # No necesitamos devolver nada aquí, solo realiza el reinicio de datos.