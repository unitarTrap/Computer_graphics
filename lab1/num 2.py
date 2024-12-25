import pygame

pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("num 2")

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(white)

    pygame.draw.circle(screen, red, (400, 300), 100, 5)


    pygame.draw.line(screen, green, (100, 100), (700, 100), 5)
    pygame.draw.line(screen, blue, (100, 500), (700, 500), 5)

    pygame.draw.rect(screen, yellow, (300, 200, 200, 100), 3)

    pygame.display.flip()
