import sys

import pygame
from pygame.locals import *

import game

import subprocess

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Button():
    """
    Class to create a new button in pygame window.
    """
    # initialise the button

    def __init__(self, colour, x, y, width, height, text=""):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    # draw the button on the screen
    def draw(self, win, text_col, font):
        drawRoundRect(win, self.colour, (self.x, self.y,
                                         self.width, self.height))

        if self.text != "":
            text = font.render(self.text, 1, text_col)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    # check if the mouse is positioned over the button
    def isOver(self, pos):
        # pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def drawRoundRect(surface, colour, rect, radius=0.4):
    """
    Draw an antialiased rounded filled rectangle on screen

    Parameters:
        surface (pygame.Surface): destination
        colour (tuple): RGB values for rectangle fill colour
        radius (float): 0 <= radius <= 1
    """

    rect = Rect(rect)
    colour = Color(*colour)
    alpha = colour.a
    colour.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, SRCALPHA)

    circle = pygame.Surface([min(rect.size) * 3] * 2, SRCALPHA)
    pygame.draw.ellipse(circle, BLACK, circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(
        circle, [int(min(rect.size)*radius)]*2)

    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)

    rectangle.fill(BLACK, rect.inflate(-radius.w, 0))
    rectangle.fill(BLACK, rect.inflate(0, -radius.h))

    rectangle.fill(colour, special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=BLEND_RGBA_MIN)

    surface.blit(rectangle, pos)


def showMenu(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    level_0 = Button(
        tuple([237, 194, 46]), SCREEN_WIDTH // 2 - 300 - 150, SCREEN_HEIGHT // 2 - 500 , 300, 300, "Level 0")
    level_1 = Button(
        tuple([237, 194, 46]), SCREEN_WIDTH // 2 + 300 - 150, SCREEN_HEIGHT // 2 - 500 , 300, 300, "Level 1")
    running = True
    current_level = 0
    level_selected = False
    play = Button(tuple([237, 194, 46]),
                  SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 300, "play")
    while running:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level_0.isOver(pos):
                    level_0.colour = tuple([246,94,59])
                    current_level = 0
                    level_selected = True

                if level_1.isOver(pos):
                    level_1.colour = tuple([246,94,59])
                    current_level = 1
                    level_selected = True

                if play.isOver(pos):
                    play.colour = tuple([246,94,59])
                    if level_selected != False:
                        subprocess.call(
                            "python /home/shogo/master/qc/Zenith-zealots/Game/game.py", shell=True)

        screen.fill(BLACK)
        font = pygame.font.SysFont("Verdana", 69, bold=True)
        font1 = pygame.font.SysFont("Verdana", 69, bold=True)

        theme_text = font.render("WELCOME ", 1, WHITE)
        screen.blit(theme_text, (SCREEN_WIDTH / 2 - 150, 200))
        level_0.draw(screen, BLACK, font1)
        level_1.draw(screen, BLACK, font1)
        play.draw(screen, BLACK, font1)

        pygame.display.update()

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    SCREEN_WIDTH = 2500
    SCREEN_HEIGHT = 2500
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Zenith Zealots")

    showMenu(screen, SCREEN_WIDTH,SCREEN_HEIGHT)

    pygame.quit()
