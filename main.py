from pygame.constants import *
import pygame as pg
import numpy as np
pg.init()

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BORDER_COLOR = (180, 132, 84)

drawing = False
stop = False
FPS = 30
CELL_LINE = 75
BORDER = 0
WIDTH = CELL_LINE * 8 + BORDER * 2
HEIGHT = CELL_LINE * 8 + BORDER * 2


class figure:
    def __init__(self, image, cell, color, type):
        assert color == 'white' or color == 'black', "Неверно указан цвет фигуры"
        assert type == 'castle' or type == 'horse' or type == 'officer' or type == 'queen' or type == 'king' or type == 'pawn', "Неверно указан тип фигуры"
        self.image = image
        self.x = (cell[1] + 8) % 8 * CELL_LINE
        self.y = (cell[0] + 8) % 8 * CELL_LINE
        self.start_pos = self.y // CELL_LINE, self.x // CELL_LINE
        self.color = color
        self.type = type
        self.click = False

    def draw(self):
        screen.blit(self.image, (self.x + BORDER, self.y + BORDER))

    def get_attack(self, chess_field, attack_self = False):
        output_field = np.zeros((8, 8))
        if self.type == 'pawn':
            try:
                if self.color == 'white':
                    if chess_field[self.y // CELL_LINE - 1][self.x // CELL_LINE - 1] != 0 and (chess_field[self.y // CELL_LINE - 1][self.x // CELL_LINE - 1] == 1 or chess_field[self.y // CELL_LINE - 1][self.x // CELL_LINE - 1].color != self.color or attack_self) and self.x // CELL_LINE - 1 >= 0 or attack_self:
                        output_field[self.y // CELL_LINE - 1][self.x // CELL_LINE - 1] = 1
                    if chess_field[self.y // CELL_LINE - 1][self.x // CELL_LINE] == 0 and not attack_self:
                        if self.y // CELL_LINE == 6 and chess_field[self.y // CELL_LINE - 2][self.x // CELL_LINE] == 0:
                            output_field[self.y // CELL_LINE - 2][self.x // CELL_LINE] = 1
                        output_field[self.y // CELL_LINE - 1][self.x // CELL_LINE] = 1
                    if chess_field[self.y // CELL_LINE - 1][self.x // CELL_LINE + 1] != 0 and (chess_field[self.y // CELL_LINE - 1][self.x // CELL_LINE + 1] == 1 or chess_field[self.y // CELL_LINE - 1][self.x // CELL_LINE + 1].color != self.color or attack_self) and self.x // CELL_LINE + 1 < 8 or attack_self:
                        output_field[self.y // CELL_LINE - 1][self.x // CELL_LINE + 1] = 1
                if self.color == 'black':
                    if chess_field[self.y // CELL_LINE + 1][self.x // CELL_LINE - 1] != 0 and (chess_field[self.y // CELL_LINE + 1][self.x // CELL_LINE - 1] == 1 or chess_field[self.y // CELL_LINE + 1][self.x // CELL_LINE - 1].color != self.color or attack_self) and self.x // CELL_LINE - 1 >= 0 or attack_self:
                        output_field[self.y // CELL_LINE + 1][self.x // CELL_LINE - 1] = 1
                    if chess_field[self.y // CELL_LINE + 1][self.x // CELL_LINE] == 0 and not attack_self:
                        if self.y // CELL_LINE == 1 and chess_field[self.y // CELL_LINE + 2][self.x // CELL_LINE] == 0:
                            output_field[self.y // CELL_LINE + 2][self.x // CELL_LINE] = 1
                        output_field[self.y // CELL_LINE + 1][self.x // CELL_LINE] = 1
                    if chess_field[self.y // CELL_LINE + 1][self.x // CELL_LINE + 1] != 0 and (chess_field[self.y // CELL_LINE + 1][self.x // CELL_LINE + 1] == 1 or chess_field[self.y // CELL_LINE + 1][self.x // CELL_LINE + 1].color != self.color or attack_self) and self.x // CELL_LINE + 1 < 8 or attack_self:
                        output_field[self.y // CELL_LINE + 1][self.x // CELL_LINE + 1] = 1
            except IndexError:
                pass

        if self.type == 'castle':
            for i in range(self.x // CELL_LINE+1, 8, 1):
                output_field[self.y // CELL_LINE][i] = 1
                if chess_field[self.y // CELL_LINE][i] != 0:
                    if chess_field[self.y // CELL_LINE][i] != 1 and chess_field[self.y // CELL_LINE][i].color == self.color and not attack_self:
                        output_field[self.y // CELL_LINE][i] = 0
                        break
                    elif chess_field[self.y // CELL_LINE][i] == 1 or (attack_self and chess_field[self.y // CELL_LINE][i].color == self.color) or chess_field[self.y // CELL_LINE][i].type != 'king':
                        break
            for i in range(self.y // CELL_LINE+1, 8, 1):
                output_field[i][self.x // CELL_LINE] = 1
                if chess_field[i][self.x // CELL_LINE] != 0:
                    if chess_field[i][self.x // CELL_LINE] != 1 and chess_field[i][self.x // CELL_LINE].color == self.color and not attack_self:
                        output_field[i][self.x // CELL_LINE] = 0
                        break
                    elif chess_field[i][self.x // CELL_LINE] == 1 or (attack_self and chess_field[i][self.x // CELL_LINE].color == self.color) or chess_field[i][self.x // CELL_LINE].type != 'king':
                        break
            for i in range(self.x // CELL_LINE-1, -1, -1):
                output_field[self.y // CELL_LINE][i] = 1
                if chess_field[self.y // CELL_LINE][i] != 0:
                    if chess_field[self.y // CELL_LINE][i] != 1 and chess_field[self.y // CELL_LINE][i].color == self.color and not attack_self:
                        output_field[self.y // CELL_LINE][i] = 0
                        break
                    elif chess_field[self.y // CELL_LINE][i] == 1 or (attack_self and chess_field[self.y // CELL_LINE][i].color == self.color) or chess_field[self.y // CELL_LINE][i].type != 'king':
                        break
            for i in range(self.y // CELL_LINE-1, -1, -1):
                output_field[i][self.x // CELL_LINE] = 1
                if chess_field[i][self.x // CELL_LINE] != 0:
                    if chess_field[i][self.x // CELL_LINE] != 1 and chess_field[i][self.x // CELL_LINE].color == self.color and not attack_self:
                        output_field[i][self.x // CELL_LINE] = 0
                        break
                    elif chess_field[i][self.x // CELL_LINE] == 1 or (attack_self and chess_field[i][self.x // CELL_LINE].color == self.color) or chess_field[i][self.x // CELL_LINE].type != 'king':
                        break

        if self.type == 'horse':
            if self.y // CELL_LINE - 2 >= 0:
                for i in range(-1, 2, 2):
                    if self.x // CELL_LINE + i < 8 and self.x // CELL_LINE + i >= 0:
                        output_field[self.y // CELL_LINE - 2][self.x // CELL_LINE + i] = 1
                        if chess_field[self.y // CELL_LINE - 2][self.x // CELL_LINE + i] != 0:
                            if chess_field[self.y // CELL_LINE - 2][self.x // CELL_LINE + i] == 1 or chess_field[self.y // CELL_LINE - 2][self.x // CELL_LINE + i].color == self.color and not attack_self:
                                output_field[self.y // CELL_LINE - 2][self.x // CELL_LINE + i] = 0
            if self.y // CELL_LINE + 2 < 8:
                for i in range(-1, 2, 2):
                    if self.x // CELL_LINE + i < 8 and self.x // CELL_LINE + i >= 0:
                        output_field[self.y // CELL_LINE + 2][self.x // CELL_LINE + i] = 1
                        if chess_field[self.y // CELL_LINE + 2][self.x // CELL_LINE + i] != 0:
                            if chess_field[self.y // CELL_LINE + 2][self.x // CELL_LINE + i] == 1 or chess_field[self.y // CELL_LINE + 2][self.x // CELL_LINE + i].color == self.color and not attack_self:
                                output_field[self.y // CELL_LINE + 2][self.x // CELL_LINE + i] = 0
            if self.x // CELL_LINE - 2 >= 0:
                for i in range(-1, 2, 2):
                    if self.y // CELL_LINE + i < 8 and self.y // CELL_LINE + i >= 0:
                        output_field[self.y // CELL_LINE + i][self.x // CELL_LINE - 2] = 1
                        if chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE - 2] != 0:
                            if chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE - 2] == 1 or chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE - 2].color == self.color and not attack_self:
                                output_field[self.y // CELL_LINE + i][self.x // CELL_LINE - 2] = 0
            if self.x // CELL_LINE + 2 < 8:
                for i in range(-1, 2, 2):
                    if self.y // CELL_LINE + i < 8 and self.y // CELL_LINE + i >= 0:
                        output_field[self.y // CELL_LINE + i][self.x // CELL_LINE + 2] = 1
                        if chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE + 2] != 0:
                            if chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE + 2] == 1 or chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE + 2].color == self.color and not attack_self:
                                output_field[self.y // CELL_LINE + i][self.x // CELL_LINE + 2] = 0

        if self.type == 'officer':
            i = 1
            while self.x // CELL_LINE - i >= 0 and self.y // CELL_LINE - i >= 0:
                output_field[self.y // CELL_LINE - i][self.x // CELL_LINE - i] = 1

                if chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE - i] != 0:
                    if chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE - i] != 1 and chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE - i].color == self.color and not attack_self:
                        output_field[self.y // CELL_LINE - i][self.x // CELL_LINE - i] = 0
                        break
                    else:
                        if chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE - i] == 1 or (attack_self and chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE - i].color == self.color) or chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE - i].type != 'king':
                            break
                i += 1
            i = 1
            while self.x // CELL_LINE + i < 8 and self.y // CELL_LINE - i >= 0:
                output_field[self.y // CELL_LINE - i][self.x // CELL_LINE + i] = 1

                if chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE + i] != 0:
                    if chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE + i] != 1 and chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE + i].color == self.color and not attack_self:
                        output_field[self.y // CELL_LINE - i][self.x // CELL_LINE + i] = 0
                        break
                    else:
                        if chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE + i] == 1 or (attack_self and chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE + i].color == self.color) or chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE + i].type != 'king':
                            break
                i += 1
            i = 1
            while self.x // CELL_LINE + i < 8 and self.y // CELL_LINE + i < 8:
                output_field[self.y // CELL_LINE + i][self.x // CELL_LINE + i] = 1

                if chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE + i] != 0:
                    if chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE + i] != 1 and chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE + i].color == self.color and not attack_self:
                        output_field[self.y // CELL_LINE + i][self.x // CELL_LINE + i] = 0
                        break
                    else:
                        if chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE + i] == 1 or (attack_self and chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE + i].color == self.color) or chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE + i].type != 'king':
                            break
                i += 1
            i = 1
            while self.x // CELL_LINE - i >= 0 and self.y // CELL_LINE + i < 8:
                output_field[self.y // CELL_LINE + i][self.x // CELL_LINE - i] = 1

                if chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE - i] != 0:
                    if chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE - i] != 1 and chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE - i].color == self.color and not attack_self:
                        output_field[self.y // CELL_LINE + i][self.x // CELL_LINE - i] = 0
                        break
                    else:
                        if chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE - i] == 1 or (attack_self and chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE - i].color == self.color) or chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE - i].type != 'king':
                            break
                i += 1

        if self.type == 'queen':
            for i in range(self.x // CELL_LINE+1, 8, 1):
                output_field[self.y // CELL_LINE][i] = 1
                if chess_field[self.y // CELL_LINE][i] != 0:
                    if chess_field[self.y // CELL_LINE][i] != 1 and chess_field[self.y // CELL_LINE][i].color == self.color and not attack_self:
                        output_field[self.y // CELL_LINE][i] = 0
                        break
                    elif chess_field[self.y // CELL_LINE][i] == 1 or (attack_self and chess_field[self.y // CELL_LINE][i].color == self.color) or chess_field[self.y // CELL_LINE][i].type != 'king':
                        break
            for i in range(self.y // CELL_LINE+1, 8, 1):
                output_field[i][self.x // CELL_LINE] = 1
                if chess_field[i][self.x // CELL_LINE] != 0:
                    if chess_field[i][self.x // CELL_LINE] != 1 and chess_field[i][self.x // CELL_LINE].color == self.color and not attack_self:
                        output_field[i][self.x // CELL_LINE] = 0
                        break
                    elif chess_field[i][self.x // CELL_LINE] == 1 or (attack_self and chess_field[i][self.x // CELL_LINE].color == self.color) or chess_field[i][self.x // CELL_LINE].type != 'king':
                        break
            for i in range(self.x // CELL_LINE-1, -1, -1):
                output_field[self.y // CELL_LINE][i] = 1
                if chess_field[self.y // CELL_LINE][i] != 0:
                    if chess_field[self.y // CELL_LINE][i] != 1 and chess_field[self.y // CELL_LINE][i].color == self.color and not attack_self:
                        output_field[self.y // CELL_LINE][i] = 0
                        break
                    elif chess_field[self.y // CELL_LINE][i] == 1 or (attack_self and chess_field[self.y // CELL_LINE][i].color == self.color) or chess_field[self.y // CELL_LINE][i].type != 'king':
                        break
            for i in range(self.y // CELL_LINE-1, -1, -1):
                output_field[i][self.x // CELL_LINE] = 1
                if chess_field[i][self.x // CELL_LINE] != 0:
                    if chess_field[i][self.x // CELL_LINE] != 1 and chess_field[i][self.x // CELL_LINE].color == self.color and not attack_self:
                        output_field[i][self.x // CELL_LINE] = 0
                        break
                    elif chess_field[i][self.x // CELL_LINE] == 1 or (attack_self and chess_field[i][self.x // CELL_LINE].color == self.color) or chess_field[i][self.x // CELL_LINE].type != 'king':
                        break

            i = 1
            while self.x // CELL_LINE - i >= 0 and self.y // CELL_LINE - i >= 0:
                output_field[self.y // CELL_LINE - i][self.x // CELL_LINE - i] = 1

                if chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE - i] != 0:
                    if chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE - i] != 1 and chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE - i].color == self.color and not attack_self:
                        output_field[self.y // CELL_LINE - i][self.x // CELL_LINE - i] = 0
                        break
                    else:
                        if chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE - i] == 1 or (attack_self and chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE - i].color == self.color) or chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE - i].type != 'king':
                            break
                i += 1
            i = 1
            while self.x // CELL_LINE + i < 8 and self.y // CELL_LINE - i >= 0:
                output_field[self.y // CELL_LINE - i][self.x // CELL_LINE + i] = 1

                if chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE + i] != 0:
                    if chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE + i] != 1 and chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE + i].color == self.color and not attack_self:
                        output_field[self.y // CELL_LINE - i][self.x // CELL_LINE + i] = 0
                        break
                    else:
                        if chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE + i] == 1 or (attack_self and chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE + i].color == self.color) or chess_field[self.y // CELL_LINE - i][self.x // CELL_LINE + i].type != 'king':
                            break
                i += 1
            i = 1
            while self.x // CELL_LINE + i < 8 and self.y // CELL_LINE + i < 8:
                output_field[self.y // CELL_LINE + i][self.x // CELL_LINE + i] = 1

                if chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE + i] != 0:
                    if chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE + i] != 1 and chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE + i].color == self.color and not attack_self:
                        output_field[self.y // CELL_LINE + i][self.x // CELL_LINE + i] = 0
                        break
                    else:
                        if chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE + i] == 1 or (attack_self and chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE + i].color == self.color) or chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE + i].type != 'king':
                            break
                i += 1
            i = 1
            while self.x // CELL_LINE - i >= 0 and self.y // CELL_LINE + i < 8:
                output_field[self.y // CELL_LINE + i][self.x // CELL_LINE - i] = 1

                if chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE - i] != 0:
                    if chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE - i] != 1 and chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE - i].color == self.color and not attack_self:
                        output_field[self.y // CELL_LINE + i][self.x // CELL_LINE - i] = 0
                        break
                    else:
                        if chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE - i] == 1 or (attack_self and chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE - i].color == self.color) or chess_field[self.y // CELL_LINE + i][self.x // CELL_LINE - i].type != 'king':
                            break
                i += 1

        if self.type == 'king':
            for i in range(self.x // CELL_LINE - 1, self.x // CELL_LINE + 2):
                for j in range(self.y // CELL_LINE - 1, self.y // CELL_LINE + 2):
                    if (i < 0 or i > 7) or (j < 0 or j > 7):
                        continue
                    if (i != self.x // CELL_LINE or j != self.y // CELL_LINE):
                        output_field[j][i] = 1
                        if chess_field[j][i] != 0 and (chess_field[j][i] == 1 or chess_field[j][i].color == self.color) and not attack_self:
                            output_field[j][i] = 0
            if not attack_self:
                try:
                    if (self.y // CELL_LINE, self.x // CELL_LINE) == self.start_pos and (chess_field[self.start_pos[0]][0].type == 'castle' or chess_field[self.start_pos[0]][7].type == 'castle'):
                        lad = chess_field[self.start_pos[0]][0], chess_field[self.start_pos[0]][7]
                        if lad[0].x // CELL_LINE == 0 and chess_field[self.start_pos[0]][1] == 0 and chess_field[self.start_pos[0]][2] == 0 and chess_field[self.start_pos[0]][3] == 0:
                            output_field[self.y // CELL_LINE][self.x // CELL_LINE - 2] = 1
                        if lad[1].x // CELL_LINE == 7 and chess_field[self.start_pos[0]][6] == 0 and chess_field[self.start_pos[0]][5] == 0:
                            output_field[self.y // CELL_LINE][self.x // CELL_LINE + 2] = 1
                except AttributeError:
                    pass
                sum = np.zeros((8, 8))
                for i in range(len(chess_field)):
                    for j in range(len(chess_field[i])):
                        if chess_field[i][j] != 0 and chess_field[i][j] != 1 and chess_field[i][j].color != self.color:
                             sum = sum + chess_field[i][j].get_attack(chess_field, True)
                output_field = sum - output_field
                output_field[output_field >= 0] = 0
                output_field[output_field < 0] = 1

        return output_field

chess_field = [[0 for j in range(8)] for i in range(8)]
clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Шахматы')
icon = pg.image.load('images/icon.png')
icon.set_colorkey(WHITE)
pg.display.set_icon(icon)

castle_black = pg.image.load('images/Ладья черных.png')
horse_black = pg.image.load('images/Конь черных.png')
officer_black = pg.image.load('images/Офицер черных.png')
queen_black = pg.image.load('images/Королева черных.png')
king_black = pg.image.load('images/Король черных.png')
pawn_black = pg.image.load('images/Пешка черных.png')

castle_white = pg.image.load('images/Ладья белых.png')
horse_white = pg.image.load('images/Конь белых.png')
officer_white = pg.image.load('images/Офицер белых.png')
queen_white = pg.image.load('images/Королева белых.png')
king_white = pg.image.load('images/Король белых.png')
pawn_white = pg.image.load('images/Пешка белых.png')

castle_white.set_colorkey(WHITE)
horse_white.set_colorkey(WHITE)
officer_white.set_colorkey(WHITE)
queen_white.set_colorkey(WHITE)
king_white.set_colorkey(WHITE)
pawn_white.set_colorkey(WHITE)

castle_black.set_colorkey(WHITE)
horse_black.set_colorkey(WHITE)
officer_black.set_colorkey(WHITE)
queen_black.set_colorkey(WHITE)
king_black.set_colorkey(WHITE)
pawn_black.set_colorkey(WHITE)

chess_field[0][0], chess_field[0][-1] = figure(castle_black, (0, 0), 'black', 'castle'), figure(castle_black, (0, -1), 'black', 'castle')
chess_field[-1][0], chess_field[-1][-1] = figure(castle_white, (-1, 0), 'white', 'castle'), figure(castle_white, (-1, -1), 'white', 'castle')

chess_field[0][1], chess_field[0][-2] = figure(horse_black, (0, 1), 'black', 'horse'), figure(horse_black, (0, -2), 'black', 'horse')
chess_field[-1][1], chess_field[-1][-2] = figure(horse_white, (-1, 1), 'white', 'horse'), figure(horse_white, (-1, -2), 'white', 'horse')

chess_field[0][2], chess_field[0][-3] = figure(officer_black, (0, 2), 'black', 'officer'), figure(officer_black, (0, -3), 'black', 'officer')
chess_field[-1][2], chess_field[-1][-3] = figure(officer_white, (-1, 2), 'white', 'officer'), figure(officer_white, (-1, -3), 'white', 'officer')

chess_field[0][3] = figure(queen_black, (0, 3), 'black', 'queen')
chess_field[-1][3] = figure(queen_white, (-1, 3), 'white', 'queen')

chess_field[0][4] = figure(king_black, (0, 4), 'black', 'king')
chess_field[-1][4] = figure(king_white, (-1, 4), 'white', 'king')
move = 'white'
step = False
steped = []

for i in range(8):
    chess_field[1][i] = figure(pawn_black, (1, i), 'black', 'pawn')
    chess_field[-2][i] = figure(pawn_white, (-2, i), 'white', 'pawn')

while True:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            if chess_field[event.pos[1] // CELL_LINE][event.pos[0] // CELL_LINE] != 0 and chess_field[event.pos[1] // CELL_LINE][event.pos[0] // CELL_LINE].color == move:
                attack = chess_field[event.pos[1] // CELL_LINE][event.pos[0] // CELL_LINE].get_attack(chess_field)
                drawing = True
                atacking = (event.pos[1] // CELL_LINE, event.pos[0] // CELL_LINE)
            if drawing and attack[event.pos[1] // CELL_LINE][event.pos[0] // CELL_LINE]:
                if chess_field[atacking[0]][atacking[1]].type == 'king':
                    if chess_field[atacking[0]][atacking[1]].x - event.pos[0] // CELL_LINE * CELL_LINE == 2 * CELL_LINE:
                        chess_field[atacking[0]][3] = chess_field[atacking[0]][0]
                        chess_field[atacking[0]][0] = 0
                        chess_field[atacking[0]][3].x = 3 * CELL_LINE
                    if chess_field[atacking[0]][atacking[1]].x - event.pos[0] // CELL_LINE * CELL_LINE == -(2 * CELL_LINE):
                        chess_field[atacking[0]][5] = chess_field[atacking[0]][7]
                        chess_field[atacking[0]][7] = 0
                        chess_field[atacking[0]][5].x = 5 * CELL_LINE
                chess_field[event.pos[1] // CELL_LINE][event.pos[0] // CELL_LINE] = chess_field[atacking[0]][atacking[1]]
                chess_field[event.pos[1] // CELL_LINE][event.pos[0] // CELL_LINE].x = event.pos[0] // CELL_LINE * CELL_LINE
                chess_field[event.pos[1] // CELL_LINE][event.pos[0] // CELL_LINE].y = event.pos[1] // CELL_LINE * CELL_LINE
                chess_field[atacking[0]][atacking[1]] = 0
                drawing = False
                if move == 'white':
                    move = 'black'
                else:
                    move = 'white'

        if event.type == KEYDOWN and stop:
            if event.key == K_a:
                chess_field[stoping[0]][stoping[1]].type = 'queen'
                if chess_field[stoping[0]][stoping[1]].color == 'white':
                    chess_field[stoping[0]][stoping[1]].image = queen_white
                if chess_field[stoping[0]][stoping[1]].color == 'black':
                    chess_field[stoping[0]][stoping[1]].image = queen_black
                stop = False
            if event.key == K_k:
                chess_field[stoping[0]][stoping[1]].type = 'castle'
                if chess_field[stoping[0]][stoping[1]].color == 'white':
                    chess_field[stoping[0]][stoping[1]].image = castle_white
                if chess_field[stoping[0]][stoping[1]].color == 'black':
                    chess_field[stoping[0]][stoping[1]].image = castle_black
                stop = False
            if event.key == K_r:
                chess_field[stoping[0]][stoping[1]].type = 'horse'
                if chess_field[stoping[0]][stoping[1]].color == 'white':
                    chess_field[stoping[0]][stoping[1]].image = horse_white
                if chess_field[stoping[0]][stoping[1]].color == 'black':
                    chess_field[stoping[0]][stoping[1]].image = horse_black
                stop = False
            if event.key == K_j:
                chess_field[stoping[0]][stoping[1]].type = 'officer'
                if chess_field[stoping[0]][stoping[1]].color == 'white':
                    chess_field[stoping[0]][stoping[1]].image = officer_white
                if chess_field[stoping[0]][stoping[1]].color == 'black':
                    chess_field[stoping[0]][stoping[1]].image = officer_black
                stop = False

    for i in range(len(chess_field)):
        for j in range(len(chess_field[i])):
            if (i+j)%2==0:
                pg.draw.rect(screen, WHITE, (j * CELL_LINE + BORDER, i * CELL_LINE + BORDER, CELL_LINE, CELL_LINE))
            else:
                pg.draw.rect(screen, BLACK, (j * CELL_LINE + BORDER, i * CELL_LINE + BORDER, CELL_LINE, CELL_LINE))

    for i in range(len(chess_field)):
        for j in range(len(chess_field[i])):
            if chess_field[i][j] != 0:
                chess_field[i][j].draw()
                if i == 0 or i == 7 and chess_field[i][j].type == 'pawn':
                    stop = True
                    stoping = (i, j)

                if chess_field[i][j].type == 'king' and chess_field[i][j].color == move:
                    steped = []
                    pos_king = i, j
                    for k in range(len(chess_field)):
                        for l in range(len(chess_field[k])):
                            if chess_field[k][l] != 0 and chess_field[k][l].get_attack(chess_field)[i][j]:
                                steped.append((k, l))
                                step = True
                    if not steped:
                        step = False
                        steped = []

    if drawing:
        for i in range(len(attack)):
            for j in range(len(attack[i])):
                if attack[i][j]:
                    if step and chess_field[atacking[0]][atacking[1]].type != 'king':
                        ij = chess_field[i][j]
                        chess_field[i][j] = 1
                        for steper in steped:
                            if chess_field[steper[0]][steper[1]] != 1 and chess_field[steper[0]][steper[1]].get_attack(chess_field)[pos_king]:
                                attack[i][j] = 0
                                break
                        chess_field[i][j] = ij
                    elif chess_field[atacking[0]][atacking[1]].type != 'king':
                        sum = np.zeros((8, 8))
                        ij = chess_field[i][j]
                        ji = chess_field[atacking[0]][atacking[1]]
                        chess_field[i][j] = 1
                        chess_field[atacking[0]][atacking[1]] = 0
                        for k in range(len(chess_field)):
                            for l in range(len(chess_field[i])):
                                if chess_field[k][l] != 0 and chess_field[k][l] != 1 and chess_field[k][l].get_attack(chess_field)[pos_king]:
                                    attack[i][j] = 0
                                    break
                        chess_field[i][j] = ij
                        chess_field[atacking[0]][atacking[1]] = ji

                    if attack[i][j]:
                        pg.draw.circle(screen, GREEN, (j * CELL_LINE + CELL_LINE // 2, i * CELL_LINE + CELL_LINE // 2), CELL_LINE // 4)

    pg.display.update()
    screen.fill(BORDER_COLOR)