import keystrokes
from combat_tank_colisao import collision_tank_or_ball
from creat_arena_1 import creat_arena
from config import *
from tanques import Tank
from ball import Ball
from draw_elements import draw_walls
from draw_elements import victory_texts
from draw_elements import hud
from draw_elements import draw_menu1
from draw_elements import draw_menu2

pygame.init()

# screen
size_screen = (1366, 720)
screen = pygame.display.set_mode(size_screen)

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
    arena = creat_arena("Arena_1")
    obstacle_color = gray
    arena_color = green
else:
    arena = creat_arena("Arena_2")
    obstacle_color = yellow
    arena_color = orange
list_of_obstacle = arena[0]
list_spawn_position = arena[1]
list_of_color = [red, blue, yellow, purple]

# creat tank
list_name_archive_tank = ["assets/tank1.png", "assets/tank2.png", "assets/tank3.png", "assets/tank4.png"]
list_name_archive_ball = ["assets/bala1.png", "assets/bala2.png", "assets/bala3.png", "assets/bala4.png"]
list_of_tank = []
n = 0
for a in range(number_of_tank):
    archive = pygame.image.load(list_name_archive_tank[n])
    x = list_spawn_position[n][0]
    y = list_spawn_position[n][1]
    tank = Tank(
        archive, x, y, 0, -speed_tank, 0, False, False, False, False, speed_angle_tank, 0, n, 0, False,
        arena_color, 0, False, 0, False)
    list_of_tank.append(tank)
    n += 1
list_of_tank_original = list_of_tank.copy()

# creat walls and obstacles
size_walls = 17
up_Wall = pygame.draw.rect(screen, gray, (0, 60, 1366, size_walls))
down_Wall = pygame.draw.rect(screen, gray, (0, size_screen[1] - size_walls, 1366, size_walls))
right_Wall = pygame.draw.rect(screen, gray, (size_screen[0] - size_walls, 60, size_walls, 660))
left_Wall = pygame.draw.rect(screen, gray, (0, 60, size_walls, 660))
for obstacle in list_of_obstacle:
    pygame.draw.rect(screen, obstacle_color, obstacle)

# victory texts
font = pygame.font.Font("assets/PressStart2P.ttf", 45)
list_of_victory = victory_texts(font, size_screen)

# hud
font = pygame.font.Font("assets/PressStart2P.ttf", 45)
list_of_hud = hud(font)

