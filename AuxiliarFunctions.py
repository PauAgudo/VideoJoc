import pygame
import os
import random

# ─────────────────────────────────────────────────────
# Variables globals del joc
# ─────────────────────────────────────────────────────
TOTAL_TIME = 180
start_time = None

grid = None
game_grid = None
powerups = []
players = []
bombs = []
explosions = []
dropped_abilities = []
exploding_blocks = {}

# Carregador d’imatges amb escala
def load_image(file, size, folder):
    path = os.path.join(folder, file)
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)

# Verifica si una cel·la és lliure (sense obstacle, bomba o maledicció)
def cell_free(tile, grid, bombs, powerups, tx, ty, self_bomb=None, curse_types=None):
    if grid[ty][tx] in (1, 2, 3):
        return False
    for bomb in bombs:
        if bomb is not self_bomb and not bomb.exploded:
            if bomb.tile_x == tx and bomb.tile_y == ty:
                return False
    if curse_types:
        for p in powerups:
            if p.x == tx and p.y == ty and p.visible and p.type in curse_types:
                return False
    return True

# Reapareix totes les habilitats (excepte calavera) amb animació de spawn
def respawn_all_abilities_with_animation(powerups, grid, PowerUp):
    powerups[:] = [p for p in powerups if p.type == "calavera"]
    free_tiles = [(x, y) for y, row in enumerate(grid) for x, val in enumerate(row) if val == 0]
    random.shuffle(free_tiles)
    for ability_type in ["speed", "bomb", "range", "push", "hit"]:
        if not free_tiles:
            break
        tx, ty = free_tiles.pop()
        new_pu = PowerUp(tx, ty, ability_type)
        powerups.append(new_pu)
        new_pu.start_spawn_animation()

# Carrega les imatges del temporitzador (digits, separador, marc)
def load_timer_images(load_image_func, ASSETS_DIR):
    DIGIT_SIZE = (40, 60)
    SEPARADOR_SIZE = (20, 60)
    MARCO_SIZE = (200, 80)
    contador_dir = os.path.join(ASSETS_DIR, "Contador")
    timer_digits = {str(i): load_image_func(f"{i}.png", DIGIT_SIZE, folder=contador_dir) for i in range(10)}
    timer_separador = load_image_func("separador.png", SEPARADOR_SIZE, folder=contador_dir)
    timer_marco = load_image_func("marco_contador.png", MARCO_SIZE, folder=contador_dir)
    return timer_digits, timer_separador, timer_marco, DIGIT_SIZE, SEPARADOR_SIZE, MARCO_SIZE