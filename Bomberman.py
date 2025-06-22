import pygame
import os
import sys
import math
import random
import time
from Config import config, audio
from ConfiguraciónMandos import gestor_jugadores
from PausaPartida import menu_pausa

# ------------------------------------------------------------------------------------
# Inicialización y configuración de pantalla
# ------------------------------------------------------------------------------------
pygame.init()
pygame.mixer.init()

# Inicialización de mandos
pygame.joystick.init()


def get_joystick_by_instance_id(instance_id: int):
    for i in range(pygame.joystick.get_count()):
        joy = pygame.joystick.Joystick(i)
        if joy.get_instance_id() == instance_id:
            return joy
    return None  # si se ha desconectado


BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "Media")

TOP_OFFSET = 80  # Espacio para el contador y el HUD
TILE_SIZE = 40
GRID_COLS = 21
GRID_ROWS = 17
WIDTH = GRID_COLS * TILE_SIZE  # Ancho total de la pantalla
HEIGHT = GRID_ROWS * TILE_SIZE + TOP_OFFSET

CURSES = {
    "reset": {"duration": None, "shows_in_hud": False, "clears_previous": False,
              "set_effect": lambda p, c: p._do_reset(),
              "clear_effect": lambda p, c: None},
    "no_ability": {"duration": 40.0, "shows_in_hud": True, "clears_previous": True,
                   "set_effect": lambda p, c: p._set_curse_effects(c),
                   "clear_effect": lambda p, c: p._clear_curse_effects(c)},
    "no_bomb": {"duration": 40.0, "shows_in_hud": True, "clears_previous": True,
                "set_effect": lambda p, c: p._set_curse_effects(c),
                "clear_effect": lambda p, c: p._clear_curse_effects(c)},
    "auto_bomb": {"duration": 40.0, "shows_in_hud": True, "clears_previous": True,
                  "set_effect": lambda p, c: p._set_curse_effects(c),
                  "clear_effect": lambda p, c: p._clear_curse_effects(c)},
    "inverted": {"duration": 40.0, "shows_in_hud": True, "clears_previous": True,
                 "set_effect": lambda p, c: p._set_curse_effects(c),
                 "clear_effect": lambda p, c: p._clear_curse_effects(c)},
    "hyper_speed": {"duration": 40.0, "shows_in_hud": True, "clears_previous": True,
                    "set_effect": lambda p, c: p._set_curse_effects(c),
                    "clear_effect": lambda p, c: p._clear_curse_effects(c)},
    "slow_speed": {"duration": 40.0, "shows_in_hud": True, "clears_previous": True,
                   "set_effect": lambda p, c: p._set_curse_effects(c),
                   "clear_effect": lambda p, c: p._clear_curse_effects(c)},
}


def respawn_all_abilities_with_animation():
    """
    Reparte de nuevo todas las habilidades (excepto calavera) con animación.
    """
    global powerups, grid  # o ajusta si usas otro nombre de lista o variable
    # 1) Elimina las habilidades existentes (excepto calavera)
    for p in powerups[:]:
        if p.type != "calavera":
            powerups.remove(p)
    # 2) Reparte nuevas en tiles libres con animación
    free_tiles = [(x, y) for y, row in enumerate(grid)
                  for x, val in enumerate(row) if val == 0]
    random.shuffle(free_tiles)
    for ability_type in ["speed", "bomb", "range", "push", "hit"]:
        if not free_tiles:
            break
        tx, ty = free_tiles.pop()
        new_pu = PowerUp(tx, ty, ability_type)
        powerups.append(new_pu)
        new_pu.start_spawn_animation()


pygame.display.set_caption("Bomberman - Maldiciones Rebotando")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
font = pygame.font.SysFont("Arial", 20)

EXPLOSION_DURATION = 0.75
PUSH_SPEED = 3

exploding_blocks = {}


# ------------------------------------------------------------------------------------
# Función para cargar imágenes
# ------------------------------------------------------------------------------------
def load_image(file, size, folder=ASSETS_DIR):
    return pygame.transform.scale(
        pygame.image.load(os.path.join(folder, file)).convert_alpha(),
        size
    )


def cargar_mapa():  # FUNCION CARGAR MAPA SEGUN SELECCION
    nombre_mapa = config.selected_map
    mapa_path = os.path.join(ASSETS_DIR, "Mapas", "Mapa" + str(nombre_mapa))
    SUELO1 = load_image("suelo1.png", (TILE_SIZE, TILE_SIZE), folder=mapa_path)
    SUELO2 = load_image("suelo2.png", (TILE_SIZE, TILE_SIZE), folder=mapa_path)
    STONE = load_image("muro_irrompible.png", (TILE_SIZE, TILE_SIZE), folder=mapa_path)
    BRICK = load_image("muro_rompible.png", (TILE_SIZE, TILE_SIZE), folder=mapa_path)
    LIMIT_IMG = load_image("limite_mapa.png", (TILE_SIZE, TILE_SIZE), folder=mapa_path)

    return SUELO1, SUELO2, STONE, BRICK, LIMIT_IMG


# Habilidades
SPEED_IMG = load_image("mas_velocidad.png", (40, 40), folder=os.path.join(ASSETS_DIR, "Gadgets", "Habilidades"))
MORE_BOMB_IMG = load_image("mas_bombas.png", (40, 40), folder=os.path.join(ASSETS_DIR, "Gadgets", "Habilidades"))
MAYOR_EXPLOSION_IMG = load_image("mayor_explosion.png", (40, 40),
                                 folder=os.path.join(ASSETS_DIR, "Gadgets", "Habilidades"))

# Poderes
PUSH_BOMB_IMG = load_image("patada.png", (40, 40), folder=os.path.join(ASSETS_DIR, "Gadgets", "Poderes"))
PUÑO_IMG = load_image("puño.png", (40, 40), folder=os.path.join(ASSETS_DIR, "Gadgets", "Poderes"))
ESCUDO_IMG = load_image("escudo.png", (40, 40), folder=os.path.join(ASSETS_DIR, "Gadgets", "Poderes"))

# Maldiciones
CALAVERA_IMG = load_image("calavera.png", (40, 40), folder=os.path.join(ASSETS_DIR, "Gadgets", "Maldiciones"))

# Lapidas
LAPIDA_IMG = load_image("lapida.png", (TILE_SIZE, TILE_SIZE), folder=os.path.join(ASSETS_DIR, "Mapas"))

# Marcas de jugadores (escalado proporcional)
def load_mark_scaled(path):
    full_path = os.path.join(ASSETS_DIR, "Jugadores", "Marca", path)
    img = pygame.image.load(full_path).convert_alpha()
    scale_factor = 0.03  # ajusta este factor según lo pequeño que lo quieras
    new_width = int(img.get_width() * scale_factor)
    new_height = int(img.get_height() * scale_factor)
    return pygame.transform.smoothscale(img, (new_width, new_height))


PLAYER_MARKS = [
    load_mark_scaled("Jugador 1.png"),
    load_mark_scaled("Jugador 2.png"),
    load_mark_scaled("Jugador 3.png"),
    load_mark_scaled("Jugador 4.png")
]

# Sonidos
SOUND_BOMB_PATH = os.path.join(ASSETS_DIR, "Sonidos_juego", "bomba", "explotar_bomba.wav")
EXPLOSION_SOUND = pygame.mixer.Sound(SOUND_BOMB_PATH)
EXPLOSION_SOUND.set_volume(0.35)

COLOCAR_BOMBA_SOUND_PATH = os.path.join(ASSETS_DIR, "Sonidos_juego", "bomba", "colocar_bomba.wav")
COLOCAR_BOMBA_SOUND = pygame.mixer.Sound(COLOCAR_BOMBA_SOUND_PATH)
COLOCAR_BOMBA_SOUND.set_volume(0.35)

FOOTSTEP_SOUND_PATH = os.path.join(ASSETS_DIR, "Sonidos_juego", "movimiento", "pisadas_jugador.wav")
FOOTSTEP_SOUND = pygame.mixer.Sound(FOOTSTEP_SOUND_PATH)
FOOTSTEP_SOUND.set_volume(1)

COGER_HABILIDAD_SOUND_PATH = os.path.join(ASSETS_DIR, "Sonidos_juego", "habilidades", "coger_habilidad.wav")
COGER_HABILIDAD_SOUND = pygame.mixer.Sound(COGER_HABILIDAD_SOUND_PATH)
COGER_HABILIDAD_SOUND.set_volume(0.35)

COGER_MALDICION_SOUND = pygame.mixer.Sound(
    os.path.join(ASSETS_DIR, "Sonidos_juego", "habilidades", "coger_maldicion.mp3"))
COGER_MALDICION_SOUND.set_volume(0.35)

MUERTE_SOUND_PATH = os.path.join(ASSETS_DIR, "Sonidos_juego", "Personajes", "muerte.mpeg")
MUERTE_SOUND = pygame.mixer.Sound(MUERTE_SOUND_PATH)
MUERTE_SOUND.set_volume(0.4)

REAPARICION_SOUND_PATH = os.path.join(ASSETS_DIR, "Sonidos_juego", "Personajes", "reaparicion.mp3")
REAPARICION_SOUND = pygame.mixer.Sound(REAPARICION_SOUND_PATH)
REAPARICION_SOUND.set_volume(0.4)

FANTASMA_SOUND_PATH = os.path.join(ASSETS_DIR, "Sonidos_juego", "movimiento", "fantasma.mp3")
FANTASMA_SOUND = pygame.mixer.Sound(FANTASMA_SOUND_PATH)
FANTASMA_SOUND.set_volume(0.7)

modo_posicion = config.current_position_index

posiciones_iniciales = [
    (1, 1),
    (GRID_COLS - 2, GRID_ROWS - 2),
    (1, GRID_ROWS - 2),
    (GRID_COLS - 2, 1),
]

# Controles por defecto para teclado
controles_teclado = {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "bomb": pygame.K_RETURN,
    "hit": pygame.K_p,
}

# Animaciones de explosión de la bomba
EXPLOSION_FRAMES = [load_image(f"explosion_{i}.png", (40, 40)) for i in range(3)]
CENTER_EXPLOSION_FRAMES = []
for i in range(1, 18):
    nombre = f"bomba_c{i}.png"
    img = load_image(nombre, (40, 40), folder=os.path.join(ASSETS_DIR, "Bombas"))
    CENTER_EXPLOSION_FRAMES.append({"image": img, "name": nombre})

EXTREME_EXPLOSION_FRAMES = []
for i in range(1, 18):
    nombre = f"ex_e{i}.png"
    img = load_image(nombre, (40, 40), folder=os.path.join(ASSETS_DIR, "Bombas"))
    EXTREME_EXPLOSION_FRAMES.append({"image": img, "name": nombre})

LATERAL_EXPLOSION_FRAMES = []
for i in range(1, 18):
    nombre = f"ex_l{i}.png"
    img = load_image(nombre, (40, 40), folder=os.path.join(ASSETS_DIR, "Bombas"))
    LATERAL_EXPLOSION_FRAMES.append({"image": img, "name": nombre})

ABILITY_EXPLOSION_FRAMES = [load_image("habilidad_ex" + str(i) + ".png", (40, 40),
                                       folder=os.path.join(ASSETS_DIR, "Gadgets", "Explosion_gadget"))
                            for i in range(1, 18)]

POWERUP_DESTROY_FRAMES = [pygame.Surface((40, 40)), pygame.Surface((40, 40))]
POWERUP_DESTROY_FRAMES[0].fill((255, 200, 0))
POWERUP_DESTROY_FRAMES[1].fill((255, 100, 0))

BOMB_IMAGES = []
bomb_folder = os.path.join(ASSETS_DIR, "Bombas")
for i in range(1, 16):
    img = load_image("bomb" + str(i) + ".png", (40, 40), folder=bomb_folder)
    BOMB_IMAGES.append(img)

POWERUP_DESTROY_FRAMES = [pygame.Surface((40, 40)), pygame.Surface((40, 40))]
POWERUP_DESTROY_FRAMES[0].fill((255, 200, 0))
POWERUP_DESTROY_FRAMES[1].fill((255, 100, 0))


# ------------------------------------------------------------------------------------
# Funciones auxiliares
# ------------------------------------------------------------------------------------
def tile_blocked_for_player(grid, bombs, tile_x, tile_y, player):
    if tile_x < 0 or tile_x >= GRID_COLS or tile_y < 0 or tile_y >= GRID_ROWS:
        return True

    # --- > LÓGICA MODIFICADA AQUÍ <---
    # Comprobar si el jugador es un fantasma
    if player.is_ghost:
        # Un fantasma solo es bloqueado por muros irrompibles (2) y límites (3)
        if grid[tile_y][tile_x] in (2, 3):
            return True
        # Los fantasmas ignoran bloques rompibles (1) y bombas, así que no hacemos más comprobaciones
        return False
    else:
        # Lógica original para jugadores vivos
        if grid[tile_y][tile_x] in (1, 2, 3):
            return True
        for b in bombs:
            if b.tile_x == tile_x and b.tile_y == tile_y:
                if player in b.passable_players:
                    return False
                else:
                    return True
        return False

def generar_poderes_al_morir(grid, bombs, powerups, players):
    """
    Genera entre 2 y 5 gadgets aleatorios en casillas completamente libres cuando un jugador muere.
    Cada gadget se coloca en una casilla diferente y con animación de aparición.
    """
    tipos_poderes = ["speed", "more_bomb", "major_explosion", "push_bomb", "golpear_bombas"]
    cantidad = random.randint(2, 5)
    celdas_validas = []

    for y in range(1, GRID_ROWS - 1):
        for x in range(1, GRID_COLS - 1):
            if grid[y][x] != 0:
                continue
            if any(b.tile_x == x and b.tile_y == y for b in bombs):
                continue
            if any(p.x == x and p.y == y and p.visible for p in powerups):
                continue
            if any(
                pygame.Rect(jugador.x, jugador.y, jugador.hitbox_size, jugador.hitbox_size).colliderect(
                    pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                ) for jugador in players
            ):
                continue
            # Casilla válida
            celdas_validas.append((x, y))

    random.shuffle(celdas_validas)
    for i in range(min(cantidad, len(celdas_validas))):
        x, y = celdas_validas[i]
        tipo = random.choice(tipos_poderes)
        nuevo_poder = PowerUp(x, y, tipo)
        nuevo_poder.visible = True
        nuevo_poder.start_spawn_animation()
        powerups.append(nuevo_poder)

