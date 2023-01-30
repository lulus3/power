import keystrokes
from combat_tank_colisao import collision_tank_or_ball
from config import *
from draw_elements import victory_texts
from draw_elements import hud
from draw_elements import draw_menu1
from draw_elements import draw_menu2
from tanques import Tank
import arena_class

pygame.init()

menu = True
ask = 2
font = pygame.font.Font("assets/PressStart2P.ttf", 25)
while menu:
    screen.fill(black)
    draw_menu1("assets/arena1.png", "assets/arena2.png", screen, font)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                ask = 1
                menu = False
            if event.key == pygame.K_2:
                ask = 2
                menu = False
    pygame.display.flip()

menu = True
number_of_tank = 0
while menu:
    screen.fill(black)
    draw_menu2("assets/tank1.png", "assets/tank2.png", "assets/tank3.png", "assets/tank4.png", screen, font)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_2:
                number_of_tank = 2
                menu = False
            if event.key == pygame.K_3:
                number_of_tank = 3
                menu = False
            if event.key == pygame.K_4:
                number_of_tank = 4
                menu = False
    pygame.display.flip()

# creat arena
if ask == 1:
    arena = arena_class.Arena()
    arena.creat_arena("Arena_1")
    obstacle_color = gray
    arena_color = green
else:
    arena = arena_class.Arena()
    arena.creat_arena("Arena_2")
    obstacle_color = yellow
    arena_color = orange

list_of_color = [red, blue, yellow, purple]

# creat tank
list_name_archive_tank = ["assets/tank1.png", "assets/tank2.png", "assets/tank3.png", "assets/tank4.png"]
list_of_tank = []
list_spawn_position = arena.get_spawns()
n = 0
for a in range(number_of_tank):
    archive = pygame.image.load(list_name_archive_tank[n])
    x = list_spawn_position[n][0]
    y = list_spawn_position[n][1]
    tank = Tank(archive, arena_color, x, y, 0, speed_tank, 0, n)
    list_of_tank.append(tank)
    n += 1

# creat walls
size_walls = 17
up_Wall = pygame.draw.rect(screen, gray, (0, 60, 1366, size_walls))
down_Wall = pygame.draw.rect(screen, gray, (0, size_screen[1] - size_walls, 1366, size_walls))
right_Wall = pygame.draw.rect(screen, gray, (size_screen[0] - size_walls, 60, size_walls, 660))
left_Wall = pygame.draw.rect(screen, gray, (0, 60, size_walls, 660))
list_wall = [up_Wall, down_Wall, right_Wall, left_Wall]
arena.set_walls(list_wall)

# victory texts
font = pygame.font.Font("assets/PressStart2P.ttf", 45)
list_of_victory = victory_texts(font, size_screen)

# hud
font = pygame.font.Font("assets/PressStart2P.ttf", 45)
list_of_hud = hud(font)

