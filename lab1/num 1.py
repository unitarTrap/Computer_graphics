import pygame
import numpy  as np

pygame.init()
window_size = (500, 500)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("num 1")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

transformation_matrix = [
    [1, 3],
    [4, 1]
]

x = int(input("Введите координату x: "))
y = int(input("Введите координату y: "))

point = np.array([x, y])  
T = np.array(transformation_matrix)  

transformed_point = T @ point

print(f"Начальные координаты: ({point})")
print(f"Новые координаты: ({transformed_point})")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(white)

    pygame.draw.circle(screen, red, point, 5)
    pygame.draw.circle(screen, blue, transformed_point, 5)

    pygame.display.flip()

