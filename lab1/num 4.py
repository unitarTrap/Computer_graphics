import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("num 4")

L = np.array([[0, 100], [200, 300]])  
T = np.array([[1, 2], [3, 1]])        

transformed_L = (T @ L.T).T

mid_L = (L[0] + L[1]) / 2
mid_transformed_L = (transformed_L[0] + transformed_L[1]) / 2

scale = 0.1
scaled_L = L * scale
scaled_transformed_L = transformed_L * scale
scaled_mid_L = mid_L * scale
scaled_mid_transformed_L = mid_transformed_L * scale

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.line(screen, (255, 0, 0), scaled_L[0], scaled_L[1], 2)
    pygame.draw.circle(screen, (255, 0, 0), scaled_mid_L.astype(int), 5)

    pygame.draw.line(screen, (0, 255, 0), scaled_transformed_L[0], scaled_transformed_L[1], 2)
    pygame.draw.circle(screen, (0, 255, 0), scaled_mid_transformed_L.astype(int), 5)

    pygame.draw.line(screen, (0, 0, 0), scaled_mid_L, scaled_mid_transformed_L, 1)

    pygame.display.flip()

pygame.quit()