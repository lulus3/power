def creat_arena(file_name):
    list_of_rect = []
    mc = 1332/222
    ml = 620/40
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
                rect = (((column * mc) + 17), ((line * ml) + 77), (w * mc), (h * ml))
                list_of_rect.append(rect)
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
    list_spawn_position = [location1, location2, location3, location4]

    archive.close()
    return list_of_rect, list_spawn_position