def reveal_powerup_if_any(powerups, x, y):
    for p in powerups:
        if p.x == x and p.y == y and not p.visible:
            p.visible = True


def get_available_free_cells(grid, powerups):
    cells = []
    for y in range(1, GRID_ROWS - 1):
        for x in range(1, GRID_COLS - 1):
            if grid[y][x] == 0:
                if not any(p.x == x and p.y == y and p.visible for p in powerups):
                    cells.append((x, y))
    return cells


def get_free_cells(grid):
    cells = []
    for y in range(1, GRID_ROWS - 1):
        for x in range(1, GRID_COLS - 1):
            if grid[y][x] == 0:
                cells.append((x, y))
    return cells


def find_free_cell_far_from(player, grid):
    player_tile = player.get_center_tile()
    free_cells = get_free_cells(grid)
    if free_cells:
        far_cell = max(free_cells, key=lambda cell: math.hypot(cell[0] - player_tile[0], cell[1] - player_tile[1]))
        return far_cell
    return player_tile


def update_powerups(powerups, dt):
    to_remove = []
    for p in powerups:
        p.update(dt)
        if p.is_destroyed():
            to_remove.append(p)
    for r in to_remove:
        powerups.remove(r)


def draw_powerups(screen, powerups):
    # Dibujamos los powerups (maldiciones) después de las explosiones para que se vean por encima
    for p in powerups:
        p.draw(screen)


# ------------------------------------------------------------------------------------
# Función HUD combinada: Bonus y Curse
# ------------------------------------------------------------------------------------
def draw_HUD(screen, player, pos, color):
    x, y = pos
    line_height = 20
    # Mostrar puntuación de sets ganados
    score_text = f"Sets: {player.sets_won}"
    screen.blit(font.render(score_text, True, color), (x, y))
    y += line_height + 5  # Añadimos un pequeño espacio extra

    # --- > INICIO DE LA MODIFICACIÓN <---
    # Lógica para mostrar el estado de las bombas
    if player.is_ghost:
        # Si el jugador es un fantasma, comprobar el cooldown
        current_time = time.time()
        elapsed_since_bomb = current_time - player.last_bomb_placed_time

        if elapsed_since_bomb < player.ghost_bomb_cooldown:
            # Si la bomba está en cooldown, mostrar el tiempo restante
            remaining_cooldown = player.ghost_bomb_cooldown - elapsed_since_bomb
            # Se usa max(0, ...) para evitar números negativos y +1 para que el contador sea más intuitivo (30s a 1s)
            text = f"Bombas: x0 ({max(0, int(remaining_cooldown)) + 1}s)"
        else:
            # Si el cooldown ha terminado, la bomba está disponible
            text = "Bombas: x1"
    else:
        # Si es un jugador vivo, mostrar el límite de bombas normal
        text = f"Bombas: x{player.bomb_limit}"

    screen.blit(font.render(text, True, color), (x, y))
    y += line_height
    # --- > FIN DE LA MODIFICACIÓN <---

    # El resto de la función se mantiene como la tenías
    text = f"Rango x{player.bomb_range}"
    screen.blit(font.render(text, True, color), (x, y))
    y += line_height

    # Lógica para la velocidad
    if player.is_ghost:
        text = "Velocidad: Fantasma"
    elif player.curse == "slow_speed":
        text = "Velocidad: slow"
    elif player.curse == "hyper_speed":
        text = "Velocidad: fast"
    else:
        text = f"Velocidad x{player.display_speed}"

    screen.blit(font.render(text, True, color), (x, y))
    y += line_height
    text = "Empujar bomba: Sí" if player.push_bomb_available else "Empujar bomba: No"
    screen.blit(font.render(text, True, color), (x, y))
    y += line_height
    text = "Golpear bombas: Sí" if player.hit_bomb_available else "Golpear bombas: No"
    screen.blit(font.render(text, True, color), (x, y))
    y += line_height
    if player.escudo_available:
        current_time = time.time()
        if current_time < player.escudo_cooldown_end_time:
            remaining_cooldown = player.escudo_cooldown_end_time - current_time
            text = f"Escudo: No ({max(0, int(remaining_cooldown)) + 1}s)"
        else:
            text = "Escudo: Sí"
    else:
        text = "Escudo: No"
    screen.blit(font.render(text, True, color), (x, y))
    y += line_height
    if getattr(player, 'active_curse', None) and getattr(player, 'curse_ends_at', None):
        meta = CURSES[player.active_curse]
        # Solo mostrar temporales
        if meta["shows_in_hud"] and meta["duration"] is not None:
            remaining = max(0, int(player.curse_ends_at - time.time()))
            text = f"{player.active_curse}: {remaining}s"
        else:
            text = "No curse"
    else:
        text = "No curse"

    # Este bloque if/else estaba duplicado en tu código, lo he dejado en una sola versión
    screen.blit(font.render(text, True, color), (x, y))


# ------------------------------------------------------------------------------------
# Temporizador
# ------------------------------------------------------------------------------------
def load_timer_images():
    DIGIT_SIZE = (40, 60)
    SEPARADOR_SIZE = (20, 60)
    MARCO_SIZE = (200, 80)
    contador_dir = os.path.join(ASSETS_DIR, "Contador")
    timer_digits = {}
    for i in range(10):
        timer_digits[str(i)] = load_image(f"{i}.png", DIGIT_SIZE, folder=contador_dir)
    timer_separador = load_image("separador.png", SEPARADOR_SIZE, folder=contador_dir)
    timer_marco = load_image("marco_contador.png", MARCO_SIZE, folder=contador_dir)
    return timer_digits, timer_separador, timer_marco, DIGIT_SIZE, SEPARADOR_SIZE, MARCO_SIZE


timer_digits, timer_separador, timer_marco, DIGIT_SIZE, SEPARADOR_SIZE, MARCO_SIZE = load_timer_images()


def draw_timer(screen, remaining_time):
    remaining = int(remaining_time)
    minutes = remaining // 60
    seconds = remaining % 60
    time_str = f"{minutes:02d}{seconds:02d}"
    timer_width = 4 * DIGIT_SIZE[0] + SEPARADOR_SIZE[0]
    marco_width = MARCO_SIZE[0]
    marco_x = (WIDTH - marco_width) // 2
    marco_y = 10
    screen.blit(timer_marco, (marco_x, marco_y))
    timer_x = marco_x + (marco_width - timer_width) // 2
    timer_y = marco_y + (MARCO_SIZE[1] - DIGIT_SIZE[1]) // 2
    screen.blit(timer_digits[time_str[0]], (timer_x, timer_y))
    screen.blit(timer_digits[time_str[1]], (timer_x + DIGIT_SIZE[0], timer_y))
    screen.blit(timer_separador, (timer_x + 2 * DIGIT_SIZE[0], timer_y))
    screen.blit(timer_digits[time_str[2]], (timer_x + 2 * DIGIT_SIZE[0] + SEPARADOR_SIZE[0], timer_y))
    screen.blit(timer_digits[time_str[3]], (timer_x + 3 * DIGIT_SIZE[0] + SEPARADOR_SIZE[0], timer_y))


