import pygame
import os
from AuxiliarFunctions import load_image

# Inicialització de mixer (es pot fer abans al main també)
pygame.mixer.init()

# Constants bàsiques
TILE_SIZE = 40
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
MUSIC_PATH = os.path.join(ASSETS_DIR, "Banda Sonora", "banda_sonora_juego.mp3")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Contenidors globals (es carregaran després)
SUELO1 = SUELO2 = STONE = BRICK = LIMIT_IMG = None
SPEED_IMG = MORE_BOMB_IMG = MAYOR_EXPLOSION_IMG = CALAVERA_IMG = PUSH_BOMB_IMG = PUÑO_IMG = None
BOMB_IMAGES = CENTER_EXPLOSION_FRAMES = EXTREME_EXPLOSION_FRAMES = LATERAL_EXPLOSION_FRAMES = []
EXPLOSION_FRAMES = ABILITY_EXPLOSION_FRAMES = []
POWERUP_DESTROY_FRAMES = []
EXPLOSION_SOUND = FOOTSTEP_SOUND = COLOCAR_BOMBA_SOUND = COGER_HABILIDAD_SOUND = COGER_MALDICION_SOUND = None
timer_digits = {}
timer_separador = timer_marco = None
DIGIT_SIZE = (40, 60)
SEPARADOR_SIZE = (20, 60)
MARCO_SIZE = (200, 80)
RED_RIGHT_IMAGES = RED_LEFT_IMAGES = RED_UP_IMAGES = RED_DOWN_IMAGES = []
BLUE_RIGHT_IMAGES = BLUE_LEFT_IMAGES = BLUE_UP_IMAGES = BLUE_DOWN_IMAGES = []

