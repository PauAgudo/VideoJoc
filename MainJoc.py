import pygame
import time

from AuxiliarFunctions import TOTAL_TIME, start_time, grid, game_grid, powerups, players, bombs, explosions, dropped_abilities, exploding_blocks
from Assets import carregar_assets, COLOCAR_BOMBA_SOUND, COGER_HABILIDAD_SOUND, COGER_MALDICION_SOUND, SPEED_IMG, MAYOR_EXPLOSION_IMG, MORE_BOMB_IMG, PUSH_BOMB_IMG, RED_RIGHT_IMAGES, RED_LEFT_IMAGES, RED_UP_IMAGES, RED_DOWN_IMAGES, BLUE_RIGHT_IMAGES, BLUE_LEFT_IMAGES, BLUE_UP_IMAGES, BLUE_DOWN_IMAGES, SUELO1, SUELO2, STONE, BRICK, LIMIT_IMG, BLACK, RED, BLUE
from Drawing import draw_grid, draw_grid_lines, draw_powerups, draw_HUD, draw_timer
from Entities import Player, Explosion, WIDTH, HEIGHT
from GameLogic import generate_grid_and_powerups, check_pickup

def pantalla_partida(screen, bg_anim=None):
    clock = pygame.time.Clock()

    global grid, game_grid, powerups, players, bombs, explosions, dropped_abilities, exploding_blocks, start_time

    # Carregar imatges i sons un cop la pantalla està creada
    carregar_assets()

    # Inicialització del joc
    grid, powerups[:] = generate_grid_and_powerups()
    game_grid = grid
    players[:] = [
        Player(1, 1, RED, {
            'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d,
            'bomb': pygame.K_SPACE, 'hit': pygame.K_q
        }),
        Player(19, 15, BLUE, {
            'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
            'bomb': pygame.K_RETURN, 'hit': pygame.K_p
        })
    ]
    start_time = time.time()

    running = True
    while running:
        screen.fill(BLACK)
        draw_grid(screen, grid)
        draw_grid_lines(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                for player in players:
                    if event.key == player.controls['bomb']:
                        player.place_bomb(bombs, powerups)
                    elif 'hit' in player.controls and event.key == player.controls['hit']:
                        if player.hit_bomb_available:
                            dx, dy = 0, 0
                            if player.current_direction == "up": dy = -1
                            elif player.current_direction == "down": dy = 1
                            elif player.current_direction == "left": dx = -1
                            elif player.current_direction == "right": dx = 1
                            if player.invert_controls:
                                dx, dy = -dx, -dy
                            front_tile_x = player.get_center_tile()[0] + dx
                            front_tile_y = player.get_center_tile()[1] + dy
                            for b in bombs:
                                if b.tile_x == front_tile_x and b.tile_y == front_tile_y:
                                    if not b.hit_bouncing and not b.sliding:
                                        b.hit_by_player(dx, dy, grid, bombs, powerups)
                                    break

        keys = pygame.key.get_pressed()
        for player in players:
            if player.curse == "inverted":
                if keys[player.controls['up']]: player.move_down(grid, bombs)
                elif keys[player.controls['down']]: player.move_up(grid, bombs)
                elif keys[player.controls['left']]: player.move_right(grid, bombs)
                elif keys[player.controls['right']]: player.move_left(grid, bombs)
            else:
                if keys[player.controls['up']]: player.move_up(grid, bombs)
                elif keys[player.controls['down']]: player.move_down(grid, bombs)
                elif keys[player.controls['left']]: player.move_left(grid, bombs)
                elif keys[player.controls['right']]: player.move_right(grid, bombs)

            player.update_animation()
            player.update_passable(bombs)
            player.update_curse()

        for bomb in bombs[:]:
            if bomb.chain_triggered and time.time() - bomb.chain_trigger_time >= 0.75:
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

        dt = clock.tick(60) / 1000.0

        from GameLogic import update_powerups
        update_powerups(powerups, dt)
        draw_powerups(screen, powerups)

        check_pickup(players, powerups, game_grid, dropped_abilities,
                     COGER_MALDICION_SOUND, COGER_HABILIDAD_SOUND,
                     SPEED_IMG, MAYOR_EXPLOSION_IMG, MORE_BOMB_IMG, PUSH_BOMB_IMG)

        for player in players:
            player.draw(screen)

        for da in dropped_abilities[:]:
            da.update(dt)
            da.draw(screen)
            if da.completed:
                dropped_abilities.remove(da)

        now = time.time()
        to_remove = []
        for pos, start_time_expl in exploding_blocks.items():
            if now - start_time_expl >= 0.75:
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

    pygame.quit()
