import pygame
import sys
import Config
from Config import personajes

# Este módulo centraliza la limpieza del estado del juego para un reinicio completo
def reiniciar_estado():
    print("[ESTADO] Reiniciando estado de la partida...")

    # Señal para detener la partida actual (evitando importación circular)
    try:
        import importlib
        Bomberman = importlib.import_module("Bomberman")
        if hasattr(Bomberman, 'salir_de_la_partida'):
            Bomberman.salir_de_la_partida = True
            print("[ESTADO] Señal enviada a Bomberman para cerrar el bucle de juego")
        if hasattr(Bomberman, 'partida_en_curso'):
            Bomberman.partida_en_curso = False
            print("[ESTADO] Bandera de partida en curso reiniciada")
    except Exception as e:
        print(f"[ESTADO] Error al importar Bomberman dinámicamente: {e}")

    print("[ESTADO] Todos los datos han sido reseteados.")
