import pygame
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Legend:
    def __init__(self, x, y, width, height, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.elements = []

    def draw(self):
        pygame.draw.rect(self.screen, WHITE,
                         (self.x, self.y, self.width, self.height))
        c = 0
        for element in self.elements:
            self.screen.blit(element, (self.x + 10, self.y +
                             c * 200 + 10))
            c += 1


def display(board, screen, legend):
    box = 1200 // 4
    padding = 10
    font = pygame.font.SysFont("Verdana", 69, bold=True)
    grid_x = (screen.get_width() - 4 * box) // 2 - 300
    grid_y = (screen.get_height() - 4 * box) // 2 - 100

    for i in range(4):
        for j in range(4):
            colour = [237, 194, 46]
            pygame.draw.rect(screen, colour, (grid_x + j * box + padding,
                                              grid_y + i * box + padding,
                                              box - 2 * padding,
                                              box - 2 * padding), 0)
            if board[i][j] != 0:
                if board[i][j] in (2, 4):
                    text_colour = [119, 110, 101]
                else:
                    text_colour = [249, 246, 242]
                
                screen.blit(font.render("{:>4}".format(
                    board[i][j]), 1, text_colour),
                    
                    (j * box + 2.5 * padding, i * box + 7 * padding))
    
    left_text = font.render("Z", 1, WHITE)
    screen.blit(left_text, (grid_x - left_text.get_width() -
                padding, grid_y + box * 2 - left_text.get_height() // 2))

    right_text = font.render("H", 1, WHITE)
    screen.blit(right_text, (grid_x + box * 4 + padding,
                grid_y + box * 2 - right_text.get_height() // 2))

    top_text = font.render("I", 1, WHITE)
    screen.blit(top_text, (grid_x + box * 2 - top_text.get_width() //
                2, grid_y - top_text.get_height() - padding))

    bottom_text = font.render("X", 1, WHITE)
    screen.blit(bottom_text, (grid_x + box * 2 -
                bottom_text.get_width() // 2, grid_y + box * 4 + padding))

    legend.draw()
    pygame.display.update()


def start(screen, SCREEN_WIDTH):
    running = True
    font = pygame.font.SysFont("Verdana", 69, bold=True)
    board = [[0] * 4 for _ in range(4)]
    legend = Legend(SCREEN_WIDTH * 0.75, 0, SCREEN_WIDTH *
                    0.25, SCREEN_HEIGHT, screen)
    dynamic_element = font.render("        LEGEND", 1, BLACK)
    legend.elements.append(dynamic_element)
    dynamic_element2 = font.render("        SHOGO", 1, BLACK)
    legend.elements.append(dynamic_element2)
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        screen.fill(BLACK)
        level_text = font.render("LEVEL : 0", 1, WHITE)
        screen.blit(level_text, (SCREEN_WIDTH // 2 -
                    level_text.get_width() // 2, 10))
        display(board, screen, legend)

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    SCREEN_WIDTH = 2500
    SCREEN_HEIGHT = 2000
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Zenith Zealots")

    start(screen, SCREEN_WIDTH)

    pygame.quit()
