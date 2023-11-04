import pygame
from pygame.locals import *

# Import necessary libraries from Qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
import numpy as np

# Import the necessary functions for visualizing quantum states
from qiskit.visualization import plot_bloch_multivector

# Import the State vector class from Qiskit's quantum information module
from qiskit.quantum_info import Statevector
import numpy as np
import random
import json

# import helper functions
from HelperFunctions import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def process(qc_map, qc_loc, qc_matrix, dir, gates, state_vector):
    # first we will shift the matrix
    shift(qc_matrix, dir)

    # now we will operate the gates
    gate_op(dir, qc_map, qc_loc, qc_matrix, gates)

    # now we will merge the qubits
    merge(qc_map, qc_loc, qc_matrix, dir, state_vector)

    shift(qc_matrix, dir)

LevelInfo = json.load(open("levels.json", "r"))
q_circuts = {}
q_location = {}
number_of_levels = LevelInfo["Levels"]["Number"]

wall_gate = {
    0: 'H',
    1: 'X',
    2: 'I',
    3: 'Z'
}

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

    q_circuts = {}
    q_location = {}

    number_of_q_circuits = LevelInfo["Levels"]["Info"][0]["Qubits"]["number"]

    for _ in range(number_of_q_circuits):
        q = QuantumCircuit(1)
        gates = LevelInfo["Levels"]["Info"][0]["Qubits"]["Info"][_]["Gates"]
        q_location[_] = LevelInfo["Levels"]["Info"][0]["Qubits"]["Info"][_]["Location"]
        for n_ in gates:
            print(n_)
            if n_ == 'h':
                q.h(0)
            elif n_ == 'x':
                q.x(0)
            elif n_ == 'z':
                q.z(0)
        q_circuts[_] = q


    board = matrix_gen(q_location)

    state_vector_dict = {}
    for _ in range(number_of_q_circuits):
        state_vector_dict[_] = Statevector(q_circuts[_])

    
    qc_map = {}

    for _ in range(number_of_q_circuits):
        qc_map[_] = q_circuts[_]

    legend = Legend(SCREEN_WIDTH * 0.75, 0, SCREEN_WIDTH *
                    0.25, SCREEN_HEIGHT, screen)
    dynamic_element = font.render("        LEGEND", 1, BLACK)
    legend.elements.append(dynamic_element)

    for _ in range(number_of_q_circuits):
        for n_ in range(2):
            legend.elements.append(font.render(state_vector_dict[_][n_],1,BLACK))
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            process(qc_map, q_location, board, 2, wall_gate, state_vector_dict)
        elif pressed_keys[K_DOWN]:
            process(qc_map, q_location, board, 3, wall_gate, state_vector_dict)
        elif pressed_keys[K_LEFT]:
            process(qc_map, q_location, board, 0, wall_gate, state_vector_dict)
        elif pressed_keys[K_RIGHT]:
            process(qc_map, q_location, board, 1, wall_gate, state_vector_dict)
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
