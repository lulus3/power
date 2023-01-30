import pygame.draw


class Arena:
    def __init__(self):
        self.__list_obstacles = []
        self.__list_wall = []
        self.__list_spawn = []

    def draw_obstacles(self, surface, color):
        for obstacle in self.__list_obstacles:
            pygame.draw.rect(surface, color, obstacle.get_rect())

    def draw_walls(self, surface, color):
        for wall in self.__list_wall:
            pygame.draw.rect(surface, color, wall)

    def set_obstacles(self, obstacles):
        self.__list_obstacles = obstacles

    def set_walls(self, walls):
        self.__list_wall = walls

    def get_obstacles(self):
        return self.__list_obstacles

    def get_walls(self):
        return self.__list_wall

    def get_spawns(self):
        return self.__list_spawn

    def creat_arena(self, file_name):
        mc = 1332 / 222
        ml = 620 / 40
        archive = open(file_name, "r")
        lista_of_lines = archive.readlines()
        t1, t2, t3, t4 = 0, 0, 0, 0
        location1, location2, location3, location4 = 0, 0, 0, 0
        for line in range(len(lista_of_lines)):
            for column in range(len(lista_of_lines[line])):
                if lista_of_lines[line][column] == "2":
                    w = 1
                    h = 1
                    while lista_of_lines[line][column + w] == "1":
                        w += 1
                    while lista_of_lines[line + h][column] == "3":
                        h += 1
                    block = Block(((column * mc) + 17), ((line * ml) + 77), (w * mc), (h * ml))
                    self.__list_obstacles.append(block)

                if lista_of_lines[line][column] == "a" and t1 == 0:
                    t1 += 1
                    location3 = (((column * mc) + 39), ((line * ml) + 99))
                if lista_of_lines[line][column] == "b" and t2 == 0:
                    t2 += 1
                    location1 = (((column * mc) + 39), ((line * ml) + 99))
                if lista_of_lines[line][column] == "c" and t3 == 0:
                    t3 += 1
                    location2 = (((column * mc) + 39), ((line * ml) + 99))
                if lista_of_lines[line][column] == "d" and t4 == 0:
                    t4 += 1
                    location4 = (((column * mc) + 39), ((line * ml) + 99))
        self.__list_spawn = [location1, location2, location3, location4]

        archive.close()


class Block:
    def __init__(self, x, y, w, h):
        self.__x_position = x
        self.__y_position = y
        self.__width = w
        self.__height = h
        self.__rect = (x, y, w, h)

    def get_x(self) -> float:
        return self.__x_position

    def get_y(self) -> float:
        return self.__y_position

    def get_w(self):
        return self.__width

    def get_h(self):
        return self.__height

    def get_rect(self):
        return self.__rect
