import sys
import pygame
from pygame.locals import *
from colors import *
import math


pygame.init()

space_dim = 100
screen_dim = space_dim * 8


screen = pygame.display.set_mode((screen_dim, screen_dim))
screen_rect = screen.get_rect()
pygame.display.set_caption("Checkers")
fontobj = pygame.font.Font('freesansbold.ttf', 32)

clock = pygame.time.Clock()
FPS = 30


class BoardSpace(object):
    def __init__(self, x, y):
        self.rect = pygame.rect.Rect((x, y, space_dim, space_dim))

    def draw(self, surface, color):
        pygame.draw.rect(screen, color, self.rect)


class RedPieces(object):
    def __init__(self, x, y):
        self.pos = (x, y)
        self.radius = 25
        self.scale = 1

    def clicked(self, move):
        p = pygame.mouse.get_pos()
        dist = piece_mouse_hover(self.pos[0], self.pos[1])
        if dist < piece_rad:
            self.pos = p
        self.draw(screen, piece_rad)

    def draw(self, surface, radius):
        pygame.draw.circle(screen, red, self.pos, radius)


class BluePieces(object):
    def __init__(self, x, y):
        self.pos = (x, y)

    def draw(self, surface):
        pygame.draw.circle(screen, blue, self.pos, 25)


rlist = []
board_list = []
color_list = []
piece_rad = 25


def create_game_board():
    game_color1 = black
    game_color2 = white
    x = 0
    color1 = game_color1
    color2 = game_color2
    y = 0
    for space in range(64):
        # print(f'({space_dim * x}, {space_dim * y})')
        space = BoardSpace(space_dim * x, space_dim * y)
        board_list.append(space)
        if x % 2 == 0:
            color = color1
        else:
            color = color2
        space.draw(screen, color)
        color_list.append(color)
        if color == black and y < 3:
            r = RedPieces((space_dim * x) + 50, (space_dim * y) + 50)
            rlist.append(r)
        elif color == black and y > 4:
            r = BluePieces((space_dim * x) + 50, (space_dim * y) + 50)
            r.draw(screen)
        x += 1
        if x > 7:
            x = 0
            y += 1
            if y % 2 != 0:
                color1 = game_color2
                color2 = game_color1
            else:
                color1 = game_color1
                color2 = game_color2


def piece_mouse_hover(x, y):
    p = pygame.mouse.get_pos()
    q = (x, y)
    dist = math.dist(p, q)
    return dist


angle = 0
scale = 1
moving = False


def main():
    global piece_rad, moving
    create_game_board()
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            for space in board_list:
                space.draw(screen, color_list[board_list.index(space)])

            for piece in rlist:
                po = piece.pos
                p = pygame.mouse.get_pos()
                dist = piece_mouse_hover(piece.pos[0], piece.pos[1])
                if dist < piece_rad:
                    piece_rad = 35
                else:
                    piece_rad = 25
                piece.draw(screen, piece_rad)

                if event.type == MOUSEBUTTONDOWN:
                    moving = True

                    dist = piece_mouse_hover(piece.pos[0], piece.pos[1])
                    if dist < piece_rad and moving is True:
                        piece.pos = p
                    piece.draw(screen, piece_rad)

                elif event.type == MOUSEBUTTONUP:
                    piece.pos = po
                piece.draw(screen, piece_rad)


        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
