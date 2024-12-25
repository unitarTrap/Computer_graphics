import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("num 3")

line_start = np.array([10, 111])
line_end = np.array([40, 200])

T = np.array([[1, 3], [4, 1]])

transformed_start = T @ line_start
transformed_end = T @ line_end

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.line(screen, (0, 0, 255), line_start, line_end, 3)
    pygame.draw.line(screen, (0, 255, 0), transformed_start, transformed_end, 3)
    pygame.display.flip()

pygame.quit()