clock = pygame.time.Clock()
loop_game = True
animation = False
respawn = False
stop = False
victory = False
clear_ball = False
loop_victory = True
invisible_mode = [False]
remove_tank = False
round_finished = False
list_of_losers = []
list_of_animations = []
animation_time *= 1000
identify = 0
counter = 0
time_to_respawn = 0
ide = -1
while loop_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop_game = False
            loop_victory = False
        if event.type == pygame.KEYDOWN:
            keystrokes.keys_down(event, list_of_tank, invisible_mode, counter)

        if event.type == pygame.KEYUP:
            keystrokes.keys_up(event, list_of_tank)

    screen.fill(arena_color)
    counter = pygame.time.get_ticks()

    if respawn:
        list_of_tank = list_of_animations.copy()
        list_of_animations.clear()
        for tank in list_of_tank:
            tank.respawn(speed_tank)
            respawn = False

    for tank in list_of_tank:

        # tank rect
        tank.rect = tank.get_photo().get_rect()
        tank.rect.center = (tank.get_x(), tank.get_y())

        screen.blit(tank.get_photo(), tank.rect)

        tank.move()
        tank.spin_right()
        tank.spin_left()

        for obstacle in arena.get_obstacles():
            x_obstacle_position = obstacle.get_x()
            y_obstacle_position = obstacle.get_y()
            w = obstacle.get_w()
            h = obstacle.get_h()

            # tank collision with obstacles
            if tank.rect.colliderect(obstacle.get_rect()):
                vector = tank.get_vector()
                pos = collision_tank_or_ball(
                    tank.get_x(), tank.get_y(), vector[0], vector[1], x_obstacle_position,
                    y_obstacle_position, w, h, 0)
                if tank.get_x() != pos[0][0]:
                    tank.set_x(pos[0][0])
                if tank.get_y() != pos[0][1]:
                    tank.set_y(pos[0][1])

            # bullet collision with obstacles
            for bullet in tank.get_bullets():
                if bullet.rect.colliderect(obstacle.get_rect()):
                    bounce_ball.play()
                    bullet.life -= 1
                    pos = collision_tank_or_ball(
                        bullet.x_position, bullet.y_position, bullet.speed_x, bullet.speed_y, x_obstacle_position,
                        y_obstacle_position, w, h, 1)
                    bullet.x_position = pos[0][0]
                    bullet.y_position = pos[0][1]
                    bullet.speed_x = pos[1][0]
                    bullet.speed_y = pos[1][1]

        # tank collision with wall
        if tank.rect.colliderect(up_Wall):
            tank.set_y(tank.get_y() + abs(tank.get_vector()[1]))
        if tank.rect.colliderect(down_Wall):
            tank.set_y(tank.get_y() - abs(tank.get_vector()[1]))
        if tank.rect.colliderect(right_Wall):
            tank.set_x(tank.get_x() - abs(tank.get_vector()[0]))
        if tank.rect.colliderect(left_Wall):
            tank.set_x(tank.get_x() + abs(tank.get_vector()[0]))

        # bullet collision with wall
        for bullet in tank.get_bullets():
            bullet.move()
            bullet.rect.center = (bullet.x_position, bullet.y_position)
            if bullet.rect.colliderect(up_Wall) or bullet.rect.colliderect(down_Wall):
                bullet.speed_y *= -1
                bullet.life -= 1
            if bullet.rect.colliderect(right_Wall) or bullet.rect.colliderect(left_Wall):
                bullet.speed_x *= -1
                bullet.life -= 1
            screen.blit(bullet.photo, bullet.rect)
            if bullet.life <= 0:
                tank.get_bullets().remove(bullet)

        for tank_enemy in list_of_tank:
            if tank.get_id() != tank_enemy.get_id():
                for ball in tank_enemy.get_bullets():
                    if ball.rect.colliderect(tank.rect):
                        tank_enemy.ad_point()
                        tank.get_bullets().clear()
                        tank_enemy.get_bullets().remove(ball)
                        tank.set_time_of_animation()
                        list_of_animations.append(tank)
                        list_of_tank.remove(tank)
                        tank_explode.play()
                        break

    # animations death tank
    for tank in list_of_animations:
        tank.spin_death(counter, screen, tank.rect)

    if len(list_of_tank) == 1 and counter - list_of_animations[number_of_tank - 2].get_time_of_animation() > animation_time:
        list_of_animations.append(list_of_tank[0])
        list_of_tank.clear()
        respawn = True

    # draw walls and obstacles
    arena.draw_obstacles(screen, obstacle_color)
    arena.draw_walls(screen, obstacle_color)

    # draw hud
    for tank in list_of_tank:
        list_of_hud[tank.get_id()][0] = font.render(str(tank.get_point()), True, list_of_color[tank.get_id()])
        screen.blit(list_of_hud[tank.get_id()][0], list_of_hud[tank.get_id()][1])
        if tank.get_point() >= point_victory:
            if ide == -1:
                ide = tank.get_id()
            if counter - list_of_animations[-1].get_time_of_animation() > animation_time:
                loop_game = False
    for tank in list_of_animations:
        list_of_hud[tank.get_id()][0] = font.render(str(tank.get_point()), True, list_of_color[tank.get_id()])
        screen.blit(list_of_hud[tank.get_id()][0], list_of_hud[tank.get_id()][1])

    pygame.display.flip()
    clock.tick(60)

while loop_victory:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop_victory = False
    screen.fill(black)
    screen.blit(list_of_victory[ide][0], list_of_victory[ide][1])
    pygame.display.flip()

pygame.quit()
