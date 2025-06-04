import pygame

import time

from pygame import Rect

# S'assumeix que aquestes constants i imatges seran importades o definides a config/assets
TILE_SIZE = 40
TOP_OFFSET = 80
WIDTH = 21 * TILE_SIZE
HEIGHT = 17 * TILE_SIZE + TOP_OFFSET
EXPLOSION_DURATION = 0.75
PUSH_SPEED = 3

# Placeholder per CURSES si no s'importa
CURSES = {
    "reset": {"duration": None, "shows_in_hud": False, "clears_previous": False},
    "no_ability": {"duration": 40.0, "shows_in_hud": True, "clears_previous": True},
    "no_bomb": {"duration": 40.0, "shows_in_hud": True, "clears_previous": True},
    "auto_bomb": {"duration": 40.0, "shows_in_hud": True, "clears_previous": True},
    "inverted": {"duration": 40.0, "shows_in_hud": True, "clears_previous": True},
    "hyper_speed": {"duration": 40.0, "shows_in_hud": True, "clears_previous": True},
    "slow_speed": {"duration": 40.0, "shows_in_hud": True, "clears_previous": True},
}


class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.visible = False
        self.disappearing = False
        self.destroy_frames = []
        self.destroy_frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.vanished = False
        self.spawning = True
        self.spawn_timer = 0.0
        self.bouncing = False
        self.bounce_path = []
        self.bounce_index = 0
        self.bounce_timer = 0.0
        self.bounce_cell_time = 0.15
        self.teleporting = False

    def start_spawn_animation(self):
        self.spawning = True
        self.spawn_timer = 0.0

    def update(self, dt):
        # Simplificat
        pass

    def draw(self, screen):
        # Placeholder de dibuix
        pass

    def start_disappear(self):
        self.disappearing = True
        self.destroy_frame_index = 0
        self.last_update = pygame.time.get_ticks()

    def is_destroyed(self):
        return self.vanished or (self.disappearing and self.destroy_frame_index >= len(self.destroy_frames))


class Player:
    def __init__(self, init_tile_x, init_tile_y, color, controls):
        self.x = init_tile_x * TILE_SIZE - 40
        self.y = init_tile_y * TILE_SIZE - 40
        self.color = color
        self.controls = controls
        self.original_controls = controls.copy()
        self.bomb_limit = 1
        self.bomb_range = 1
        self.speed = 1.0
        self.base_speed = 1.0
        self.active_curse = None
        self.curse_ends_at = None
        self.push_bomb_available = False
        self.hit_bomb_available = False
        self.auto_bombing = False
        self.invert_controls = False
        self.health = 3

    def get_center_tile(self):
        cx = self.x + 60
        cy = self.y + 60
        return int(cx // TILE_SIZE), int(cy // TILE_SIZE)

    def draw(self, screen):
        # Placeholder de dibuix
        pass

    def place_bomb(self, bombs, powerups, forced=False):
        # Placeholder de col·locació de bomba
        pass

    def apply_curse(self, curse_name):
        # Placeholder per aplicar una maledicció
        pass

    def update_curse(self):
        # Placeholder per actualitzar la maledicció
        pass


class Bomb:
    def __init__(self, tile_x, tile_y, blast_range):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.blast_range = blast_range
        self.timer = 3
        self.plant_time = time.time()
        self.exploded = False
        self.pos_x = self.tile_x * TILE_SIZE
        self.pos_y = self.tile_y * TILE_SIZE
        self.passable_players = set()

    def explode(self, grid, players, bombs, powerups):
        return []

    def draw(self, screen):
        pass


class Explosion:
    def __init__(self, tile_x, tile_y, explosion_type="normal", direction=None):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.explosion_type = explosion_type
        self.direction = direction
        self.finished = False
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

    def update(self):
        pass

    def draw(self, screen):
        pass


class DroppedAbility:
    def __init__(self, start_pos, image, target_cell, ability_type):
        self.start_x, self.start_y = start_pos
        self.image = image
        self.target_cell = target_cell
        self.ability_type = ability_type
        self.elapsed = 0
        self.duration = 1.5
        self.completed = False
        self.current_pos = start_pos

    def update(self, dt):
        pass

    def draw(self, screen):
        pass
