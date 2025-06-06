import pygame


class Config:
    def __init__(self):
        # Valores por defecto
        self.current_set_index = 2  # Índice para set_options (1,3,5) → inicialmente 3 sets
        self.current_minute = 3  # Número de minutos
        self.current_level_index = 1  # Nivel COM: 0:"Fácil", 1:"Intermedio", 2:"Avanzado"
        self.current_position_index = 0  # Posición inicial: 0:"Fija", 1:"Aleatoria"
        self.current_ultimas_index = {
            "aviones": 0,  # 0:"Sí", 1:"No"
            "Maldiciones": 0,
            "Bloques_final": 0
        }
        # Opciones fijas
        self.set_options = [1, 2, 3, 4, 5]
        self.level_options = ["Fácil", "Intermedio", "Avanzado"]
        self.position_options = ["Fija", "Aleatoria"]
        self.ultimas_opciones = ["Sí", "No"]

        # Configuración mapa
        self.selected_map = 1

config = Config()


class Audio:
    def __init__(self):
        # Volumen música de fondo
        self.volume = 1.0
        # Volumen efectos de sonido
        self.volume_effects = 1.0

        # Parámetros de los sliders (posición y tamaño, igual que antes)
        self.slider_pos = (300, 120)
        self.slider_size = (300, 10)
        # Ahora sólo hay dos valores: [volume (música), volume_effects]
        self.slider_values = [1.0, 1.0]

    def save(self):
        self.slider_values = [
            self.volume,
            self.volume_effects
        ]

    def load(self):
        if len(self.slider_values) >= 2:
            self.volume = self.slider_values[0]
            self.volume_effects = self.slider_values[1]
        else:
            # Si por alguna razón slider_values no está inicializada correctamente,
            # reasignamos valores por defecto.
            self.volume = 1.0
            self.volume_effects = 1.0

audio = Audio()
audio.load()  # Cargar valores iniciales


# clase para guardar seleccion de personajes para cada uno de los jugadores

class Personajes:
    def __init__(self):
        self.seleccion = {
            "jugador_1": {"personaje": None},
            "jugador_2": {"personaje": None},
            "jugador_3": {"personaje": None},
            "jugador_4": {"personaje": None},
        }

    def set_personaje(self, jugador_id, personaje_nombre):
        if jugador_id in self.seleccion:
            self.seleccion[jugador_id]["personaje"] = personaje_nombre

    def get_personaje(self, jugador_id):
        return self.seleccion.get(jugador_id, {}).get("personaje")

    def reset(self):
        for jugador in self.seleccion:
            self.seleccion[jugador]["personaje"] = None

# Instancia global de los personajes
personajes = Personajes()


# CONFIGURACIÓN COMPLETA
from ConfiguraciónMandos import gestor_jugadores

def get_configuracion_completa():
    return {
        "sets": config.set_options[config.current_set_index],
        "tiempo": config.current_minute * 60,  # en segons
        "nivel": config.level_options[config.current_level_index],
        "posicion_inicial": config.position_options[config.current_position_index],
        "ultimas_opciones": config.current_ultimas_index,
        "mapa": config.selected_map,
        "jugadores": gestor_jugadores.todos(),
        "personajes": personajes.seleccion,
        "volumen_musica": audio.volume,
        "volumen_efectos": audio.volume_effects
    }



