import pygame

pygame.init()

screen_width = 1000

screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))

done = False

white = pygame.Color(255, 255, 255)

while not done:

  for event in pygame.event.get():

    if event.type == pygame.QUIT:

      done = True

  screen.set_at((100, 100), white)

  pygame.display.update()

pygame.quit()
