import sys
from Config import get_configuracion_completa
from Bomberman import *  # reutilitzem totes les classes i funcions ja definides


def iniciar_partida(screen):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    config = get_configuracion_completa()
    pygame.init()

    TOTAL_TIME = 180
    start_time = time.time()
    grid, powerups = generate_grid_and_powerups()
    game_grid = grid
    players = [
        Player(1, 1, RED,
               {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d, 'bomb': pygame.K_SPACE,
                'hit': pygame.K_q}),
        Player(19, 15, BLUE, {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
                              'bomb': pygame.K_RETURN, 'hit': pygame.K_p}),
    ]
    bombs = []
    explosions = []
    dropped_abilities = []

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)
        draw_grid(screen, grid)
        draw_grid_lines(screen)
        for player in players:
            if player.auto_bombing:
                player.place_bomb(bombs, powerups, forced=True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                for player in players:
                    player.update_curse()
                    if event.key == player.controls['bomb']:
                        player.place_bomb(bombs, powerups)
                    elif 'hit' in player.controls and event.key == player.controls['hit']:
                        # Si el jugador tiene el poder de golpear bombas
                        if player.hit_bomb_available:
                            # Determinamos la dirección (dx, dy) según hacia dónde mira el jugador
                            dx, dy = 0, 0
                            if player.current_direction == "up":
                                dy = -1
                            elif player.current_direction == "down":
                                dy = 1
                            elif player.current_direction == "left":
                                dx = -1
                            elif player.current_direction == "right":
                                dx = 1
                            if player.invert_controls:
                                dx, dy = -dx, -dy
                            if dx > 0:
                                player.move_right(grid, bombs)
                            elif dx < 0:
                                player.move_left(grid, bombs)
                            if dy > 0:
                                player.move_down(grid, bombs)
                            elif dy < 0:
                                player.move_up(grid, bombs)

                            # Casilla que está frente al jugador
                            front_tile_x = player.get_center_tile()[0] + dx
                            front_tile_y = player.get_center_tile()[1] + dy

                            # Buscamos si hay una bomba en esa casilla
                            for b in bombs:
                                if b.tile_x == front_tile_x and b.tile_y == front_tile_y:
                                    # Si no está ya rebotando ni deslizándose, la golpeamos
                                    if not b.hit_bouncing and not b.sliding:
                                        b.hit_by_player(dx, dy, grid, bombs, powerups)
                                    break  # Salimos tras golpear la primera bomba encontrada

        keys = pygame.key.get_pressed()
        for player in players:
            if player.curse == "inverted":
                if keys[player.controls['up']]:
                    player.move_down(grid, bombs)
                elif keys[player.controls['down']]:
                    player.move_up(grid, bombs)
                elif keys[player.controls['left']]:
                    player.move_right(grid, bombs)
                elif keys[player.controls['right']]:
                    player.move_left(grid, bombs)
            else:
                if keys[player.controls['up']]:
                    player.move_up(grid, bombs)
                elif keys[player.controls['down']]:
                    player.move_down(grid, bombs)
                elif keys[player.controls['left']]:
                    player.move_left(grid, bombs)
                elif keys[player.controls['right']]:
                    player.move_right(grid, bombs)

            player.update_animation()
            player.update_passable(bombs)
            player.check_static_push(grid, bombs, players, powerups)
            player.update_curse()

        for player in players:
            if player.curse == "auto_bomb":
                current_tile = player.get_center_tile()
                current_bombs = [b for b in bombs if b.owner == player and not b.exploded]
                if len(current_bombs) < player.bomb_limit:
                    bomb_exists = any(b for b in bombs if (b.tile_x, b.tile_y) == current_tile and not b.exploded)
                    if not bomb_exists:
                        player.place_bomb(bombs, powerups, forced=True)
                player.last_auto_bomb_tile = current_tile

        current_time = time.time()
        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                p1 = players[i]
                p2 = players[j]
                cx1, cy1 = p1.get_center_coords()
                cx2, cy2 = p2.get_center_coords()
                dist = math.hypot(cx2 - cx1, cy2 - cy1)
                if dist <= 10 and (current_time - p1.last_curse_exchange >= 3) and (
                        current_time - p2.last_curse_exchange >= 3):
                    if p1.curse is not None and p2.curse is None:
                        p2.curse = p1.curse
                        p2.curse_start = p1.curse_start
                        p1.curse = None
                        p1.curse_start = None
                    elif p2.curse is not None and p1.curse is None:
                        p1.curse = p2.curse
                        p1.curse_start = p2.curse_start
                        p2.curse = None
                        p2.curse_start = None
                    else:
                        p1.curse, p2.curse = p2.curse, p1.curse
                        p1.curse_start, p2.curse_start = p2.curse_start, p1.curse_start
                    p1.last_curse_exchange = current_time
                    p2.last_curse_exchange = current_time

        for bomb in bombs[:]:
            if bomb.chain_triggered:
                if time.time() - bomb.chain_trigger_time >= 0.75:
                    exp_positions = bomb.explode(grid, players, bombs, powerups)
                    for pos in exp_positions:
                        tx, ty, expl_type, direction = pos
                        explosions.append(Explosion(tx, ty, explosion_type=expl_type, direction=direction))
            elif time.time() - bomb.plant_time >= bomb.timer:
                exp_positions = bomb.explode(grid, players, bombs, powerups)
                for pos in exp_positions:
                    tx, ty, expl_type, direction = pos
                    explosions.append(Explosion(tx, ty, explosion_type=expl_type, direction=direction))

        for bomb in bombs:
            bomb.draw(screen)

        for explosion in explosions[:]:
            explosion.update()
            if explosion.finished:
                explosions.remove(explosion)
            else:
                explosion.draw(screen)

        dt = clock.tick(60) / 1000.0  # ← define dt (a 60 FPS, en segundos)
        update_powerups(powerups, dt)  # Ahora dt ya está definidod
        draw_powerups(screen, powerups)

        check_pickup(players, powerups)

        for player in players:
            player.draw(screen)

        dt = clock.get_time() / 1000.0
        for da in dropped_abilities[:]:
            da.update(dt)
            da.draw(screen)
            if da.completed:
                dropped_abilities.remove(da)

        now = time.time()
        to_remove = []
        for pos, start_time_expl in exploding_blocks.items():
            if now - start_time_expl >= EXPLOSION_DURATION:
                x, y = pos
                grid[y][x] = 0
                to_remove.append(pos)
        for pos in to_remove:
            del exploding_blocks[pos]

        elapsed = time.time() - start_time
        remaining_time = TOTAL_TIME - elapsed
        if remaining_time < 0:
            remaining_time = 0
        draw_timer(screen, remaining_time)

        draw_HUD(screen, players[0], (10, 5), RED)
        draw_HUD(screen, players[1], (WIDTH - 210, 5), BLUE)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()