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
        # Volumen botones menú
        self.volume_buttons = 1.0
        # Volumen efectos de sonido
        self.volume_effects = 1.0

        # Parámetros de los sliders
        self.slider_pos = (300, 120)
        self.slider_size = (300, 10)
        self.slider_values = [1.0, 1.0, 1.0]

    def save(self):
        """Guarda los valores directamente en la clase."""
        self.slider_values = [self.volume, self.volume_buttons, self.volume_effects]

    def load(self):
        """Carga los valores directamente desde la clase."""
        self.volume = self.slider_values[0]
        self.volume_buttons = self.slider_values[1]
        self.volume_effects = self.slider_values[2]


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

# Instancia global que puedes importar en cualquier parte del juego
personajes = Personajes()



