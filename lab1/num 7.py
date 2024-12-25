import pygame
import numpy as np

def apply_rotation(L, T):
    return np.dot(L, T.T)

def shift_to_visible_area(matrix, shift_x, shift_y):
    return matrix + np.array([shift_x, shift_y])



pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("num 7")

white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

L = np.array([
    [3, -1],
    [4, 1],
    [2, 1]
]) * 100 

T = np.array([
    [0, 1],
    [-1, 0]
])

rotated_L = apply_rotation(L, T)

visible_shift = (300, 450)
shifted_L = shift_to_visible_area(L, *visible_shift)
shifted_rotated_L = shift_to_visible_area(rotated_L, *visible_shift)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(white)

    pygame.draw.polygon(screen, red, shifted_L, 3)

    pygame.draw.polygon(screen, blue, shifted_rotated_L, 3)

    pygame.display.flip()

pygame.quit()
