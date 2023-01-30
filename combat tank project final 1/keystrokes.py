import pygame


def keys_down(event, list_of_tank, invisible_mode, counter):
    if event.key == pygame.K_m and not invisible_mode[0]:
        invisible_mode[0] = True
    if event.key == pygame.K_n and invisible_mode:
        invisible_mode[0] = False

    for tank in list_of_tank:
        if tank.get_id() == 0:
            move_front = pygame.K_w
            spin_left = pygame.K_a
            spin_right = pygame.K_d
            shoot = pygame.K_s

        elif tank.get_id() == 1:
            move_front = pygame.K_UP
            spin_left = pygame.K_LEFT
            spin_right = pygame.K_RIGHT
            shoot = pygame.K_DOWN

        elif tank.get_id() == 2:
            move_front = pygame.K_t
            spin_left = pygame.K_f
            spin_right = pygame.K_h
            shoot = pygame.K_g

        elif tank.get_id() == 3:
            move_front = pygame.K_i
            spin_left = pygame.K_j
            spin_right = pygame.K_l
            shoot = pygame.K_k
        else:
            move_front = 0
            spin_right = 0
            spin_left = 0
            shoot = 0

        if event.key == move_front:
            tank.set_movement(True)
        if event.key == spin_right:
            tank.set_spin_r(True)
        if event.key == spin_left:
            tank.set_spin_l(True)
        if event.key == shoot:
            tank.shoot(counter)
            tank.time_to_recharge = pygame.time.get_ticks()


def keys_up(event, list_of_tank):
    for tank in list_of_tank:
        if tank.get_id() == 0:
            move_front = pygame.K_w
            spin_left = pygame.K_a
            spin_right = pygame.K_d

        elif tank.get_id() == 1:
            move_front = pygame.K_UP
            spin_left = pygame.K_LEFT
            spin_right = pygame.K_RIGHT

        elif tank.get_id() == 2:
            move_front = pygame.K_t
            spin_left = pygame.K_f
            spin_right = pygame.K_h

        elif tank.get_id() == 3:
            move_front = pygame.K_i
            spin_left = pygame.K_j
            spin_right = pygame.K_l
        else:
            move_front = 0
            spin_right = 0
            spin_left = 0

        if event.key == move_front:
            tank.set_movement(False)
        if event.key == spin_right:
            tank.set_spin_r(False)
        if event.key == spin_left:
            tank.set_spin_l(False)
