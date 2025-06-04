import pygame
import time

# Constants d'entorn (hauries d'importar-les des de config si es modularitza més)
TILE_SIZE = 40
GRID_COLS = 21
GRID_ROWS = 17
TOP_OFFSET = 80
WIDTH = GRID_COLS * TILE_SIZE
HEIGHT = GRID_ROWS * TILE_SIZE + TOP_OFFSET
EXPLOSION_DURATION = 0.75

# Variables globals per simulació (substituir per dependències reals si cal)
exploding_blocks = {}
font = pygame.font.SysFont("Arial", 20)

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

# Imatges que hauries de carregar externament
SUELO1 = None
SUELO2 = None
BRICK = None
STONE = None
LIMIT_IMG = None
timer_digits = {}
timer_separador = None
timer_marco = None
DIGIT_SIZE = (40, 60)
SEPARADOR_SIZE = (20, 60)
MARCO_SIZE = (200, 80)


def draw_grid(screen, grid):
    current_time = time.time()
    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + TOP_OFFSET, TILE_SIZE, TILE_SIZE)
            if (x + y) % 2 == 0:
                screen.blit(SUELO1, rect)
            else:
                screen.blit(SUELO2, rect)

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


def draw_powerups(screen, powerups):
    for p in powerups:
        p.draw(screen)


def draw_HUD(screen, player, pos, color):
    x, y = pos
    line_height = 20
    screen.blit(font.render(f"Bombas x{player.bomb_limit}", True, color), (x, y))
    y += line_height
    screen.blit(font.render(f"Rango x{player.bomb_range}", True, color), (x, y))
    y += line_height
    if player.curse == "slow_speed":
        text = "Velocidad: slow"
    elif player.curse == "hyper_speed":
        text = "Velocidad: fast"
    else:
        text = f"Velocidad x{player.speed:.1f}"
    screen.blit(font.render(text, True, color), (x, y))
    y += line_height
    text = "Empujar bomba: Sí" if player.push_bomb_available else "Empujar bomba: No"
    screen.blit(font.render(text, True, color), (x, y))
    y += line_height
    text = "Golpear bombas: Sí" if player.hit_bomb_available else "Golpear bombas: No"
    screen.blit(font.render(text, True, color), (x, y))
    y += line_height
    if getattr(player, 'active_curse', None) and getattr(player, 'curse_ends_at', None):
        meta = CURSES[player.active_curse]
        if meta["shows_in_hud"] and meta["duration"] is not None:
            remaining = max(0, int(player.curse_ends_at - time.time()))
            text = f"{player.active_curse}: {remaining}s"
        else:
            text = "No curse"
    else:
        text = "No curse"
    screen.blit(font.render(text, True, color), (x, y))


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
