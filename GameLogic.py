import math
import random
import time

from Entities import PowerUp, DroppedAbility

GRID_COLS = 21
GRID_ROWS = 17

CURSES = {
    "reset": {}, "no_ability": {}, "no_bomb": {}, "auto_bomb": {},
    "inverted": {}, "hyper_speed": {}, "slow_speed": {}
}


def tile_blocked_for_player(grid, bombs, tile_x, tile_y, player):
    if tile_x < 0 or tile_x >= GRID_COLS or tile_y < 0 or tile_y >= GRID_ROWS:
        return True
    if grid[tile_y][tile_x] in (1, 2, 3):
        return True
    for b in bombs:
        if b.tile_x == tile_x and b.tile_y == tile_y:
            if player in b.passable_players:
                return False
            else:
                return True
    return False


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
            if grid[y][x] == 0 and random.random() < 0.7:
                grid[y][x] = 1
                r = random.random()
                if r < 0.1:
                    powerups.append(PowerUp(x, y, "speed"))
                elif r < 0.3:
                    powerups.append(PowerUp(x, y, "major_explosion"))
                elif r < 0.4:
                    powerups.append(PowerUp(x, y, "more_bomb"))
                elif r < 0.45:
                    powerups.append(PowerUp(x, y, "calavera"))
                elif r < 0.5:
                    if random.random() < 0.5:
                        powerups.append(PowerUp(x, y, "push_bomb"))
                    else:
                        powerups.append(PowerUp(x, y, "golpear_bombas"))
    return grid, powerups


def check_pickup(players, powerups, game_grid, dropped_abilities,
                  SOUND_CURSE, SOUND_POWERUP,
                  IMG_SPEED, IMG_EXPLOSION, IMG_BOMB, IMG_PUSH):
    to_remove = []
    for p in powerups:
        if p.visible and not p.disappearing and not p.vanished:
            for player in players:
                if player.get_center_tile() == (p.x, p.y):
                    if player.curse == "no_ability" and p.type != "calavera":
                        continue
                    if p.type == "calavera":
                        curse_name = random.choice(list(CURSES.keys()))
                        player.apply_curse(curse_name)
                        SOUND_CURSE.play()
                        p.visible = False
                        try:
                            powerups.remove(p)
                        except ValueError:
                            pass
                        dropped_abilities.append(p)
                        to_remove.append(p)
                        break
                    elif p.type != "calavera" and not player.can_pick_abilities:
                        continue
                    elif p.type == "push_bomb":
                        player.push_bomb_available = True
                        SOUND_POWERUP.play()
                        to_remove.append(p)
                        break
                    elif p.type == "golpear_bombas":
                        player.hit_bomb_available = True
                        SOUND_POWERUP.play()
                        to_remove.append(p)
                        break
                    elif p.type == "reset":
                        default_speed = 1.0
                        default_bomb_range = 1
                        default_bomb_limit = 1
                        dropped = []
                        if player.base_speed > default_speed:
                            bonus_units = int(round((player.base_speed - default_speed) / 0.5))
                            for _ in range(bonus_units):
                                dropped.append(("speed", IMG_SPEED))
                            player.base_speed = default_speed
                        if player.bomb_range > default_bomb_range:
                            bonus_units = player.bomb_range - default_bomb_range
                            for _ in range(bonus_units):
                                dropped.append(("major_explosion", IMG_EXPLOSION))
                            player.bomb_range = default_bomb_range
                        if player.bomb_limit > default_bomb_limit:
                            bonus_units = player.bomb_limit - default_bomb_limit
                            for _ in range(bonus_units):
                                dropped.append(("more_bomb", IMG_BOMB))
                            player.bomb_limit = default_bomb_limit
                        if player.push_bomb_available:
                            dropped.append(("push_bomb", IMG_PUSH))
                            player.push_bomb_available = False
                        free_cells = get_available_free_cells(game_grid, powerups)
                        for ability_type, img in dropped:
                            if free_cells:
                                target = random.choice(free_cells)
                                free_cells.remove(target)
                            else:
                                target = find_free_cell_far_from(player, game_grid)
                            dropped_abilities.append(
                                DroppedAbility(player.get_center_coords(), img, target, ability_type)
                            )
                        SOUND_POWERUP.play()
                        to_remove.append(p)
                        break
                    else:
                        if player.curse == "no_ability":
                            continue
                        if p.type == "major_explosion":
                            player.bomb_range += 1
                        elif p.type == "speed":
                            if player.active_curse in ("hyper_speed", "slow_speed"):
                                player.pending_speed_boosts += 0.5
                            else:
                                player.base_speed += 0.5
                                player.speed = player.base_speed
                        elif p.type == "more_bomb":
                            player.bomb_limit += 1
                        SOUND_POWERUP.play()
                        p.start_disappear()
                        to_remove.append(p)
                        break
    for r in to_remove:
        if r in powerups:
            powerups.remove(r)
