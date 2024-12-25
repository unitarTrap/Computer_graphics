import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("num 5")

lines = np.array([[50, 100], [250, 200], [50, 200], [250, 300]])
T = np.array([[1, 2], [3, 1]])  

transformed_lines = np.dot(T, lines.T).T

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.line(screen, (0, 255, 0), lines[0], lines[1], 3)
    pygame.draw.line(screen, (0, 255, 0), lines[2], lines[3], 3)
    pygame.draw.line(screen, (0, 0, 255), transformed_lines[0], transformed_lines[1], 3)
    pygame.draw.line(screen, (0, 0, 255), transformed_lines[2], transformed_lines[3], 3)

    pygame.display.flip()

pygame.quit()