# ------------------------------------------------------------------------------------
# Clase PowerUp (maldición que rebota de 1 en 1)
# ------------------------------------------------------------------------------------
class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.completed = False
        self.visible = False
        self.block_explosion = True
        self.disappearing = False
        self.destroy_frames = POWERUP_DESTROY_FRAMES
        self.destroy_frame_index = 0
        self.destroy_frame_time = 100
        self.last_update = pygame.time.get_ticks()
        self.vanished = False
        self.spawn_timer = 0.0
        self.spawning = True
        # atributos para rebote:
        self.bouncing = False
        self.bounce_dir = (0, 0)
        self.bounce_path = []  # lista de tiles [(x1,y1), (x2,y2), …]
        self.bounce_index = 0  # casilla actual en path
        self.bounce_timer = 0.0  # acumulador de tiempo
        self.bounce_cell_time = 0.15  # segundos que dura botar de una celda a la siguiente

    def start_spawn_animation(self):
        self.spawning = True
        self.spawn_timer = 0.0

    def update(self, dt):
        # Lógica de animación de spawn (si self.spawning está activo)
        if self.spawning:
            self.spawn_timer += dt
            if self.spawn_timer >= 0.5:  # media segundo de animación
                self.spawning = False

    def update(self, dt):
        if self.disappearing:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.destroy_frame_time:
                self.destroy_frame_index += 1
                self.last_update = now

        if self.vanished:
            self.disappearing = True
            self.destroy_frame_index = len(self.destroy_frames)

        if self.bouncing:
            self.bounce_timer += dt

            # Solo avanzar si hay otra celda a la que moverse
            if self.bounce_index + 1 < len(self.bounce_path):
                if self.bounce_timer >= self.bounce_cell_time:
                    self.bounce_timer -= self.bounce_cell_time
                    self.bounce_index += 1

                    if self.bounce_index >= len(self.bounce_path):
                        fx, fy = self.bounce_path[-1]
                        self.x, self.y = fx, fy
                        self.bouncing = False
                    else:
                        self.x, self.y = self.bounce_path[self.bounce_index]
            else:
                # Si ya no hay siguiente, terminamos la animación
                fx, fy = self.bounce_path[-1]
                self.x, self.y = fx, fy
                self.bouncing = False

    def draw(self, screen):
        if not self.visible or self.vanished:
            return

        if self.bouncing and len(self.bounce_path) >= 2:
            ability_size = int(TILE_SIZE * 0.8)

            # Usamos el índice actual y forzamos siempre la animación del tramo activo
            idx = self.bounce_index
            x1, y1 = self.bounce_path[idx]
            x2, y2 = self.bounce_path[min(idx + 1, len(self.bounce_path) - 1)]

            px1 = x1 * TILE_SIZE + TILE_SIZE // 2
            py1 = y1 * TILE_SIZE + TILE_SIZE // 2 + TOP_OFFSET
            px2 = x2 * TILE_SIZE + TILE_SIZE // 2
            py2 = y2 * TILE_SIZE + TILE_SIZE // 2 + TOP_OFFSET

            # t controla el progreso dentro del tramo, garantiza curva desde el principio
            t = max(0.0, min(self.bounce_timer / self.bounce_cell_time, 1.0))

            dx_px = px2 - px1
            dy_px = py2 - py1

            map_w = WIDTH
            map_h = HEIGHT - TOP_OFFSET
            half_w = map_w // 2
            half_h = map_h // 2

            if abs(dx_px) > half_w:
                dx_px -= map_w * (1 if dx_px > 0 else -1)
            if abs(dy_px) > half_h:
                dy_px -= map_h * (1 if dy_px > 0 else -1)

            interp_x = px1 + dx_px * t
            interp_y = py1 + dy_px * t

            # Esta es la parábola para el efecto de bote, ahora visible desde el primer salto
            arc = -TILE_SIZE * 0.45 * math.sin(math.pi * t)
            interp_y += arc

            if self.teleporting:
                if abs(px2 - px1) > half_w:
                    interp_x += WIDTH if px2 > px1 else -WIDTH
                if abs(py2 - py1) > half_h:
                    interp_y += HEIGHT if py2 > py1 else -HEIGHT

            img = pygame.transform.scale(CALAVERA_IMG, (ability_size, ability_size))
            screen.blit(img, (interp_x - ability_size // 2, interp_y - ability_size // 2))
            return

        # Dibujo estático/flotante
        ability_size = int(TILE_SIZE * 0.8)
        amplitude = 3.0
        freq = 0.4
        offset_y = amplitude * math.sin(2 * math.pi * freq * time.time())
        center_x = self.x * TILE_SIZE + TILE_SIZE // 2
        center_y = self.y * TILE_SIZE + TILE_SIZE // 2 + TOP_OFFSET + int(offset_y)
        top_left_x = center_x - ability_size // 2
        top_left_y = center_y - ability_size // 2

        if self.type == "major_explosion":
            img = MAYOR_EXPLOSION_IMG
        elif self.type == "speed":
            img = SPEED_IMG
        elif self.type == "more_bomb":
            img = MORE_BOMB_IMG
        elif self.type == "calavera":
            img = CALAVERA_IMG
        elif self.type == "push_bomb":
            img = PUSH_BOMB_IMG
        elif self.type == "golpear_bombas":
            img = PUÑO_IMG
        elif self.type == "escudo":
            img = ESCUDO_IMG
        elif self.type == "reset":
            img = CALAVERA_IMG
        elif self.type in CURSES:
            img = CALAVERA_IMG
        else:
            if self.destroy_frame_index < len(self.destroy_frames):
                img = self.destroy_frames[self.destroy_frame_index]
            else:
                img = CALAVERA_IMG

        scaled_img = pygame.transform.scale(img, (ability_size, ability_size))
        screen.blit(scaled_img, (top_left_x, top_left_y))

    def start_disappear(self):
        self.disappearing = True
        self.destroy_frame_index = 0
        self.last_update = pygame.time.get_ticks()

    def is_destroyed(self):
        if self.vanished:
            return True
        return (self.disappearing and (self.destroy_frame_index >= len(self.destroy_frames)))

    def calculate_bounce_path(self, direction, grid, bombs, powerups):
        """
        direction: (dx,dy) de la explosión.
        Devuelve la secuencia de celdas destino hasta encontrar una libre.
        Con wrap-around en bordes.
        """
        dx, dy = direction
        path = []
        cx, cy = self.x, self.y

        # avanzamos 1 en 1 hasta encontrar un destino válido
        while True:
            nx = (cx + dx) % GRID_COLS
            ny = (cy + dy) % GRID_ROWS
            if (dx == 1 and nx == 0) or (dx == -1 and nx == GRID_COLS - 1):
                self.teleporting = True
            elif (dy == 1 and ny == 0) or (dy == -1 and ny == GRID_ROWS - 1):
                self.teleporting = True
            else:
                self.teleporting = False
            # ¿casilla libre para terminar?
            libre = (grid[ny][nx] == 0 and
                     not any(p.x == nx and p.y == ny and p.visible and p.type in CURSES for p in powerups))
            path.append((nx, ny))

            if libre:
                break

            # sino, saltamos a la siguiente
            cx, cy = nx, ny

        return path

    def start_bounce(self, direction, grid, bombs, powerups):
        # Construye la ruta incluyendo la posición actual como primer punto
        path = []
        cx, cy = self.x, self.y
        dx, dy = direction

        while True:
            nx = (cx + dx) % GRID_COLS
            ny = (cy + dy) % GRID_ROWS

            # Si hay wrap-around, activa teleporting
            if (dx == 1 and nx == 0) or (dx == -1 and nx == GRID_COLS - 1):
                self.teleporting = True
            elif (dy == 1 and ny == 0) or (dy == -1 and ny == GRID_ROWS - 1):
                self.teleporting = True
            else:
                self.teleporting = False

            # Detectar si hay otra maldición visible
            otra_maldicion = any(
                p.x == nx and p.y == ny and p.visible and not p.disappearing and p.type == "calavera"
                for p in powerups
            )

            # Detectar si hay una habilidad distinta a calavera
            habilidad_diferente = None
            for p in powerups:
                if p.x == nx and p.y == ny and p.visible and not p.disappearing and p.type != "calavera":
                    habilidad_diferente = p
                    break

            if habilidad_diferente:
                habilidad_diferente.start_disappear()

            # Si no hay otra maldición, esta casilla es válida para terminar
            if grid[ny][nx] == 0 and not otra_maldicion:
                path.append((nx, ny))
                break

            path.append((nx, ny))
            cx, cy = nx, ny

        # Incluye la posición actual como primer paso para animar desde el inicio
        self.bounce_path = [(self.x, self.y)] + path
        self.bouncing = True
        self.bounce_index = 0
        self.bounce_timer = 0.0


# ------------------------------------------------------------------------------------
# Clase Player (sin cambios)
# ------------------------------------------------------------------------------------
class Player:
    def __init__(self, init_tile_x, init_tile_y, color, controls):
        self.initial_tile_x = init_tile_x
        self.initial_tile_y = init_tile_y
        self.active_curse = None
        self.curse_ends_at = None
        self.x = init_tile_x * TILE_SIZE - 40
        self.y = init_tile_y * TILE_SIZE - 40
        self.color = color
        self.can_pick_abilities = True
        self.can_place_bombs = True
        self.auto_bombing = False
        self.invert_controls = False
        self.speed = 2.0
        self.base_speed = 2.0
        self.display_speed = 1
        self.pending_speed_boosts = 0
        self.controls = controls
        self.original_controls = controls.copy()
        self.bomb_range = 1
        self.bomb_limit = 1
        self.sprite_size = 120
        self.hitbox_size = 36
        self.sprite_draw_offset_y = -10
        self.anim_frame = 0
        self.last_anim_update = time.time()
        self.anim_delay = 0.2
        self.current_direction = "right"
        self.prev_x = self.x
        self.prev_y = self.y
        self.last_step_sound = 0
        self.step_delay = 0.3
        self.auto_align_factor = 0.5
        self.curse = None
        self.curse_start = None
        self.curse_multiplier = 1
        self.last_curse_exchange = 0
        self.flashing = False
        self.flash_count = 0
        self.flash_timer = 0
        self.last_auto_bomb_tile = None
        self.push_bomb_available = False
        self.hit_bomb_available = False
        self.is_ghost = False
        self.ghost_anim_frames = []
        self.ghost_anim_frame_index = 0
        self.last_ghost_anim_update = 0
        self.ghost_anim_delay = 100  # ms por frame del GIF
        self.last_bomb_placed_time = 0
        self.ghost_bomb_cooldown = 30.0  # 30 segundos
        self.is_invulnerable = False
        self.invulnerable_until = 0
        self.invulnerable_duration = 3.0  # 3 segundos
        self.invulnerable_flash_timer = 0
        self.escudo_available = False
        self.escudo_active = False
        self.escudo_activation_time = 0
        self.escudo_duration = 10.0
        self.escudo_cooldown_end_time = 0
        self.escudo_cooldown_duration = 30.0
        self.sets_won = 0
        self.is_set_winner = False
        self.set_winner_start_time = 0.0
        self.is_eliminated = False

    def get_center_coords(self):
        return (self.x + self.sprite_size / 2, self.y + self.sprite_size / 2)

    def get_hitbox(self):
        center_x = self.x + self.sprite_size // 2
        center_y = self.y + self.sprite_size // 2
        left = center_x - self.hitbox_size // 2
        top = center_y - self.hitbox_size // 2
        return pygame.Rect(left, top, self.hitbox_size, self.hitbox_size)

    def get_center_tile(self):
        cx, cy = self.get_center_coords()
        return int(cx // TILE_SIZE), int(cy // TILE_SIZE)

    def check_collision(self, grid, bombs):
        # SI ES FANTASMA, APLICA REGLAS DE COLISIÓN ESPECIALES
        if self.is_ghost:
            rect = self.get_hitbox()
            left_cell = rect.left // TILE_SIZE
            right_cell = (rect.right - 1) // TILE_SIZE
            top_cell = rect.top // TILE_SIZE
            bottom_cell = (rect.bottom - 1) // TILE_SIZE

            for cell_x in range(left_cell, right_cell + 1):
                for cell_y in range(top_cell, bottom_cell + 1):
                    if cell_x < 0 or cell_x >= GRID_COLS or cell_y < 0 or cell_y >= GRID_ROWS:
                        return True # Choca con los límites exteriores del mapa
                    # Un fantasma solo choca con muros irrompibles (2) y límites (3)
                    if grid[cell_y][cell_x] in (2, 3):
                        return True
            # Los fantasmas no chocan con bombas ni con bloques rompibles.
            return False

        # CÓDIGO ORIGINAL PARA JUGADORES VIVOS (SIN CAMBIOS)
        rect = self.get_hitbox()
        left_cell = rect.left // TILE_SIZE
        right_cell = (rect.right - 1) // TILE_SIZE
        top_cell = rect.top // TILE_SIZE
        bottom_cell = (rect.bottom - 1) // TILE_SIZE
        for cell_x in range(left_cell, right_cell + 1):
            for cell_y in range(top_cell, bottom_cell + 1):
                if cell_x < 0 or cell_x >= GRID_COLS or cell_y < 0 or cell_y >= GRID_ROWS:
                    return True
                if grid[cell_y][cell_x] in (1, 2, 3):
                    return True
        for bomb in bombs:
            bomb_rect = pygame.Rect(bomb.pos_x, bomb.pos_y, TILE_SIZE, TILE_SIZE)
            if rect.colliderect(bomb_rect) and self not in bomb.passable_players:
                return True
        return False

    def is_compressed_vertically(self, grid, bombs):
        cx, cy = self.get_center_tile()
        up_blocked = tile_blocked_for_player(grid, bombs, cx, cy - 1, self)
        down_blocked = tile_blocked_for_player(grid, bombs, cx, cy + 1, self)
        return up_blocked and down_blocked

    def is_compressed_horizontally(self, grid, bombs):
        cx, cy = self.get_center_tile()
        left_blocked = tile_blocked_for_player(grid, bombs, cx - 1, cy, self)
        right_blocked = tile_blocked_for_player(grid, bombs, cx + 1, cy, self)
        return left_blocked and right_blocked

    def auto_align_x_once(self, grid, bombs):
        cx, cy = self.get_center_tile()
        desired_x = cx * TILE_SIZE + (TILE_SIZE // 2) - self.sprite_size // 2
        dist = desired_x - self.x
        if abs(dist) < 0.1:
            return True
        direction = 1 if dist > 0 else -1
        max_move = min(abs(dist), self.speed * self.auto_align_factor)
        old_x = self.x
        self.x += direction * max_move
        if self.check_collision(grid, bombs):
            self.x = old_x
            return True
        if abs(self.x - desired_x) < 0.1:
            self.x = desired_x
            return True
        return False

    def auto_align_y_once(self, grid, bombs):
        cx, cy = self.get_center_tile()
        desired_y = cy * TILE_SIZE + (TILE_SIZE // 2) - self.sprite_size // 2
        dist = desired_y - self.y
        if abs(dist) < 0.1:
            return True
        direction = 1 if dist > 0 else -1
        max_move = min(abs(dist), self.speed * self.auto_align_factor)
        old_y = self.y
        self.y += direction * max_move
        if self.check_collision(grid, bombs):
            self.y = old_y
            return True
        if abs(self.y - desired_y) < 0.1:
            self.y = desired_y
            return True
        return False

    def activate_escudo(self):
        current_time = time.time()
        if (self.escudo_available and
                not self.escudo_active and
                current_time >= self.escudo_cooldown_end_time):
            self.escudo_active = True
            self.escudo_activation_time = current_time

    def update_escudo(self):
        if self.escudo_active and time.time() > self.escudo_activation_time + self.escudo_duration:
            self.escudo_active = False
            self.escudo_cooldown_end_time = time.time() + self.escudo_cooldown_duration

    def move_in_small_steps(self, dx, dy, grid, bombs):
        steps_int = int(self.speed)
        frac = self.speed - steps_int
        for _ in range(steps_int):
            old_x, old_y = self.x, self.y
            self.x += dx
            self.y += dy
            if self.check_collision(grid, bombs):
                self.x, self.y = old_x, old_y

                if self.push_bomb_available:
                    cx = old_x + self.sprite_size // 2
                    cy = old_y + self.sprite_size // 2
                    tile_x = int(cx // TILE_SIZE)
                    tile_y = int(cy // TILE_SIZE)
                    dir_x, dir_y = dx, dy
                    if abs(dir_x) > abs(dir_y):
                        dir_y = 0
                        dir_x = 1 if dir_x > 0 else -1
                    else:
                        dir_x = 0
                        dir_y = 1 if dir_y > 0 else -1
                    next_tile_x = tile_x + dir_x
                    next_tile_y = tile_y + dir_y

                    bomb_target = next(
                        (b for b in bombs if b.tile_x == next_tile_x and b.tile_y == next_tile_y and not b.exploded),
                        None)
                    if bomb_target:
                        if not bomb_target.sliding:
                            bomb_target.try_start_push(dir_x, dir_y, grid, bombs, players, powerups)

        if frac > 0:
            old_x, old_y = self.x, self.y
            self.x += dx * frac
            self.y += dy * frac
            if self.check_collision(grid, bombs):
                self.x, self.y = old_x, old_y

    def move_up(self, grid, bombs, powerups, lapidas):
        self.current_direction = "up"
        if self.is_compressed_vertically(grid, bombs):
            return
        if self.auto_align_x_once(grid, bombs):
            old_tile = self.get_center_tile()  # ① guarda casilla antigua
            self.move_in_small_steps(0, -1, grid, bombs)  # ② mueve al jugador
            new_tile = self.get_center_tile()  # ③ lee casilla nueva
            # ④ si auto_bomb active y cambias de casilla, coloca bomba forzada
            if self.auto_bombing and new_tile != old_tile:
                self.place_bomb(bombs, powerups, grid, lapidas, forced=True)

    def move_down(self, grid, bombs, powerups, lapidas):
        self.current_direction = "down"
        if self.is_compressed_vertically(grid, bombs):
            return
        if self.auto_align_x_once(grid, bombs):
            old_tile = self.get_center_tile()
            self.move_in_small_steps(0, 1, grid, bombs)
            new_tile = self.get_center_tile()
            if self.auto_bombing and new_tile != old_tile:
                self.place_bomb(bombs, powerups, grid, lapidas, forced=True)

    def move_left(self, grid, bombs, powerups, lapidas):
        self.current_direction = "left"
        if self.is_compressed_horizontally(grid, bombs):
            return
        if self.auto_align_y_once(grid, bombs):
            old_tile = self.get_center_tile()
            self.move_in_small_steps(-1, 0, grid, bombs)
            new_tile = self.get_center_tile()
            if self.auto_bombing and new_tile != old_tile:
                self.place_bomb(bombs, powerups, grid, lapidas, forced=True)

    def move_right(self, grid, bombs, powerups, lapidas):
        self.current_direction = "right"
        if self.is_compressed_horizontally(grid, bombs):
            return
        if self.auto_align_y_once(grid, bombs):
            old_tile = self.get_center_tile()
            self.move_in_small_steps(1, 0, grid, bombs)
            new_tile = self.get_center_tile()
            if self.auto_bombing and new_tile != old_tile:
                self.place_bomb(bombs, powerups, grid, lapidas, forced=True)

    def update_passable(self, bombs):
        for bomb in bombs:
            if self in bomb.passable_players:
                bomb_rect = pygame.Rect(bomb.pos_x, bomb.pos_y, TILE_SIZE, TILE_SIZE)
                if not self.get_hitbox().colliderect(bomb_rect):
                    bomb.passable_players.remove(self)

    def update_animation(self):
        current_time = time.time()
        if (self.x != self.prev_x or self.y != self.prev_y):
            if (current_time - self.last_step_sound >= self.step_delay):
                FOOTSTEP_SOUND.play()
                self.last_step_sound = current_time
            if (current_time - self.last_anim_update >= self.anim_delay):
                self.anim_frame = (self.anim_frame + 1) % 9
                self.last_anim_update = current_time
        else:
            self.anim_frame = 0
        self.prev_x = self.x
        self.prev_y = self.y

    def apply_curse(self, curse_name):
        meta = CURSES[curse_name]

        # 1) Si la nueva maldición debe borrar la anterior, la limpiamos
        if meta.get("clears_previous", False) and self.active_curse:
            self._clear_curse_effects(self.active_curse)

        # 2) Para hyper_speed / slow_speed, guardamos velocidad actual y reseteamos boosts
        if curse_name in ("hyper_speed", "slow_speed"):
            self._saved_speed_before_curse = self.speed
            self.pending_speed_boosts = 0

        # 3) Activamos la maldición y calculamos su fin (si duration no es None)
        self.active_curse = curse_name
        duration = meta.get("duration")
        self.curse_ends_at = time.time() + duration if duration is not None else None

        # 4) Aplicamos el efecto concreto
        meta["set_effect"](self, curse_name)

        # 5) Caso especial: resetear habilidades sin tocar el timer
        if curse_name == "reset":
            self.bomb_limit = 1
            self.bomb_range = 1
            self._do_reset()

    def update_curse(self):
        """Debe llamarse cada frame para limpiar automáticamente al expirar."""
        if self.active_curse and self.curse_ends_at:
            if time.time() >= self.curse_ends_at:
                ended = self.active_curse
                self._clear_curse_effects(ended)
                self.active_curse = None
                self.curse_ends_at = None
                # Opcional: efecto de parpadeo al finalizar
                self.flashing = True
                self.flash_count = 3
                self.flash_timer = time.time()

    def _do_reset(self):
        self.bomb_limit = 1
        self.bomb_range = 1
        # Si guardas otras habilidades (speed, push, hit…), restáuralas también:
        self.speed = self.base_speed
        self.can_pick_abilities = True
        self.can_place_bombs = True
        self.auto_bombing = False
        self.invert_controls = False
        # Aquí debes llamar a tu rutina de respawn/animación:
        respawn_all_abilities_with_animation()

    def become_ghost(self):
        """
        Transforma al jugador en un fantasma en la casilla donde murió.
        """
        print(f"¡El jugador {self.player_index + 1} se ha convertido en un fantasma!")

        # 1. Estado de fantasma
        self.is_ghost = True
        self.is_invulnerable = False  # No es invulnerable como fantasma

        # 2. Limpiar estado de jugador vivo
        if self.active_curse:
            self._clear_curse_effects(self.active_curse)
        self.active_curse = None
        self.curse_ends_at = None
        self.bomb_limit = 1
        self.bomb_range = 1
        self.push_bomb_available = False
        self.hit_bomb_available = False
        self.display_speed = 1  # Mostramos la velocidad del fantasma
        self.pending_speed_boosts = 0
        # Resetear estado del escudo
        self.escudo_available = False
        self.escudo_active = False
        self.escudo_cooldown_end_time = 0

        # 3. Aplicar propiedades de fantasma
        self.speed = 1  # Velocidad reducida

        # El jugador no se mueve, se queda en la casilla donde murió.
        # Su posición (self.x, self.y) ya es la correcta.

    def eliminate(self):
        print(f"¡El jugador {self.player_index + 1} ha sido eliminado de la ronda!")
        self.is_eliminated = True

    def resurrect(self):
        """
        Devuelve al fantasma a la vida en su posición inicial.
        """
        print(f"¡El jugador {self.player_index + 1} ha vuelto a la vida!")
        REAPARICION_SOUND.play()  # Reproduce el sonido de reaparición
        self.is_ghost = False

        # Restaurar habilidades y estado de jugador vivo
        self.bomb_limit = 1
        self.bomb_range = 1
        self.speed = self.base_speed
        self.display_speed = 1
        self.push_bomb_available = False
        self.hit_bomb_available = False
        self.active_curse = None  # Limpiar cualquier maldición residual

        # Resetear estado del escudo
        self.escudo_available = False
        self.escudo_active = False
        self.escudo_cooldown_end_time = 0

        # Mover al jugador a su posición de inicio de partida
        self.x = self.initial_tile_x * TILE_SIZE - 40
        self.y = self.initial_tile_y * TILE_SIZE - 40

        # Activar invulnerabilidad temporal con parpadeo
        self.is_invulnerable = True
        self.invulnerable_until = time.time() + self.invulnerable_duration
        self.invulnerable_flash_timer = time.time()  # Inicia el temporizador para el parpadeo

    def draw(self, screen):
        # SI ES FANTASMA, DIBUJA EL GIF CON TRANSPARENCIA
        if self.is_ghost:
            if not self.ghost_anim_frames:
                return  # No hacer nada si la animación no se cargó

            # Actualizar frame de la animación del fantasma (siempre se mueve)
            current_time_ms = pygame.time.get_ticks()
            if current_time_ms - self.last_ghost_anim_update > self.ghost_anim_delay:
                self.ghost_anim_frame_index = (self.ghost_anim_frame_index + 1) % len(self.ghost_anim_frames)
                self.last_ghost_anim_update = current_time_ms

            sprite = self.ghost_anim_frames[self.ghost_anim_frame_index].copy()
            sprite.set_alpha(int(255 * 0.80))  # 80% de opacidad
            offset_x = (self.sprite_size - sprite.get_width()) // 2
            offset_y = (self.sprite_size - sprite.get_height()) // 2
            # Aplicamos el offset a las coordenadas de dibujado
            draw_x = self.x + offset_x
            draw_y = self.y + offset_y + self.sprite_draw_offset_y + TOP_OFFSET
            screen.blit(sprite, (draw_x, draw_y))
            return
        # --- PARPADEO DEL GANADOR DEL SET ---
        if self.is_set_winner:
            flash_interval = 0.1  # segundos
            if int((time.time() - self.set_winner_start_time) / flash_interval) % 2 == 0:
                flash_surf = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
                flash_surf.fill((255, 255, 255, 150))  # Blanco semitransparente
                screen.blit(flash_surf, (self.x, self.y + self.sprite_draw_offset_y + TOP_OFFSET))
        # SI ES UN JUGADOR VIVO, COMPROBAR INVULNERABILIDAD Y DIBUJAR NORMAL

        # 1) Aura por detrás (solo si hay maldición activa)
        if self.active_curse and CURSES[self.active_curse]["duration"] is not None:
            if not hasattr(Player, 'aura_frames'):
                import os
                from PIL import Image
                aura_path = os.path.join(os.path.dirname(__file__), ASSETS_DIR, "Gadgets", "Efectos_visuales",
                                         "maldicion.gif")
                pil_image = Image.open(aura_path)
                frames = []
                try:
                    while True:
                        frame = pil_image.convert("RGBA")
                        data = frame.tobytes()
                        mode = frame.mode
                        size = frame.size
                        surface = pygame.image.fromstring(data, size, mode)
                        frames.append(surface)
                        pil_image.seek(pil_image.tell() + 1)
                except EOFError:
                    pass
                Player.aura_frames = frames
                Player.aura_frame_count = len(frames)
                Player.aura_frame_duration = 100  # ms por frame

            current_time_ms = pygame.time.get_ticks()
            frame_index = (current_time_ms // Player.aura_frame_duration) % Player.aura_frame_count
            aura_image = Player.aura_frames[frame_index]
            new_size = int(self.sprite_size * 0.9)
            aura_image_scaled = pygame.transform.scale(aura_image, (new_size, new_size))

            aura_behind = aura_image_scaled.copy()
            aura_behind.set_alpha(150)
            aura_rect_behind = aura_behind.get_rect()
            aura_rect_behind.center = (
                self.x + self.sprite_size // 2,
                self.y + self.sprite_draw_offset_y + TOP_OFFSET + self.sprite_size // 2 - 10
            )
            screen.blit(aura_behind, aura_rect_behind)

        # --- INICIO DE LA MODIFICACIÓN ---

        # DIBUJO DEL ESCUDO (DETRÁS)
        if self.escudo_active:
            # Carga perezosa de los frames del GIF del escudo
            if not hasattr(Player, 'escudo_frames'):
                import os
                from PIL import Image
                escudo_path = os.path.join(os.path.dirname(__file__), ASSETS_DIR, "Gadgets", "Efectos_visuales",
                                           "escudo.gif")
                try:
                    pil_image = Image.open(escudo_path)
                    frames = []
                    while True:
                        frame = pil_image.convert("RGBA")
                        pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                        frames.append(pygame_frame)
                        pil_image.seek(pil_image.tell() + 1)
                except EOFError:
                    pass
                except (FileNotFoundError, ImportError):
                    frames = []
                Player.escudo_frames = frames
                Player.escudo_frame_count = len(frames) if frames else 1
                Player.escudo_frame_duration = 100  # ms por frame

            # Si los frames están cargados, dibujamos el GIF de detrás
            if Player.escudo_frames:
                current_time_ms = pygame.time.get_ticks()
                frame_index = (current_time_ms // Player.escudo_frame_duration) % Player.escudo_frame_count
                escudo_image = Player.escudo_frames[frame_index]
                new_size = int(self.sprite_size)
                escudo_image_scaled = pygame.transform.smoothscale(escudo_image, (new_size, new_size))

                # Crear y dibujar la copia de DETRÁS con 50% de opacidad
                escudo_behind = escudo_image_scaled.copy()
                escudo_behind.set_alpha(int(255 * 0.50))  # 50% Opacidad
                escudo_rect_behind = escudo_behind.get_rect()
                escudo_rect_behind.center = (
                    self.x + self.sprite_size // 2,
                    self.y + self.sprite_draw_offset_y + TOP_OFFSET + self.sprite_size // 2
                )
                screen.blit(escudo_behind, escudo_rect_behind)

        # 2) Dibujo del jugador (sprite según dirección y personaje)
        if hasattr(self, "animaciones") and self.current_direction in self.animaciones:
            image_list = self.animaciones[self.current_direction]
            sprite = image_list[self.anim_frame % len(image_list)]
            screen.blit(sprite, (self.x, self.y + self.sprite_draw_offset_y + TOP_OFFSET))
            # Dibujar la marca del jugador encima del sprite, tocando la cabeza
            if hasattr(self, "player_index") and 0 <= self.player_index < len(PLAYER_MARKS):
                mark_img = PLAYER_MARKS[self.player_index]
                mark_rect = mark_img.get_rect()
                altura_offset = +25  # puedes ajustar este valor (positivos bajan, negativos suben)
                mark_rect.midbottom = (
                    self.x + self.sprite_size // 2,
                    self.y + self.sprite_draw_offset_y + TOP_OFFSET + altura_offset
                )
                screen.blit(mark_img, mark_rect)

        # 3) Aura por delante (solo si hay maldición activa)
        if self.active_curse and CURSES[self.active_curse]["duration"] is not None:
            aura_front = aura_image_scaled.copy()
            aura_front.set_alpha(100)
            aura_rect_front = aura_front.get_rect()
            aura_rect_front.center = (
                self.x + self.sprite_size // 2,
                self.y + self.sprite_draw_offset_y + TOP_OFFSET + self.sprite_size // 2 - 10
            )
            screen.blit(aura_front, aura_rect_front)

        # DIBUJO DEL ESCUDO (DELANTE)
        if self.escudo_active and hasattr(Player, 'escudo_frames') and Player.escudo_frames:
            current_time_ms = pygame.time.get_ticks()
            frame_index = (current_time_ms // Player.escudo_frame_duration) % Player.escudo_frame_count
            escudo_image = Player.escudo_frames[frame_index]
            new_size = int(self.sprite_size)
            escudo_image_scaled = pygame.transform.smoothscale(escudo_image, (new_size, new_size))

            # Crear y dibujar la copia de DELANTE con 30% de opacidad
            escudo_overlay = escudo_image_scaled.copy()
            escudo_overlay.set_alpha(int(255 * 0.30))  # 30% Opacidad
            escudo_rect_front = escudo_overlay.get_rect()
            escudo_rect_front.center = (
                self.x + self.sprite_size // 2,
                self.y + self.sprite_draw_offset_y + TOP_OFFSET + self.sprite_size // 2
            )
            screen.blit(escudo_overlay, escudo_rect_front)

        # --- FIN DE LA MODIFICACIÓN ---

        # 4) Efecto de parpadeo al expirar la maldición
        if self.flashing:
            flash_surf = pygame.Surface((self.sprite_size, self.sprite_size))
            flash_surf.fill(WHITE)
            flash_surf.set_alpha(180)
            screen.blit(flash_surf, (self.x, self.y + self.sprite_draw_offset_y + TOP_OFFSET))
            if time.time() - self.flash_timer >= 0.4:
                self.flash_timer = time.time()
                self.flash_count -= 1
                if self.flash_count <= 0:
                    self.flashing = False

    def place_bomb(self, bombs, powerups, grid, lapidas, forced=False):
        # SI ES FANTASMA, APLICA REGLAS ESPECIALES
        if self.is_ghost:
            current_time = time.time()
            # Comprobar si el cooldown ha terminado para poder poner una bomba
            if current_time - self.last_bomb_placed_time >= self.ghost_bomb_cooldown:
                cx = self.x + self.sprite_size // 2
                cy = self.y + self.sprite_size // 2
                bomb_tile_x = int(cx // TILE_SIZE)
                bomb_tile_y = int(cy // TILE_SIZE)

                # --- > INICIO DE LA MODIFICACIÓN <---

                # 1. RESTRICCIÓN: No colocar bomba sobre un bloque rompible (grid == 1)
                if grid[bomb_tile_y][bomb_tile_x] == 1:
                    return  # Salir de la función sin hacer nada

                # 2. RESTRICCIÓN: Comprobar si ya hay una bomba en esa casilla
                if any(b.tile_x == bomb_tile_x and b.tile_y == bomb_tile_y and not b.exploded for b in bombs):
                    return

                # 3. EFECTO: Hacer desaparecer cualquier gadget o lápida en la casilla
                for p in powerups[:]:
                    if p.visible and not p.disappearing and (p.x, p.y) == (bomb_tile_x, bomb_tile_y):
                        p.start_disappear()  # Inicia la animación para que el gadget se desvanezca

                for lapida in lapidas[:]:
                    if (lapida.tile_x, lapida.tile_y) == (bomb_tile_x, bomb_tile_y):
                        lapida.start_slow_fade()  # Inicia la animación para que la lápida se desvanezca

                # --- > FIN DE LA MODIFICACIÓN <---

                # Si pasa todas las comprobaciones, se crea la bomba
                new_bomb = Bomb(bomb_tile_x, bomb_tile_y, 1)  # La bomba del fantasma siempre tiene rango 1
                new_bomb.owner = self
                bombs.append(new_bomb)
                COLOCAR_BOMBA_SOUND.play()
                self.last_bomb_placed_time = current_time  # Actualiza el tiempo para iniciar el cooldown
            return  # Es importante que el fantasma termine su lógica aquí

        # --- Lógica para el jugador VIVO (sin cambios) ---
        if self.auto_bombing and not forced:
            return
        if not self.can_place_bombs and not forced:
            return
        if self.active_curse == "no_bomb":
            return
        if not forced:
            current_bombs = [b for b in bombs if b.owner == self and not b.exploded]
            if len(current_bombs) >= self.bomb_limit:
                return
        cx = self.x + self.sprite_size // 2
        cy = self.y + self.sprite_size // 2
        bomb_tile_x = int(cx // TILE_SIZE)
        bomb_tile_y = int(cy // TILE_SIZE)
        for b in bombs:
            if b.tile_x == bomb_tile_x and b.tile_y == bomb_tile_y and not b.exploded:
                return
        new_bomb = Bomb(bomb_tile_x, bomb_tile_y, self.bomb_range)
        new_bomb.owner = self
        new_bomb.passable_players.add(self)
        bombs.append(new_bomb)
        COLOCAR_BOMBA_SOUND.play()
        if self.active_curse == "no_ability":
            for p in powerups[:]:
                if p.visible and not p.disappearing and (p.x, p.y) == (bomb_tile_x, bomb_tile_y):
                    p.start_disappear()

    def _set_curse_effects(self, curse_name):
        if curse_name == "no_ability":
            self.can_pick_abilities = False
        elif curse_name == "no_bomb":
            self.can_place_bombs = False
        elif curse_name == "auto_bomb":
            self.auto_bombing = True

        elif curse_name == "inverted":
            # Generar permutación aleatoria de las cuatro direcciones
            dirs = ["up", "down", "left", "right"]
            perm = dirs.copy()
            random.shuffle(perm)
            # Asignar controles según permutación
            self.controls = {
                "up": self.original_controls[perm[0]],
                "down": self.original_controls[perm[1]],
                "left": self.original_controls[perm[2]],
                "right": self.original_controls[perm[3]],
                "bomb": self.original_controls["bomb"],
                "hit": self.original_controls["hit"],
            }

        elif curse_name == "hyper_speed":
            self.speed = 20
        elif curse_name == "slow_speed":
            self.speed = 0.5

    def _clear_curse_effects(self, curse_name):
        if curse_name == "no_ability":
            self.can_pick_abilities = True
        elif curse_name == "no_bomb":
            self.can_place_bombs = True
        elif curse_name == "auto_bomb":
            self.auto_bombing = False
        elif curse_name == "inverted":
            self.controls = self.original_controls.copy()
        elif curse_name in ("hyper_speed", "slow_speed"):
            original = getattr(self, "_saved_speed_before_curse", self.base_speed)
            self.speed = original + self.pending_speed_boosts
            self._saved_speed_before_curse = None
            self.pending_speed_boosts = 0

    def check_static_push(self, grid, bombs, players, powerups):
        if not self.push_bomb_available:
            return

        tile_x, tile_y = self.get_center_tile()

        direction_map = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }

        if self.current_direction not in direction_map:
            return

        dx, dy = direction_map[self.current_direction]
        target_x = tile_x + dx
        target_y = tile_y + dy

        if target_x < 0 or target_x >= GRID_COLS or target_y < 0 or target_y >= GRID_ROWS:
            return

        # Comprobamos si la casilla objetivo tiene una bomba
        for b in bombs:
            if b.tile_x == target_x and b.tile_y == target_y and not b.exploded:
                if not b.sliding:
                    b.try_start_push(dx, dy, grid, bombs, players, powerups)
                break

    def reset_for_new_set(self, init_tile_x, init_tile_y):
        """ Reinicia el estado del jugador para un nuevo set. """
        self.x = init_tile_x * TILE_SIZE - 40
        self.y = init_tile_y * TILE_SIZE - 40
        self.is_ghost = False
        self.is_eliminated = False
        self.is_set_winner = False

        self.is_invulnerable = True
        self.invulnerable_until = time.time() + self.invulnerable_duration
        self.invulnerable_flash_timer = time.time()

        self.bomb_range = 1
        self.bomb_limit = 1
        self.speed = self.base_speed
        self.display_speed = 1
        self.push_bomb_available = False
        self.hit_bomb_available = False
        self.escudo_available = False
        self.escudo_active = False
        self.pending_speed_boosts = 0

        if self.active_curse:
            self._clear_curse_effects(self.active_curse)
        self.active_curse = None
        self.curse_ends_at = None
        self.controls = self.original_controls.copy()

        self.current_direction = "right"
        self.anim_frame = 0
#--------------------------------------------------------------------------------
# Función para cargar animaciones de un personaje según su nombre
def cargar_animaciones_personaje(nombre_personaje):
    animaciones = {}
    for direccion in ["right", "left", "up", "down"]:
        carpeta = os.path.join(ASSETS_DIR, "Jugadores", nombre_personaje, direccion)
        imagenes = []
        for i in range(1, 8):
            img = load_image(f"{direccion}{i}.png", (120, 120), folder=carpeta)
            imagenes.append(img)
        animaciones[direccion] = imagenes
    return animaciones


def cargar_animacion_fantasma(player_index):
    """Carga los frames del GIF de fantasma para un jugador específico."""
    # Los GIFs están indexados a partir de 1, pero nuestro player_index empieza en 0
    gif_name = f"Jugador {player_index + 1}.gif"
    path = os.path.join(ASSETS_DIR, "Jugadores", "Fantasma muerto", f"Jugador {player_index + 1}", gif_name)

    # --- > PUEDES MODIFICAR ESTE VALOR PARA AJUSTAR EL TAMAÑO <---
    # 1.0 es el tamaño original, 0.7 es el 70%, 0.5 es el 50%, etc.
    GHOST_SCALE_FACTOR = 0.07

    if not os.path.exists(path):
        print(f"Advertencia: No se encontró el GIF del fantasma en {path}")
        return []

    try:
        from PIL import Image
        pil_image = Image.open(path)
        frames = []
        while True:
            # Convertimos cada frame del GIF a una superficie de Pygame
            frame = pil_image.convert("RGBA")
            pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)

            # --- > ESTA ES LA LÓGICA DE REESCALADO CORREGIDA <---
            # 1. Obtenemos el tamaño original del frame del GIF
            original_width, original_height = pygame_frame.get_size()

            # 2. Calculamos el nuevo tamaño usando el factor de escala
            new_width = int(original_width * GHOST_SCALE_FACTOR)
            new_height = int(original_height * GHOST_SCALE_FACTOR)

            # 3. Escalamos el frame al nuevo tamaño, manteniendo la proporción
            scaled_frame = pygame.transform.scale(pygame_frame, (new_width, new_height))

            frames.append(scaled_frame)
            pil_image.seek(pil_image.tell() + 1)

    except EOFError:
        pass  # Fin de los frames del GIF
    except ImportError:
        print("Error: La librería Pillow (PIL) es necesaria para cargar GIFs.")
        return []

    return frames

# Diccionario de nombres por índice desde la pantalla de personajes
nombres_por_indice = {
    0: "Mork",
    1: "Guerrero Rojo",
    2: "Mortis",
    3: "Grimfang",
    4: "Warlord",
    5: "Vael",
    6: "Sarthus",
    7: "Guerrero Azul",
    8: "Guerrero Blanco",
    9: "Guerrero Negro",
    10: "Calvo"
}


# ------------------------------------------------------------------------------------
# Clase Bomb (con modificación en explode para que la explosión se detenga en la maldición)
# ------------------------------------------------------------------------------------
class Bomb:
    def __init__(self, tile_x, tile_y, blast_range):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.blast_range = blast_range
        self.timer = 3
        self.plant_time = time.time()
        self.exploded = False
        self.passable_players = set()
        self.chain_triggered = False
        self.chain_trigger_time = None
        self.owner = None
        self.pos_x = self.tile_x * TILE_SIZE
        self.pos_y = self.tile_y * TILE_SIZE
        self.push_direction = None
        self.push_path = []
        self.push_index = 0
        self.push_timer = 0.0
        self.push_duration = 0.0
        self.push_speed = 0.0
        self.can_be_pushed = False
        self.sliding = False
        self.slide_start_x = 0
        self.slide_start_y = 0
        self.slide_target_x = 0
        self.slide_target_y = 0
        self.slide_duration = 0
        self.slide_elapsed = 0
        self.hit_bouncing = False
        self.hit_bounce_path = []
        self.hit_bounce_index = 0
        self.hit_bounce_start_time = 0
        self.hit_bounce_duration = 300  # ms por salto de casilla
        self.hit_bounce_height = 30  # Altura del arco en píxeles
        self.timer_frozen = False
        self.freeze_start_time = None

    def tile_blocked_for_bomb(self, grid, bombs, tx, ty):
        if tx < 0 or tx >= GRID_COLS or ty < 0 or ty >= GRID_ROWS:
            return True
        if grid[ty][tx] in (1, 2, 3):
            return True
        for b in bombs:
            if b is not self and not b.exploded:
                if b.tile_x == tx and b.tile_y == ty:
                    return True
        return False

    def center_of_tile(self, tx, ty):
        return (tx * TILE_SIZE + TILE_SIZE / 2,
                ty * TILE_SIZE + TILE_SIZE / 2)

    def start_sliding_to(self, next_tx, next_ty):
        self.sliding = True
        self.slide_elapsed = 0
        start_center = self.center_of_tile(self.tile_x, self.tile_y)
        self.slide_start_x = start_center[0]
        self.slide_start_y = start_center[1]
        target_center = self.center_of_tile(next_tx, next_ty)
        self.slide_target_x = target_center[0]
        self.slide_target_y = target_center[1]
        dist = math.hypot(self.slide_target_x - self.slide_start_x,
                          self.slide_target_y - self.slide_start_y)
        self.slide_duration = dist / PUSH_SPEED

    def update_sliding(self):
        if not self.sliding:
            return
        dt = 1
        self.slide_elapsed += dt
        if self.slide_elapsed >= self.slide_duration:
            self.slide_elapsed = self.slide_duration
            self.sliding = False
            dest_tx = int(self.slide_target_x // TILE_SIZE)
            dest_ty = int(self.slide_target_y // TILE_SIZE)
            self.tile_x = dest_tx
            self.tile_y = dest_ty
            self.pos_x = self.slide_target_x - TILE_SIZE / 2
            self.pos_y = self.slide_target_y - TILE_SIZE / 2
        else:
            ratio = self.slide_elapsed / self.slide_duration
            new_cx = (1 - ratio) * self.slide_start_x + ratio * self.slide_target_x
            new_cy = (1 - ratio) * self.slide_start_y + ratio * self.slide_target_y
            self.pos_x = new_cx - TILE_SIZE / 2
            self.pos_y = new_cy - TILE_SIZE / 2

    def update_push(self, grid, bombs):
        if self.sliding:
            self.update_sliding()
            if self.sliding:
                return
        if not self.push_direction:
            return
        while True:
            dx, dy = self.push_direction
            next_tx = self.tile_x + dx
            next_ty = self.tile_y + dy
            if self.tile_blocked_for_bomb(grid, bombs, next_tx, next_ty):
                self.push_direction = None
                return
            self.start_sliding_to(next_tx, next_ty)
            self.update_sliding()
            if self.sliding:
                break

    def draw(self, screen):
        self.update_push_slide()  # ← IMPORTANTE: actualiza animación de empuje continuo
        draw_x = self.pos_x
        draw_y = self.pos_y
        if self.chain_triggered:
            total_time = 0.75
            elapsed = time.time() - self.chain_trigger_time
        else:
            total_time = 3.0
            elapsed = time.time() - self.plant_time
        frame_time = total_time / 15.0
        frame_index = min(int(elapsed / frame_time), 14)
        bomb_image = BOMB_IMAGES[frame_index]
        base_scale = 1.4
        oscillation = 0.15 * math.sin(2 * math.pi * (elapsed / total_time))
        bomb_image_scaled = pygame.transform.scale(
            bomb_image,
            (int(bomb_image.get_width() * (base_scale + oscillation)),
             int(bomb_image.get_height() * (base_scale + oscillation)))
        )
        px = draw_x + (TILE_SIZE - bomb_image_scaled.get_width()) // 2
        py = draw_y + (TILE_SIZE - bomb_image_scaled.get_height()) // 2 + TOP_OFFSET
        screen.blit(bomb_image_scaled, (px, py))

    def explode(self, grid, players, bombs, powerups):
        if self.hit_bouncing:
            return []
        if self.exploded:
            return []
        self.exploded = True
        if self in bombs:
            bombs.remove(self)
        EXPLOSION_SOUND.play()

        # --- LÓGICA MODIFICADA PARA CREAR OBJETOS EXPLOSION CON DUEÑO ---
        explosions = [Explosion(self.tile_x, self.tile_y, "center", None, owner=self.owner)]
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        for dx, dy in directions:
            for i in range(1, self.blast_range + 1):
                nx = self.tile_x + dx * i
                ny = self.tile_y + dy * i

                if not (0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS):
                    break
                if grid[ny][nx] == 1:
                    if (nx, ny) not in exploding_blocks:
                        exploding_blocks[(nx, ny)] = time.time()
                        reveal_powerup_if_any(powerups, nx, ny)
                    break
                if grid[ny][nx] in (2, 3):
                    break

                bomb_found = next((b for b in bombs if b.tile_x == nx and b.tile_y == ny and not b.exploded), None)
                if bomb_found is not None:
                    if not bomb_found.chain_triggered:
                        bomb_found.chain_triggered = True
                        bomb_found.chain_trigger_time = time.time()
                    break

                found_powerup = False
                for p in powerups:
                    if p.x == nx and p.y == ny and p.visible and not p.disappearing:
                        if p.type == "calavera":
                            p.visible = True
                            p.start_bounce((dx, dy), grid, bombs, powerups)
                        else:
                            p.start_disappear()
                            explosions.append(Explosion(nx, ny, "ability", (dx, dy), owner=self.owner))
                        found_powerup = True
                        break
                if found_powerup:
                    break

                # Añadimos la explosión como un objeto completo con su dueño
                if i == self.blast_range:
                    explosions.append(Explosion(nx, ny, "extreme", (dx, dy), owner=self.owner))
                else:
                    explosions.append(Explosion(nx, ny, "lateral", (dx, dy), owner=self.owner))

        return explosions

    def hit_by_player(self, dx, dy, grid, bombs, powerups, players, bounce_length=3):
        import math

        # Obtén la celda de partida y su centro en píxeles
        start_tile = (self.tile_x, self.tile_y)
        start_center = (
            start_tile[0] * TILE_SIZE + TILE_SIZE / 2,
            start_tile[1] * TILE_SIZE + TILE_SIZE / 2
        )

        per_cell_duration = 150  # ms por casilla (valor base para calcular el tiempo)
        path_tiles = [start_tile]

        # Primer salto: se intenta saltar 3 casillas de un solo bote
        intended_tile = (
            (start_tile[0] + dx * bounce_length) % GRID_COLS,
            (start_tile[1] + dy * bounce_length) % GRID_ROWS
        )
        path_tiles.append(intended_tile)

        # Función para determinar si una celda está libre:
        def cell_free(tile, bombs, powerups):
            tx, ty = tile
            # Si es un muro o bloque inamovible:
            if grid[ty][tx] in (1, 2, 3):
                return False
            # Si hay alguna bomba activa (que no sea self) en esa celda:
            for bomb in bombs:
                if bomb is not self and not bomb.exploded:
                    if bomb.tile_x == tx and bomb.tile_y == ty:
                        return False
            # Si hay alguna maldición (powerup de tipo CURSE) visible bloqueante:
            for p in powerups:
                if p.x == tx and p.y == ty and p.visible and p.type in CURSES:
                    return False
            return True

        # Si la casilla destino del salto de 3 casillas no está libre, encadena saltos de 1 celda
        if not cell_free(intended_tile, bombs, powerups):
            current = intended_tile
            while not cell_free(current, bombs, powerups):
                next_tile = ((current[0] + dx) % GRID_COLS, (current[1] + dy) % GRID_ROWS)
                path_tiles.append(next_tile)
                current = next_tile

        # Convertir la secuencia de celdas a coordenadas en píxeles (centrando la posición de cada celda)
        pixel_path = [
            (t[0] * TILE_SIZE + TILE_SIZE / 2, t[1] * TILE_SIZE + TILE_SIZE / 2)
            for t in path_tiles
        ]

        # Cálculo de la duración para cada segmento basándose en la distancia real recorrida (con wrap-around)
        duration_list = []
        total_time = 0
        for i in range(len(pixel_path) - 1):
            p1 = pixel_path[i]
            p2 = pixel_path[i + 1]

            dx_px = p2[0] - p1[0]
            dy_px = p2[1] - p1[1]

            # Ajuste horizontal para wrap-around
            map_width_px = GRID_COLS * TILE_SIZE
            if abs(dx_px) > map_width_px / 2:
                if dx_px > 0:
                    dx_px -= map_width_px
                else:
                    dx_px += map_width_px

            # Ajuste vertical para wrap-around
            map_height_px = GRID_ROWS * TILE_SIZE
            if abs(dy_px) > map_height_px / 2:
                if dy_px > 0:
                    dy_px -= map_height_px
                else:
                    dy_px += map_height_px

            dist_segment = math.hypot(dx_px, dy_px)
            # La duración se calcula proporcional a la distancia recorrida; por ejemplo:
            time_segment = (dist_segment / TILE_SIZE) * per_cell_duration
            duration_list.append(time_segment)
            total_time += time_segment

        # Configura los parámetros para que update_hit_bounce realice la interpolación continua.
        self.hit_bouncing = True
        self.hit_bounce_pixel_path = pixel_path
        self.hit_bounce_durations = duration_list
        self.hit_bounce_total_time = total_time
        self.hit_bounce_start_time = pygame.time.get_ticks()
        self.hit_bounce_height = 15  # Ajusta la altura del arco del salto si lo deseas

        # Congela el temporizador de la bomba hasta que finalice la animación
        self.timer_frozen = True
        self.freeze_start_time = time.time()

    def update_hit_bounce(self, grid, players, bombs, powerups):
        import math

        if not self.hit_bouncing:
            return

        now = pygame.time.get_ticks()
        elapsed = now - self.hit_bounce_start_time

        # Si la animación ya terminó, fijamos la bomba en la última celda
        if elapsed >= self.hit_bounce_total_time:
            final_point = self.hit_bounce_pixel_path[-1]
            self.pos_x = final_point[0] - TILE_SIZE / 2
            self.pos_y = final_point[1] - TILE_SIZE / 2
            self.tile_x = int(final_point[0] // TILE_SIZE)
            self.tile_y = int(final_point[1] // TILE_SIZE)
            self.hit_bouncing = False

            # Reanudamos el temporizador de la bomba (pausado)
            if self.timer_frozen:
                freeze_time = time.time() - self.freeze_start_time
                self.plant_time += freeze_time
                self.timer_frozen = False

                # Verificamos si ha caído sobre una calavera o poder
                for p in powerups:
                    if p.x == self.tile_x and p.y == self.tile_y and p.visible and not p.disappearing:
                        if p.type == "calavera":
                            # Obtenemos la dirección del último movimiento
                            last_point_index = max(0, len(self.hit_bounce_pixel_path) - 2)
                            dx = self.tile_x - int(self.hit_bounce_pixel_path[last_point_index][0] // TILE_SIZE)
                            dy = self.tile_y - int(self.hit_bounce_pixel_path[last_point_index][1] // TILE_SIZE)

                            # Normalizamos la dirección para asegurar que sea (1,0), (-1,0), (0,1) o (0,-1)
                            if dx != 0: dx = 1 if dx > 0 else -1
                            if dy != 0: dy = 1 if dy > 0 else -1

                            # Inicia un nuevo rebote de una sola casilla
                            self.hit_by_player(dx, dy, grid, bombs, powerups, bounce_length=1)
                            return  # Salimos para que la nueva animación de rebote tome el control
                        else:
                            # Si es una habilidad, desaparecer inmediatamente
                            p.start_disappear()
                return

        # Determina en qué tramo de la ruta nos encontramos según el tiempo transcurrido
        t_accum = 0
        segment_index = 0
        for i, dur in enumerate(self.hit_bounce_durations):
            if elapsed < t_accum + dur:
                segment_index = i
                break
            t_accum += dur

        # Progreso dentro del tramo actual (entre 0 y 1)
        segment_elapsed = elapsed - t_accum
        segment_duration = self.hit_bounce_durations[segment_index]
        t_seg = max(0, min(1, segment_elapsed / segment_duration))

        # Calcula la posición de inicio y fin (en píxeles) para este tramo
        p_start = self.hit_bounce_pixel_path[segment_index]
        p_end = self.hit_bounce_pixel_path[segment_index + 1]

        dx_px = p_end[0] - p_start[0]
        dy_px = p_end[1] - p_start[1]
        map_width_px = GRID_COLS * TILE_SIZE
        map_height_px = GRID_ROWS * TILE_SIZE

        if abs(dx_px) > map_width_px / 2:
            dx_px += -map_width_px if dx_px > 0 else map_width_px
        if abs(dy_px) > map_height_px / 2:
            dy_px += -map_height_px if dy_px > 0 else map_height_px

        interp_x = p_start[0] + dx_px * t_seg
        interp_y = p_start[1] + dy_px * t_seg

        arc = -self.hit_bounce_height * math.sin(math.pi * t_seg)
        interp_y += arc

        self.pos_x = interp_x - TILE_SIZE / 2
        self.pos_y = interp_y - TILE_SIZE / 2

    def try_start_push(self, dx, dy, grid, bombs, players, powerups):
        if self.sliding:
            return
        path = []
        cx, cy = self.tile_x, self.tile_y
        while True:
            nx, ny = cx + dx, cy + dy
            # Condición de parada 1: bloque
            if nx < 0 or nx >= GRID_COLS or ny < 0 or ny >= GRID_ROWS:
                break
            if grid[ny][nx] in (1, 2, 3):
                break
            # Condición de parada 2: otra bomba
            if any(b.tile_x == nx and b.tile_y == ny and not b.exploded and b != self for b in bombs):
                break
            # Condición de parada 3: powerup/maldición
            if any(p.x == nx and p.y == ny and p.visible for p in powerups):
                break
            # Condición de parada 4: jugador ocupando >25%
            for p in players:
                rect = p.get_hitbox()
                tx = nx * TILE_SIZE
                ty = ny * TILE_SIZE
                tile_rect = pygame.Rect(tx, ty, TILE_SIZE, TILE_SIZE)
                inter = tile_rect.clip(rect)
                if inter.width * inter.height >= (TILE_SIZE * TILE_SIZE * 0.25):
                    break
            else:
                path.append((nx, ny))
                cx, cy = nx, ny
                continue
            break

        if path:
            self.push_path = [(self.tile_x, self.tile_y)] + path
            self.sliding = True
            self.push_index = 0
            self.push_speed = 10 * TILE_SIZE  # píxeles por segundo
            self.push_timer = 0
            self.push_duration = TILE_SIZE / self.push_speed
            self.set_tile_pos(*self.push_path[0])

    def update_push_slide(self):
        if not self.sliding or not self.push_path:
            return
        self.push_timer += 1 / 60
        if self.push_timer >= self.push_duration:
            self.push_timer -= self.push_duration
            self.push_index += 1
            if self.push_index >= len(self.push_path):
                self.sliding = False
                return
            self.set_tile_pos(*self.push_path[self.push_index])

        if self.push_index + 1 < len(self.push_path):
            sx, sy = self.push_path[self.push_index]
            dx, dy = self.push_path[self.push_index + 1]
            prog = self.push_timer / self.push_duration
            px = (sx * (1 - prog) + dx * prog) * TILE_SIZE
            py = (sy * (1 - prog) + dy * prog) * TILE_SIZE
            self.pos_x = px
            self.pos_y = py

    def set_tile_pos(self, tx, ty):
        self.tile_x = tx
        self.tile_y = ty
        self.pos_x = tx * TILE_SIZE
        self.pos_y = ty * TILE_SIZE


# ------------------------------------------------------------------------------------
# Clase Explosion (sin cambios)
# ------------------------------------------------------------------------------------
class Explosion:
    def __init__(self, tile_x, tile_y, explosion_type="normal", direction=None, owner=None):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.explosion_type = explosion_type
        self.direction = direction
        self.owner = owner
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.finished = False
        if explosion_type == "center":
            self.frames = CENTER_EXPLOSION_FRAMES
            TOTAL_EXPLOSION_TIME = 0.3
            self.frame_duration = TOTAL_EXPLOSION_TIME / len(self.frames)
            self.rotation_angle = 0
        elif explosion_type == "extreme":
            self.frames = EXTREME_EXPLOSION_FRAMES
            TOTAL_EXPLOSION_TIME = 0.3
            self.frame_duration = TOTAL_EXPLOSION_TIME / len(self.frames)
            if direction == (1, 0):
                self.rotation_angle = 90
            elif direction == (0, 1):
                self.rotation_angle = 180
            elif direction == (-1, 0):
                self.rotation_angle = 270
            else:
                self.rotation_angle = 0
        elif explosion_type == "lateral":
            self.frames = LATERAL_EXPLOSION_FRAMES
            TOTAL_EXPLOSION_TIME = 0.3
            self.frame_duration = TOTAL_EXPLOSION_TIME / len(self.frames)
            if direction == (1, 0):
                self.rotation_angle = 90
            elif direction == (0, 1):
                self.rotation_angle = 180
            elif direction == (-1, 0):
                self.rotation_angle = 270
            else:
                self.rotation_angle = 0
        elif explosion_type == "ability":
            self.frames = ABILITY_EXPLOSION_FRAMES
            TOTAL_EXPLOSION_TIME = 0.85
            self.frame_duration = TOTAL_EXPLOSION_TIME / len(self.frames)
            self.rotation_angle = 0
        else:
            self.frames = EXPLOSION_FRAMES
            self.frame_duration = 0.1
            self.rotation_angle = 0

    def update(self):
        now = pygame.time.get_ticks()
        if not self.finished and (now - self.last_update > self.frame_duration * 1000):
            self.current_frame += 1
            self.last_update = now
            if self.current_frame >= len(self.frames):
                self.finished = True

    def draw(self, screen):
        if not self.finished:
            px = self.tile_x * TILE_SIZE
            py = self.tile_y * TILE_SIZE + TOP_OFFSET

            frame_data = self.frames[self.current_frame]

            # --- INICIO DE LA CORRECCIÓN ---
            # Comprobamos si el frame es un diccionario o una imagen directa
            if isinstance(frame_data, dict):
                frame_image = frame_data.get("image")
            else:
                frame_image = frame_data  # Es directamente una Surface

            # Si por alguna razón no se encuentra la imagen, no hacemos nada para evitar un error.
            if frame_image is None:
                return
            # --- FIN DE LA CORRECCIÓN ---

            self.current_sprite = frame_data  # guardamos también el nombre para detección

            if self.explosion_type in ("extreme", "lateral") and self.rotation_angle != 0:
                frame_image = pygame.transform.rotate(frame_image, -self.rotation_angle)

            screen.blit(frame_image, (px, py))

# ------------------------------------------------------------------------------------
# Clase Lapida
# ------------------------------------------------------------------------------------
class Lapida:
    def __init__(self, tile_x, tile_y, image):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.image = image
        self.creation_time = time.time()
        self.duration = 10.0  # Durará 10 segundos
        self.state = "active"  # Estados: active, fading
        self.fade_duration = 1.0  # Duración del desvanecimiento
        self.fade_start_time = 0
        self.alpha = 255

    def update(self):
        current_time = time.time()
        # Si han pasado los 10 segundos, empieza a desvanecerse
        if self.state == "active" and current_time - self.creation_time > self.duration:
            self.state = "fading"
            self.fade_start_time = current_time

        # Lógica de la animación de desvanecimiento
        if self.state == "fading":
            elapsed_fade = current_time - self.fade_start_time
            if elapsed_fade >= self.fade_duration:
                self.alpha = 0
            else:
                self.alpha = 255 * (1 - (elapsed_fade / self.fade_duration))

    def is_finished(self):
        return self.alpha <= 0

    def draw(self, screen):
        if self.alpha > 0:
            temp_image = self.image.copy()
            temp_image.set_alpha(self.alpha)
            screen.blit(temp_image, (self.tile_x * TILE_SIZE, self.tile_y * TILE_SIZE + TOP_OFFSET))

    def start_slow_fade(self):
        self.state = "fading"
        self.fade_start_time = time.time()
        self.fade_duration = 3.0  # ← duración más lenta al contagiar


# ------------------------------------------------------------------------------------
# Clase DroppedAbility (sin cambios)
# ------------------------------------------------------------------------------------
class DroppedAbility:
    def __init__(self, start_pos, image, target_cell, ability_type):
        self.start_x, self.start_y = start_pos
        self.image = image
        self.target_cell = target_cell
        self.ability_type = ability_type
        self.target_pos = (
            target_cell[0] * TILE_SIZE + TILE_SIZE // 2,
            target_cell[1] * TILE_SIZE + TILE_SIZE // 2 + TOP_OFFSET
        )
        self.current_pos = start_pos
        self.elapsed = 0
        self.duration = 1.5
        self.growth_duration = 0.5
        self.completed = False
        self.dropped = False

    # REEMPLAZA TU MÉTODO 'update' ACTUAL CON ESTE:
    def update(self, dt, grid, powerups):
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.current_pos = self.target_pos
            self.completed = True
            if not self.dropped:
                available = get_available_free_cells(grid, powerups)
                if self.target_cell not in available:
                    if available:
                        self.target_cell = random.choice(available)
                        self.target_pos = (
                            self.target_cell[0] * TILE_SIZE + TILE_SIZE // 2,
                            self.target_cell[1] * TILE_SIZE + TILE_SIZE // 2 + TOP_OFFSET
                        )
                new_powerup = PowerUp(self.target_cell[0], self.target_cell[1], self.ability_type)
                new_powerup.visible = True
                powerups.append(new_powerup)
                self.dropped = True
            return
        if self.elapsed < self.growth_duration:
            offset = -10 * (self.elapsed / self.growth_duration)
            self.current_pos = (self.start_x, self.start_y + offset)
        else:
            t = (self.elapsed - self.growth_duration) / (self.duration - self.growth_duration)
            start_after_growth = (self.start_x, self.start_y - 10)
            new_x = start_after_growth[0] + (self.target_pos[0] - start_after_growth[0]) * t
            new_y = start_after_growth[1] + (self.target_pos[1] - start_after_growth[1]) * (t ** 2)
            self.current_pos = (new_x, new_y)

    def draw(self, screen):
        rect = self.image.get_rect(center=self.current_pos)
        screen.blit(self.image, rect)


# ------------------------------------------------------------------------------------
# Funciones auxiliares para celdas libres
# ------------------------------------------------------------------------------------
def get_available_free_cells(grid, powerups):
    cells = []
    for y in range(1, GRID_ROWS - 1):
        for x in range(1, GRID_COLS - 1):
            if grid[y][x] == 0:
                if not any(p.x == x and p.y == y and p.visible for p in powerups):
                    cells.append((x, y))
    return cells


def get_free_cells(grid):
    cells = []
    for y in range(1, GRID_ROWS - 1):
        for x in range(1, GRID_COLS - 1):
            if grid[y][x] == 0:
                cells.append((x, y))
    return cells


def find_free_cell_far_from(player, grid):
    player_tile = player.get_center_tile()
    free_cells = get_free_cells(grid)
    if free_cells:
        far_cell = max(free_cells, key=lambda cell: math.hypot(cell[0] - player_tile[0], cell[1] - player_tile[1]))
        return far_cell
    return player_tile


dropped_abilities = []


# ------------------------------------------------------------------------------------
# Función generate_grid_and_powerups
# ------------------------------------------------------------------------------------
# REEMPLAZA TU FUNCIÓN 'check_pickup' con esta versión:
def check_pickup(players, powerups, lapidas):
    powerups_to_remove = []

    for p in powerups:
        if not (p.visible and not p.disappearing and not p.bouncing):
            continue

        # Coordenadas del juego (SIN TOP_OFFSET)
        powerup_rect = pygame.Rect(p.x * TILE_SIZE, p.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        for player in players:
            if player.is_ghost or not player.can_pick_abilities:
                continue

            player_hitbox = player.get_hitbox()

            if player_hitbox.colliderect(powerup_rect):
                if p.type in CURSES:
                    COGER_MALDICION_SOUND.play()
                    curse_to_apply = random.choice(list(CURSES.keys()))
                    player.apply_curse(curse_to_apply)
                else:
                    COGER_HABILIDAD_SOUND.play()
                    if p.type == "speed":
                        # Lógica de velocidad corregida (como en tu original)
                        player.base_speed += 1.0
                        player.speed = player.base_speed
                        player.display_speed += 1
                    elif p.type == "more_bomb":
                        player.bomb_limit += 1
                    elif p.type == "major_explosion":
                        player.bomb_range += 1
                    elif p.type == "push_bomb":
                        player.push_bomb_available = True
                    elif p.type == "golpear_bombas":
                        player.hit_bomb_available = True
                    elif p.type == "escudo":
                        player.escudo_available = True

                powerups_to_remove.append(p)
                break

    for item in powerups_to_remove:
        if item in powerups:
            powerups.remove(item)

    for lapida in lapidas:
        if lapida.state != "active":
            continue

        lapida_rect = pygame.Rect(lapida.tile_x * TILE_SIZE, lapida.tile_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        for player in players:
            if player.is_ghost:
                continue
            if player.get_hitbox().colliderect(lapida_rect):
                COGER_MALDICION_SOUND.play()
                curse_name = random.choice(list(CURSES.keys()))
                player.apply_curse(curse_name)
                lapida.start_slow_fade()
                break

def generate_grid_and_powerups():
    grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    powerups = []
    for x in range(GRID_COLS):
        grid[0][x] = 3
        grid[GRID_ROWS - 1][x] = 3
    for y in range(GRID_ROWS):
        grid[y][0] = 3
        grid[y][GRID_COLS - 1] = 3
    for y in range(1, GRID_ROWS - 1):
        for x in range(1, GRID_COLS - 1):
            grid[y][x] = 0
    for y in range(1, GRID_ROWS - 1):
        for x in range(1, GRID_COLS - 1):
            if (x % 2 == 0) and (y % 2 == 0):
                grid[y][x] = 2
    for y in range(1, GRID_ROWS - 1):
        for x in range(1, GRID_COLS - 1):
            if grid[y][x] == 0:
                if random.random() < 0.7:
                    grid[y][x] = 1
                    r = random.random()
                    if r < 0.1:
                        powerups.append(PowerUp(x, y, "speed"))
                    elif r < 0.3:
                        powerups.append(PowerUp(x, y, "major_explosion"))
                    elif r < 0.4:
                        powerups.append(PowerUp(x, y, "more_bomb"))
                    elif r < 0.45:
                        if config.current_ultimas_index.get("Maldiciones", 0) == 0:
                            powerups.append(PowerUp(x, y, "calavera"))
                    elif r < 0.45:
                        powerups.append(PowerUp(x, y, "reset"))
                    elif r < 0.5:
                        # Dividimos aleatoriamente entre "push_bomb", "golpear_bombas" y "escudo"
                        power_choice = random.choice(["push_bomb", "golpear_bombas", "escudo"])
                        powerups.append(PowerUp(x, y, power_choice))
    if grid[1][1] != 2:
        grid[1][1] = 0
    if grid[1][2] != 2:
        grid[1][2] = 0
    if grid[2][1] != 2:
        grid[2][1] = 0
    if grid[2][2] != 2:
        grid[2][2] = 1
    if grid[1][GRID_COLS - 2] != 2:
        grid[1][GRID_COLS - 2] = 0
    if grid[1][GRID_COLS - 3] != 2:
        grid[1][GRID_COLS - 3] = 0
    if grid[2][GRID_COLS - 2] != 2:
        grid[2][GRID_COLS - 2] = 0
    if grid[2][GRID_COLS - 3] != 2:
        grid[2][GRID_COLS - 3] = 1
    if grid[GRID_ROWS - 2][1] != 2:
        grid[GRID_ROWS - 2][1] = 0
    if grid[GRID_ROWS - 2][2] != 2:
        grid[GRID_ROWS - 2][2] = 0
    if grid[GRID_ROWS - 3][1] != 2:
        grid[GRID_ROWS - 3][1] = 0
    if grid[GRID_ROWS - 3][2] != 2:
        grid[GRID_ROWS - 3][2] = 1
    if grid[GRID_ROWS - 2][GRID_COLS - 2] != 2:
        grid[GRID_ROWS - 2][GRID_COLS - 2] = 0
    if grid[GRID_ROWS - 2][GRID_COLS - 3] != 2:
        grid[GRID_ROWS - 2][GRID_COLS - 3] = 0
    if grid[GRID_ROWS - 3][GRID_COLS - 2] != 2:
        grid[GRID_ROWS - 3][GRID_COLS - 2] = 0
    if grid[GRID_ROWS - 3][GRID_COLS - 3] != 2:
        grid[GRID_ROWS - 3][GRID_COLS - 3] = 1
    forced_bricks = [(4, 1), (3, 2), (2, 3), (1, 4),
                     (4, 15), (3, 14), (2, 13), (1, 12),
                     (19, 4), (18, 3), (17, 2), (16, 1),
                     (16, 15), (17, 14), (18, 13), (19, 12)]
    for (fx, fy) in forced_bricks:
        grid[fy][fx] = 1
    return grid, powerups


def draw_grid(screen, grid, SUELO1, SUELO2, STONE, BRICK, LIMIT_IMG):
    current_time = time.time()
    # Dibujar el suelo en todas las casillas de forma alternada
    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + TOP_OFFSET, TILE_SIZE, TILE_SIZE)
            if (x + y) % 2 == 0:
                screen.blit(SUELO1, rect)
            else:
                screen.blit(SUELO2, rect)
    # Dibujar los elementos del grid por encima
    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + TOP_OFFSET, TILE_SIZE, TILE_SIZE)
            if grid[y][x] == 1:
                if (x, y) in exploding_blocks:
                    elapsed = current_time - exploding_blocks[(x, y)]
                    if elapsed < EXPLOSION_DURATION:
                        temp = BRICK.copy()
                        temp.fill((255, 165, 0), special_flags=pygame.BLEND_RGB_MULT)
                        alpha = int(255 * (1 - (elapsed / EXPLOSION_DURATION)))
                        temp.set_alpha(alpha)
                        screen.blit(temp, rect)
                    else:
                        grid[y][x] = 0
                        del exploding_blocks[(x, y)]
                        # No se dibuja nada, ya se ve el suelo debajo
                else:
                    screen.blit(BRICK, rect)
            elif grid[y][x] == 2:
                screen.blit(STONE, rect)
            elif grid[y][x] == 3:
                screen.blit(LIMIT_IMG, rect)


def draw_grid_lines(screen):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    line_color = (0, 0, 0, 80)
    for row in range(GRID_ROWS + 1):
        start = (0, row * TILE_SIZE + TOP_OFFSET)
        end = (WIDTH, row * TILE_SIZE + TOP_OFFSET)
        pygame.draw.line(overlay, line_color, start, end, 1)
    for col in range(GRID_COLS + 1):
        start = (col * TILE_SIZE, TOP_OFFSET)
        end = (col * TILE_SIZE, GRID_ROWS * TILE_SIZE + TOP_OFFSET)
        pygame.draw.line(overlay, line_color, start, end, 1)
    screen.blit(overlay, (0, 0))


def draw_curse_info(screen, player, color, pos):
    x, y = pos
    if getattr(player, 'active_curse', None) and getattr(player, 'curse_ends_at', None):
        duration = CURSES[player.active_curse]['duration']
        if duration is not None:
            remaining = max(0, int(player.curse_ends_at - time.time()))
            text = f"{player.active_curse}: {remaining}s"
        else:
            text = "No curse"
    else:
        text = "No curse"
    screen.blit(font.render(text, True, color), (x, y))


# CONDICION POSICION FIJA O ALEATORIA
def obtener_posiciones_aleatorias(num_players):
    # Esquinas interiores seguras (no borde del mapa)
    esquinas = [
        (1, 1),
        (GRID_COLS - 2, GRID_ROWS - 2),
        (1, GRID_ROWS - 2),
        (GRID_COLS - 2, 1),
    ]
    random.shuffle(esquinas)
    return esquinas[:num_players]


# Obtener el modo desde la configuración
modo_posicion = config.current_position_index  # 0 = fija, 1 = aleatoria

# ------------------------------------------------------------------------------------
# Bucle principal
# ------------------------------------------------------------------------------------
def iniciar_partida(screen):

    # dimensiones de pantalla partida
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # cargamos la musica de fondo
    MUSIC_PATH = os.path.join(ASSETS_DIR, "Sonidos_juego", "musica_fondo", "juego.mp3")
    pygame.mixer.music.load(MUSIC_PATH)
    pygame.mixer.music.set_volume(audio.volume)
    pygame.mixer.music.play(-1)

    global players
    # Creamos la lista de jugadores
    players = []
    color_pool = [RED, BLUE, (0, 255, 0), (255, 255, 0)]  # Colores para 4 jugadores

    for idx, jugador in enumerate(gestor_jugadores.todos()):
        if idx >= len(posiciones_iniciales):
            break  # Solo se admiten hasta 4 jugadores actualmente

        tipo = jugador.get("tipo")
        personaje_idx = jugador.get("indice", 0)
        tile_x, tile_y = posiciones_iniciales[idx]
        color = color_pool[idx % len(color_pool)]

        if tipo == "teclado":
            controls = controles_teclado
        elif tipo == "mando":
            controls = {"instance_id": jugador["instance_id"]}

        else:
            continue  # No válido

        nombre_personaje = nombres_por_indice.get(personaje_idx, "red")
        animaciones = cargar_animaciones_personaje(nombre_personaje)

        nuevo_jugador = Player(tile_x, tile_y, color, controls)
        nuevo_jugador.animaciones = animaciones
        nuevo_jugador.player_index = idx
        nuevo_jugador.ghost_anim_frames = cargar_animacion_fantasma(idx)
        players.append(nuevo_jugador)

    # Declaramos como globales las variables de estado para que sean accesibles desde todos los métodos
    global grid, powerups, bombs, explosions, lapidas, lapida_por_colocar, exploding_blocks, dropped_abilities

    # --- CONFIGURACIÓN DE LA PARTIDA ---
    sets_to_win = config.set_options[config.current_set_index]
    usar_fantasmas = config.current_ultimas_index.get("Fantasmas", 0) == 0
    SUELO1, SUELO2, STONE, BRICK, LIMIT_IMG = cargar_mapa()

    for p in players:
        p.sets_won = 0

    # --- BUCLE DE LA PARTIDA (GESTIONA LOS SETS) ---
    match_running = True
    while match_running:
        # --- REINICIO PARA UN NUEVO SET ---
        grid, powerups = generate_grid_and_powerups()
        bombs, explosions, lapidas, dropped_abilities = [], [], [], []
        lapida_por_colocar = None
        exploding_blocks = {}

        if config.current_position_index == 1:
            set_positions = obtener_posiciones_aleatorias(len(players))
        else:
            set_positions = posiciones_iniciales[:len(players)]

        for i, player in enumerate(players):
            x, y = set_positions[i]
            player.reset_for_new_set(x, y)

        start_time = time.time()
        TOTAL_TIME = config.current_minute * 60
        set_winner = None
        set_end_sequence_start_time = None
        clock = pygame.time.Clock()

        # --- BUCLE DEL SET ---
        set_running = True
        while set_running:
            dt = clock.tick(60) / 1000.0

            # --- MANEJO DE EVENTOS ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    resultado = menu_pausa(screen, "teclado", screen.copy())
                    if resultado == "Salir de la partida": return
                if event.type == pygame.JOYBUTTONDOWN and event.button in (7,9):
                    resultado = menu_pausa(screen, event.instance_id, screen.copy())
                    if resultado == "Salir de la partida": return

                if not set_end_sequence_start_time:
                    if event.type == pygame.KEYDOWN:
                        for player in players:
                            if "up" in player.controls and event.key == pygame.K_o: player.activate_escudo()
                            if 'bomb' in player.controls and event.key == player.controls['bomb']:
                                player.place_bomb(bombs, powerups, grid, lapidas)
                            elif 'hit' in player.controls and event.key == player.controls['hit']:
                                if player.hit_bomb_available:
                                    dx, dy = (0, -1) if player.current_direction == "up" else (
                                    0, 1) if player.current_direction == "down" else (
                                    -1, 0) if player.current_direction == "left" else (1, 0)
                                    front_tile_x, front_tile_y = player.get_center_tile()[0] + dx, \
                                                                 player.get_center_tile()[1] + dy
                                    for b in bombs:
                                        if b.tile_x == front_tile_x and b.tile_y == front_tile_y and not b.hit_bouncing and not b.sliding:
                                            b.hit_by_player(dx, dy, grid, bombs, powerups, players)
                                            break
                    elif event.type == pygame.JOYBUTTONDOWN:
                        for player in players:
                            if 'instance_id' in player.controls and getattr(event, "instance_id", event.joy) == \
                                    player.controls['instance_id']:
                                if event.button == 0:
                                    player.place_bomb(bombs, powerups, grid, lapidas)
                                elif event.button == 1 and player.hit_bomb_available:
                                    dx, dy = (0, -1) if player.current_direction == "up" else (
                                    0, 1) if player.current_direction == "down" else (
                                    -1, 0) if player.current_direction == "left" else (1, 0)
                                    front_tile_x, front_tile_y = player.get_center_tile()[0] + dx, \
                                                                 player.get_center_tile()[1] + dy
                                    for b in bombs:
                                        if b.tile_x == front_tile_x and b.tile_y == front_tile_y and not b.hit_bouncing and not b.sliding:
                                            b.hit_by_player(dx, dy, grid, bombs, powerups, players)
                                            break
                                elif event.button == 2:
                                    player.activate_escudo()

            # --- ACTUALIZACIÓN DE ESTADO ---
            keys = pygame.key.get_pressed()
            player_list_to_update = [set_winner] if set_end_sequence_start_time and set_winner else players
            for player in player_list_to_update:
                if set_end_sequence_start_time and player != set_winner: continue
                if player.is_eliminated: continue
                if player.is_invulnerable and time.time() > player.invulnerable_until: player.is_invulnerable = False

                if 'up' in player.controls:
                    if keys[player.controls['up']]:
                        player.move_up(grid, bombs, powerups, lapidas)
                    elif keys[player.controls['down']]:
                        player.move_down(grid, bombs, powerups, lapidas)
                    elif keys[player.controls['left']]:
                        player.move_left(grid, bombs, powerups, lapidas)
                    elif keys[player.controls['right']]:
                        player.move_right(grid, bombs, powerups, lapidas)
                elif "instance_id" in player.controls and player.controls.get("active", True):
                    joy = get_joystick_by_instance_id(player.controls["instance_id"])
                    if joy:
                        dx, dy, hat_x, hat_y = joy.get_axis(0), joy.get_axis(1), joy.get_hat(0)[0], joy.get_hat(0)[1]
                        if hat_x == -1:
                            player.move_left(grid, bombs, powerups, lapidas)
                        elif hat_x == 1:
                            player.move_right(grid, bombs, powerups, lapidas)
                        elif hat_y == 1:
                            player.move_up(grid, bombs, powerups, lapidas)
                        elif hat_y == -1:
                            player.move_down(grid, bombs, powerups, lapidas)
                        elif abs(dx) > 0.3 or abs(dy) > 0.3:
                            if abs(dx) > abs(dy):
                                if dx > 0.3:
                                    player.move_right(grid, bombs, powerups, lapidas)
                                else:
                                    player.move_left(grid, bombs, powerups, lapidas)
                            else:
                                if dy > 0.3:
                                    player.move_down(grid, bombs, powerups, lapidas)
                                else:
                                    player.move_up(grid, bombs, powerups, lapidas)

                player.update_animation()
                if not set_end_sequence_start_time:
                    player.update_passable(bombs)
                    player.update_curse()
                    player.update_escudo()

            for bomb in bombs[:]:
                bomb.update_push_slide()
                bomb.update_hit_bounce(grid, players, bombs, powerups)
                if not bomb.exploded and time.time() - bomb.plant_time >= bomb.timer and not bomb.timer_frozen:
                    explosions.extend(bomb.explode(grid, players, bombs, powerups))

            # --- INICIO DE LA LÓGICA DE GESTIÓN DE LÁPIDAS (VERSIÓN CORREGIDA Y COMPLETA) ---
            # 1. Colocar la lápida pendiente cuando ya no haya explosiones
            if lapida_por_colocar and not explosions:
                pos = lapida_por_colocar
                if not any(l.tile_x == pos[0] and l.tile_y == pos[1] for l in lapidas):
                    lapidas.append(Lapida(pos[0], pos[1], LAPIDA_IMG))
                lapida_por_colocar = None  # Reseteamos para la próxima muerte

            # 2. Actualizar y eliminar lápidas según todas las condiciones
            for lapida in lapidas[:]:
                lapida.update()  # Esto se encarga de la desaparición por tiempo y al ser tocada

                # Condición 1: La lápida ha terminado su animación de desvanecimiento
                if lapida.is_finished():
                    lapidas.remove(lapida)
                    continue  # Pasamos a la siguiente lápida porque esta ya no existe

                # Condición 2: Un objeto se ha colocado encima de la lápida
                debe_ser_eliminada = False
                # Si se coloca una bomba encima
                if any(b.tile_x == lapida.tile_x and b.tile_y == lapida.tile_y for b in bombs):
                    debe_ser_eliminada = True
                # Si es alcanzada por una explosión
                elif any(e.tile_x == lapida.tile_x and e.tile_y == lapida.tile_y for e in explosions):
                    debe_ser_eliminada = True
                # Si cae o se coloca un gadget visible encima
                elif any(p.x == lapida.tile_x and p.y == lapida.tile_y and p.visible for p in powerups):
                    debe_ser_eliminada = True

                if debe_ser_eliminada:
                    lapidas.remove(lapida)
            # --- FIN DE LA LÓGICA DE GESTIÓN DE LÁPIDAS ---

            for da in dropped_abilities[:]:
                da.update(dt, grid, powerups)
                if da.completed: dropped_abilities.remove(da)

            update_powerups(powerups, dt)
            if not set_end_sequence_start_time:
                check_pickup(players, powerups, lapidas)
            mortal_tiles_with_owner = {(e.tile_x, e.tile_y): e.owner for e in explosions if not e.finished}
            if mortal_tiles_with_owner and not set_end_sequence_start_time:
                for player in players[:]:
                    if player.is_ghost or player.is_invulnerable or player.escudo_active:
                        continue

                    player_hitbox = player.get_hitbox()
                    player_hitbox_area = player_hitbox.width * player_hitbox.height
                    if player_hitbox_area == 0:
                        continue

                    total_overlap_area = 0
                    killer = None

                    min_tile_x = player_hitbox.left // TILE_SIZE
                    max_tile_x = (player_hitbox.right - 1) // TILE_SIZE
                    min_tile_y = player_hitbox.top // TILE_SIZE
                    max_tile_y = (player_hitbox.bottom - 1) // TILE_SIZE

                    for tile_x in range(min_tile_x, max_tile_x + 1):
                        for tile_y in range(min_tile_y, max_tile_y + 1):
                            if (tile_x, tile_y) in mortal_tiles_with_owner:
                                # Coordenadas del juego (SIN TOP_OFFSET)
                                mortal_tile_rect = pygame.Rect(tile_x * TILE_SIZE, tile_y * TILE_SIZE, TILE_SIZE,
                                                               TILE_SIZE)
                                overlap_rect = player_hitbox.clip(mortal_tile_rect)
                                total_overlap_area += overlap_rect.width * overlap_rect.height
                                if mortal_tiles_with_owner[(tile_x, tile_y)] is not None:
                                    killer = mortal_tiles_with_owner[(tile_x, tile_y)]

                    if (total_overlap_area / player_hitbox_area) >= 0.15:
                        MUERTE_SOUND.play()
                        if killer and killer.is_ghost:
                            killer.resurrect()
                            player.become_ghost()
                        else:
                            if usar_fantasmas:
                                player.become_ghost()
                            else:
                                player.eliminate()

                        if lapida_por_colocar is None:
                            lapida_por_colocar = player.get_center_tile()

                        generar_poderes_al_morir(grid, bombs, powerups, players)
                        break

            if not set_end_sequence_start_time:
                alive_players = [p for p in players if not p.is_ghost and not p.is_eliminated]
                if len(alive_players) <= 1:
                    set_end_sequence_start_time = time.time()
                    if len(alive_players) == 1:
                        set_winner = alive_players[0]
                        set_winner.sets_won += 1
                        set_winner.is_set_winner = True
                        set_winner.set_winner_start_time = time.time()

            # --- DIBUJADO ---
            screen.fill(BLACK)
            draw_grid(screen, grid, SUELO1, SUELO2, STONE, BRICK, LIMIT_IMG)
            for lapida in lapidas:
                lapida.draw(screen)
            for p in powerups: p.draw(screen)
            for b in bombs: b.draw(screen)
            for da in dropped_abilities: da.draw(screen)

            drawable_players = [set_winner] if set_end_sequence_start_time and set_winner else players
            sorted_players = sorted([p for p in drawable_players if not p.is_ghost], key=lambda p: p.y)
            for p in sorted_players:
                if p.is_eliminated: continue
                p.draw(screen)
            for explosion in explosions[:]:
                explosion.update()
                if explosion.finished:
                    explosions.remove(explosion)
                else:
                    explosion.draw(screen)
            for p in drawable_players:
                if p.is_ghost: p.draw(screen)

            for i in range(len(gestor_jugadores.todos())):
                player_info = next((p for p in players if p.player_index == i), None)
                x_hud = 10 + i * 220
                if player_info: draw_HUD(screen, player_info, (x_hud, 5), color_pool[i % len(color_pool)])

            draw_timer(screen, max(0, TOTAL_TIME - (time.time() - start_time)))
            pygame.display.flip()

            if set_end_sequence_start_time and (time.time() - set_end_sequence_start_time > 3.0):
                set_running = False

        # --- FIN DEL SET ---
        if set_winner and set_winner.sets_won >= sets_to_win:
            match_running = False
        if not any(p for p in players):
            match_running = False

    # --- FIN DE LA PARTIDA ---

    from EstadoPartida import reiniciar_estado
    reiniciar_estado()
    # Importamos las funciones necesarias para volver al menú
    from PantallaConfigPartida import pantalla2_main
    from PantallaPrincipal import BackgroundAnimation

    # Definimos las dimensiones del menú (las mismas que en MainMenu.py)
    MENU_WIDTH = 800
    MENU_HEIGHT = 600

    # ¡AQUÍ ESTÁ LA CORRECCIÓN CLAVE!
    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))

    # Ahora creamos la animación de fondo con las dimensiones correctas del menú
    bg_anim = BackgroundAnimation(screen.get_width(), screen.get_height())

    # Y finalmente llamamos a la pantalla del menú de configuración con la pantalla ya corregida
    pantalla2_main(screen, bg_anim)