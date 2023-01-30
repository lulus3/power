import pygame


class Tank:
    def __init__(
            self, photo, x, y, speed_x, speedy, angle, trigger, spin_right, spin_left, movement, speed_angle, life, ide,
            time_to_recharge, recharge, color, time_of_visibility, animation, animation_time, remove
    ):
        self.list_ball = []
        self.tank_photo = photo
        self.tank_surface = pygame.Surface((self.tank_photo.get_width(), self.tank_photo.get_height()))
        size = (0, 0, self.tank_photo.get_width(), self.tank_photo.get_height())
        pygame.draw.rect(self.tank_surface, color, size)
        self.tank_surface.blit(self.tank_photo, (0, 0))
        self.x_position = x
        self.y_position = y
        self.x_origin = x
        self.y_origin = y
        self.list_ball = []
        self.vector = pygame.Vector2(speed_x, speedy)
        self.angle = angle
        self.trigger = trigger
        self.spin_right = spin_right
        self.spin_left = spin_left
        self.movement = movement
        self.speed_angle = speed_angle
        self.point = life
        self.id = ide
        self.time_to_recharge = time_to_recharge
        self.recharge = recharge
        self.time_of_visibility = time_of_visibility
        self.animation = animation
        self.animation_time = animation_time
        self.remove = remove

    def move(self):
        if self.movement:
            self.x_position += self.vector[0]
            self.y_position += self.vector[1]

    def shoot(self, ball):
        self.list_ball.append(ball)

    def spin(self):
        if self.spin_right:
            self.angle += -self.speed_angle
            if self.angle <= -360:
                self.angle = 0
            self.tank_photo = pygame.transform.rotate(self.tank_surface, self.angle)
            self.vector = self.vector.rotate(self.speed_angle)
        if self.spin_left:
            self.angle += self.speed_angle
            if self.angle >= 360:
                self.angle = 0
            self.tank_photo = pygame.transform.rotate(self.tank_surface, self.angle)
            self.vector = self.vector.rotate(-self.speed_angle)