def carregar_assets():
    global SUELO1, SUELO2, STONE, BRICK, LIMIT_IMG
    global SPEED_IMG, MORE_BOMB_IMG, MAYOR_EXPLOSION_IMG, CALAVERA_IMG, PUSH_BOMB_IMG, PUÑO_IMG
    global BOMB_IMAGES, CENTER_EXPLOSION_FRAMES, EXTREME_EXPLOSION_FRAMES, LATERAL_EXPLOSION_FRAMES
    global EXPLOSION_FRAMES, ABILITY_EXPLOSION_FRAMES, POWERUP_DESTROY_FRAMES
    global EXPLOSION_SOUND, FOOTSTEP_SOUND, COLOCAR_BOMBA_SOUND, COGER_HABILIDAD_SOUND, COGER_MALDICION_SOUND
    global timer_digits, timer_separador, timer_marco
    global RED_RIGHT_IMAGES, RED_LEFT_IMAGES, RED_UP_IMAGES, RED_DOWN_IMAGES
    global BLUE_RIGHT_IMAGES, BLUE_LEFT_IMAGES, BLUE_UP_IMAGES, BLUE_DOWN_IMAGES

    # Mapes
    SUELO1 = load_image("suelo1.png", (TILE_SIZE, TILE_SIZE), folder=os.path.join(ASSETS_DIR, "Mapas", "Mapa 1"))
    SUELO2 = load_image("suelo2.png", (TILE_SIZE, TILE_SIZE), folder=os.path.join(ASSETS_DIR, "Mapas", "Mapa 1"))
    STONE = load_image("stone.png", (TILE_SIZE, TILE_SIZE))
    BRICK = load_image("brick.png", (TILE_SIZE, TILE_SIZE))
    LIMIT_IMG = load_image("limit.png", (TILE_SIZE, TILE_SIZE))

    # Habilitats
    HABILIDADES_DIR = os.path.join(ASSETS_DIR, "Habilidades")
    SPEED_IMG = load_image("speed.png", (40, 40), folder=HABILIDADES_DIR)
    MORE_BOMB_IMG = load_image("more_bomb.png", (40, 40), folder=HABILIDADES_DIR)
    MAYOR_EXPLOSION_IMG = load_image("mayor_explosion.png", (40, 40), folder=HABILIDADES_DIR)
    CALAVERA_IMG = load_image("calavera.png", (40, 40), folder=HABILIDADES_DIR)
    PUSH_BOMB_IMG = load_image("xut.png", (40, 40), folder=os.path.join(ASSETS_DIR, "Poderes"))
    PUÑO_IMG = load_image("puño.png", (40, 40), folder=os.path.join(ASSETS_DIR, "Poderes"))

    # Bombes i explosions
    bomb_folder = os.path.join(ASSETS_DIR, "bombas")
    BOMB_IMAGES.extend([load_image(f"bomb{i}.png", (40, 40), folder=bomb_folder) for i in range(1, 16)])
    CENTER_EXPLOSION_FRAMES.extend([load_image(f"bomba_c{i}.png", (40, 40), folder=bomb_folder) for i in range(1, 18)])
    EXTREME_EXPLOSION_FRAMES.extend([load_image(f"ex_e{i}.png", (40, 40), folder=bomb_folder) for i in range(1, 18)])
    LATERAL_EXPLOSION_FRAMES.extend([load_image(f"ex_l{i}.png", (40, 40), folder=bomb_folder) for i in range(1, 18)])
    EXPLOSION_FRAMES.extend([load_image(f"explosion_{i}.png", (40, 40)) for i in range(3)])
    ABILITY_EXPLOSION_FRAMES.extend([
        load_image(f"habilidad_ex{i}.png", (40, 40), folder=os.path.join(HABILIDADES_DIR, "explosion"))
        for i in range(1, 18)
    ])

    POWERUP_DESTROY_FRAMES.extend([pygame.Surface((40, 40)), pygame.Surface((40, 40))])
    POWERUP_DESTROY_FRAMES[0].fill((255, 200, 0))
    POWERUP_DESTROY_FRAMES[1].fill((255, 100, 0))

    # Sons
    EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "Banda Sonora", "Bombs", "bomb.wav"))
    EXPLOSION_SOUND.set_volume(0.35)
    FOOTSTEP_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "Banda Sonora", "movimiento", "pasos.wav"))
    FOOTSTEP_SOUND.set_volume(1.0)
    COLOCAR_BOMBA_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "Banda Sonora", "Bombs", "colocar_bomba.wav"))
    COLOCAR_BOMBA_SOUND.set_volume(0.35)
    COGER_HABILIDAD_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "Banda Sonora", "habilidades", "coger_habilidad.wav"))
    COGER_HABILIDAD_SOUND.set_volume(0.35)
    COGER_MALDICION_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "Banda Sonora", "habilidades", "coger_maldicion.mp3"))
    COGER_MALDICION_SOUND.set_volume(0.35)

    # Timer visuals
    CONTADOR_DIR = os.path.join(ASSETS_DIR, "Contador")
    timer_digits.update({str(i): load_image(f"{i}.png", (40, 60), folder=CONTADOR_DIR) for i in range(10)})
    timer_separador = load_image("separador.png", (20, 60), folder=CONTADOR_DIR)
    timer_marco = load_image("marco_contador.png", (200, 80), folder=CONTADOR_DIR)

    # Jugadors (red)
    red_dirs = ["right", "left", "up", "down"]
    red_lists = [RED_RIGHT_IMAGES, RED_LEFT_IMAGES, RED_UP_IMAGES, RED_DOWN_IMAGES]
    for direction, image_list in zip(red_dirs, red_lists):
        folder = os.path.join(ASSETS_DIR, "Player1", "red", direction)
        image_list.extend([load_image(f"{direction}{i}.png", (120, 120), folder=folder) for i in range(1, 10)])

    # Jugadors (blue)
    blue_dirs = ["right", "left", "up", "down"]
    blue_lists = [BLUE_RIGHT_IMAGES, BLUE_LEFT_IMAGES, BLUE_UP_IMAGES, BLUE_DOWN_IMAGES]
    for direction, image_list in zip(blue_dirs, blue_lists):
        folder = os.path.join(ASSETS_DIR, "Player1", "blue", direction)
        image_list.extend([load_image(f"{direction}{i}.png", (120, 120), folder=folder) for i in range(1, 10)])
