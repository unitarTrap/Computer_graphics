import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("num 9")

triangle = np.array([[5, 1], [5, 2], [3, 2]]) * 25
T = np.array([[2, 0], [0, 2]])  

scaled_triangle = (T @ triangle.T).T + np.array([300, 300])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.polygon(screen, (255, 0, 0), triangle + [300, 300], 3)  
    pygame.draw.polygon(screen, (0, 0, 255), scaled_triangle, 3)

    pygame.display.flip()

pygame.quit()