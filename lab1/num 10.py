import pygame
import math

pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("num 10")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

a = 50
b = 200
center_x = window_size[0] // 2
center_y = window_size[1] // 2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(white)

    theta = 0
    points = []
    while theta < 2 * math.pi * 10: 
        r = b + 2 * a * math.cos(theta)
        x = r * math.cos(theta) + center_x
        y = r * math.sin(theta) + center_y
        points.append((int(x), int(y)))
        theta += 0.01

    if len(points) > 1:
        pygame.draw.lines(screen, red, False, points, 2)

    pygame.display.flip()
