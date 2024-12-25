import pygame
import numpy as np

def apply_reflection(L, T):
    return np.dot(L, T.T)

def shift_to_visible_area(matrix, shift_x, shift_y):
    return matrix + np.array([shift_x, shift_y])


pygame.init()

window_size = (900, 800)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("num 8")

white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

L = np.array([
    [8, 1],
    [7, 3],
    [6, 2]
]) * 100  

T = np.array([
    [0, 1],
    [1, 0]
])

reflected_L = apply_reflection(L, T)

visible_shift = (-100, -100)
shifted_L = shift_to_visible_area(L, *visible_shift)
shifted_reflected_L = shift_to_visible_area(reflected_L, *visible_shift)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(white)

    pygame.draw.polygon(screen, red, shifted_L, 3)

    pygame.draw.polygon(screen, blue, shifted_reflected_L, 3)

    pygame.display.flip()

pygame.quit()