# sounds
shoot_sound = pygame.mixer.Sound("assets/tiger.wav")
tank_explode = pygame.mixer.Sound("assets/tank_explode.wav")
bounce_ball = pygame.mixer.Sound("assets/bounce_ball.wav")
tank_walk = pygame.mixer.Sound("assets/tank_walk.wav")
time_sound = tank_walk.get_length()
time_stop = 0

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
time_of_visibility = 0
identify = 0
time = 0
ide = 0
while loop_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop_game = False
            loop_victory = False
        if event.type == pygame.KEYDOWN:
            keystrokes.keys_down(event, list_of_tank, invisible_mode)

        if event.type == pygame.KEYUP:
            keystrokes.keys_up(event, list_of_tank)

    screen.fill(arena_color)
    counter = pygame.time.get_ticks()

    if respawn:
        list_of_tank = list_of_losers.copy()
        list_of_losers.clear()
        for tank in list_of_tank:
            tank.x_position = tank.x_origin
            tank.y_position = tank.y_origin
            tank.angle = 0
            tank.tank_photo = pygame.transform.rotate(tank.tank_surface, tank.angle)
            tank.vector = pygame.Vector2(0, -speed_tank)
            tank.movement = False
            tank.spin_right = False
            tank.spin_left = False
            tank.list_ball.clear()
        respawn = False

    for tank in list_of_tank:

        # analyze recharge condition
        if counter - tank.time_to_recharge > recharge_time * 1000:
            tank.recharge = False

        # tank rect
        tank.tank_rect = tank.tank_photo.get_rect()
        tank.tank_rect.center = (tank.x_position, tank.y_position)

        # draw tank
        if invisible_mode[0] and counter - tank.time_of_visibility > time_visibility * 1000 and not tank.animation:
            pygame.draw.rect(screen, arena_color, tank.tank_rect)
        else:
            screen.blit(tank.tank_photo, tank.tank_rect)

        # tank movement
        tank.move()
        if tank.movement:
            if counter - time_stop > time_sound * 1000:
                tank_walk.play()
                time_stop = pygame.time.get_ticks()
        tank.spin()

        # ball movement and collisions
        for ball in tank.list_ball:
            ball.move()
            ball.rect.center = (ball.x_position, ball.y_position)
            if ball.rect.colliderect(up_Wall) or ball.rect.colliderect(down_Wall):
                ball.speed_y *= -1
                ball.life -= 1
                bounce_ball.play()
            if ball.rect.colliderect(right_Wall) or ball.rect.colliderect(left_Wall):
                ball.speed_x *= -1
                ball.life -= 1
                bounce_ball.play()
            screen.blit(ball.photo, ball.rect)
            for obstacle in list_of_obstacle:
                x_obstacle_position = obstacle[0]
                y_obstacle_position = obstacle[1]
                w = obstacle[2]
                h = obstacle[3]
                if ball.rect.colliderect(obstacle):
                    ball.life -= 1
                    pos = collision_tank_or_ball(
                        ball.x_position, ball.y_position, ball.speed_x, ball. speed_y, x_obstacle_position,
                        y_obstacle_position, w, h, 1)
                    ball.x_position = pos[0][0]
                    ball.y_position = pos[0][1]
                    ball.speed_x = pos[1][0]
                    ball.speed_y = pos[1][1]
                    bounce_ball.play()
                    break
            if ball.life <= 0:
                tank.list_ball.remove(ball)

        # tank collision with obstacles
        for obstacle in list_of_obstacle:
            x_obstacle_position = obstacle[0]
            y_obstacle_position = obstacle[1]
            w = obstacle[2]
            h = obstacle[3]
            if tank.tank_rect.colliderect(obstacle):
                pos = collision_tank_or_ball(
                    tank.x_position, tank.y_position, tank.vector[0], tank.vector[1], x_obstacle_position,
                    y_obstacle_position, w, h, 0)
                if tank.x_position != pos[0][0]:
                    tank.x_position = pos[0][0]
                if tank.y_position != pos[0][1]:
                    tank.y_position = pos[0][1]

        # tank collision with wall
        if tank.tank_rect.colliderect(up_Wall):
            tank.y_position += abs(tank.vector[1])
        if tank.tank_rect.colliderect(down_Wall):
            tank.y_position += -abs(tank.vector[1])
        if tank.tank_rect.colliderect(right_Wall):
            tank.x_position += -abs(tank.vector[0])
        if tank.tank_rect.colliderect(left_Wall):
            tank.x_position += abs(tank.vector[0])

        # tank collision with enemy ball
        for tank_enemy in list_of_tank:
            if tank.id != tank_enemy.id:
                for ball in tank_enemy.list_ball:
                    if ball.rect.colliderect(tank.tank_rect):
                        tank_enemy.point += 1
                        tank.animation = True
                        tank.animation_time = pygame.time.get_ticks()
                        tank.list_ball.clear()
                        tank_enemy.list_ball.remove(ball)
                        tank_explode.play()
                        list_of_animations.append(tank)
                        break
        if tank.animation:
            list_of_tank.remove(tank)
            break

        # shoot
        if len(tank.list_ball) >= limit_ball:
            tank.trigger = False
        if tank.trigger:
            if invisible_mode[0]:
                tank.time_of_visibility = pygame.time.get_ticks()
            ball_archive = pygame.image.load(list_name_archive_ball[tank.id])
            ball = Ball(
                ball_archive, tank.x_position, tank.y_position, speed_ball * tank.vector[0],
                speed_ball * tank.vector[1], life_ball)
            tank.list_ball.append(ball)
            tank.trigger = False
            shoot_sound.play()

    # animations death tank
    for tank in list_of_animations:
        if tank.animation and counter - tank.animation_time < animation_time:
            tank.angle += 20
            tank.tank_photo = pygame.transform.rotate(tank.tank_surface, tank.angle)
            tank.movement = False
            tank.spin_right = False
            tank.spin_left = False
            tank.trigger = False

        if tank.animation and counter - tank.animation_time > animation_time:
            tank.animation = False
            tank.remove = True
            identify = tank.id
        screen.blit(tank.tank_photo, tank.tank_rect)

        if tank.remove:
            list_of_losers.append(tank)
            tank.remove = False
            list_of_animations.remove(tank)
            break

    if len(list_of_tank) == 1 and len(list_of_animations) == 0:
        list_of_losers.append(list_of_tank[0])
        list_of_tank.clear()
        respawn = True

    # draw walls and obstacles
    draw_walls(screen, obstacle_color, (up_Wall, down_Wall, right_Wall, left_Wall))
    for obstacle in list_of_obstacle:
        pygame.draw.rect(screen, obstacle_color, obstacle)

    # draw hud
    for tank in list_of_tank:
        list_of_hud[tank.id][0] = font.render(str(tank.point), True, list_of_color[tank.id])
        screen.blit(list_of_hud[tank.id][0], list_of_hud[tank.id][1])
        if tank.point >= point_victory and len(list_of_animations) == 0:
            loop_game = False
            ide = tank.id
    for tank in list_of_losers:
        list_of_hud[tank.id][0] = font.render(str(tank.point), True, list_of_color[tank.id])
        screen.blit(list_of_hud[tank.id][0], list_of_hud[tank.id][1])
    for tank in list_of_animations:
        list_of_hud[tank.id][0] = font.render(str(tank.point), True, list_of_color[tank.id])
        screen.blit(list_of_hud[tank.id][0], list_of_hud[tank.id][1])

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
