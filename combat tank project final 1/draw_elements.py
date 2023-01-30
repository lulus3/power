from config import *


def draw_walls(surface, color, rects):
    pygame.draw.rect(surface, color, rects[0])
    pygame.draw.rect(surface, color, rects[1])
    pygame.draw.rect(surface, color, rects[2])
    pygame.draw.rect(surface, color, rects[3])


def victory_texts(font, size):
    victory_text1 = font.render("player red win", True, red, black)
    victory_text2 = font.render("player blue win", True, blue, black)
    victory_text3 = font.render("player yellow win", True, yellow, black)
    victory_text4 = font.render("player purple win", True, purple, black)
    victory_text1_rect = victory_text1.get_rect()
    victory_text2_rect = victory_text2.get_rect()
    victory_text3_rect = victory_text3.get_rect()
    victory_text4_rect = victory_text4.get_rect()
    victory_text1_rect.center = (size[0]/2, 350)
    victory_text2_rect.center = (size[0]/2, 350)
    victory_text3_rect.center = (size[0]/2, 350)
    victory_text4_rect.center = (size[0]/2, 350)
    vc1 = (victory_text1, victory_text1_rect)
    vc2 = (victory_text2, victory_text2_rect)
    vc3 = (victory_text3, victory_text3_rect)
    vc4 = (victory_text4, victory_text4_rect)
    list_vic = [vc1, vc2, vc3, vc4]
    return list_vic


def hud(font):
    hud_text1 = font.render("0", True, red, black)
    hud_text2 = font.render("0", True, blue, black)
    hud_text3 = font.render("0", True, yellow, black)
    hud_text4 = font.render("0", True, purple, black)
    hud_text1_rect = hud_text1.get_rect()
    hud_text2_rect = hud_text2.get_rect()
    hud_text3_rect = hud_text3.get_rect()
    hud_text4_rect = hud_text4.get_rect()
    hud_text1_rect.center = (40, 30)
    hud_text2_rect.center = (370, 30)
    hud_text3_rect.center = (740, 30)
    hud_text4_rect.center = (1110, 30)
    hd1 = [hud_text1, hud_text1_rect]
    hd2 = [hud_text2, hud_text2_rect]
    hd3 = [hud_text3, hud_text3_rect]
    hd4 = [hud_text4, hud_text4_rect]
    list_hud = [hd1, hd2, hd3, hd4]
    return list_hud


def draw_menu1(archive1, archive2, surface, font):
    image1 = pygame.image.load(archive1)
    image1_rect = image1.get_rect()
    image1_rect.center = (355, 350)
    surface.blit(image1, image1_rect)
    image2 = pygame.image.load(archive2)
    image2_rect = image2.get_rect()
    image2_rect.center = (1010, 350)
    surface.blit(image2, image2_rect)
    text = font.render("which arena will it be?", True, white, black)
    chose1 = font.render("1", True, white, black)
    chose2 = font.render("2", True, white, black)
    text_rect = text.get_rect()
    text_rect.center = (683, 100)
    surface.blit(text, text_rect)
    chose1_rect = chose1.get_rect()
    chose1_rect.center = (355, 183)
    surface.blit(chose1, chose1_rect)
    chose2_rect = chose2.get_rect()
    chose2_rect.center = (1010, 183)
    surface.blit(chose2, chose2_rect)


def draw_menu2(archive1, archive2, archive3, archive4, surface, font):
    list_archive = [archive1, archive2, archive3, archive4]
    x = 273
    for a in range(4):
        photo = pygame.image.load(list_archive[a])
        photo_rect = photo.get_rect()
        photo_rect.center = (x, 350)
        surface.blit(photo, photo_rect)
        x += 273
    text = font.render("how many players will play? min(2) max(4)", True, white, black)
    text_rect = text.get_rect()
    text_rect.center = (683, 100)
    surface.blit(text, text_rect)
