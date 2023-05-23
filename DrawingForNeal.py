import pygame

pygame.init()

screen_width = 1000
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
done = False
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
blue = pygame.Color(0, 0, 255)

while not done:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

    pygame.draw.rect(screen, white, pygame.Rect(100, 100, 100, 100))
    pygame.draw.circle(screen, red, (350, 150), 50)
    pygame.draw.polygon(screen, blue, [(550, 100), (500, 200), (600, 200)])
    pygame.display.update()

pygame.quit()
