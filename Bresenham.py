import pygame

def draw_line_low(surface, start: tuple[int, int], end: tuple[int, int], color):
    x0, y0 = start
    x1, y1 = end
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy
    D = (2 * dy) - dx
    y = y0

    for x in range(x1 - x0):
        surface.set_at((x, y), color)
        if D > 0:
            y = y + yi
            D = D + (2 * (dy - dx))
        else:
            D = D + 2*dy

def draw_line_high(surface, start: tuple[int, int], end: tuple[int, int], color):
    x0, y0 = start
    x1, y1 = end
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    D = (2 * dx) - dy
    x = x0

    for y in range(y1 - y0):
        surface.set_at((x, y), color)
        if D > 0:
            x = x + xi
            D = D + (2 * (dx - dy))
        else:
            D = D + 2*dx

def draw_line(surface, start: tuple[int, int], end: tuple[int, int], color):

    x0, y0 = start
    x1, y1 = end
    if x0 > x1:
        x0, x1 = x1, x0
    if y0 > y1:
        y0, y1 = y1, y0
    m = (y1 - y0) / (x1 - x0) 
    b = y0 - (m * x0)
    if (abs(m) > 1):
        draw_line_high(screen, (x0, y0), (x1, y1), color)
    else:
        draw_line_low(screen, (x0, y0), (x1, y1), color)

if __name__ == "__main__":
    
    pygame.init()

    screen_width = 1000

    screen_height = 800

    screen = pygame.display.set_mode((screen_width,

                                  screen_height))

    done = False

    red = pygame.Color(255, 0, 0)

    green = pygame.Color(0, 255, 0)

    while not done:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                done = True
        
        draw_line(screen, (0, 40), (500, 500), green)
        draw_line(screen, (300, 150), (350, 350), red)
        pygame.display.update()
    pygame.quit()

