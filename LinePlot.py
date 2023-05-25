import pygame

def draw_line_low(surface, start: tuple[int, int], end: tuple[int, int], slope, intercept, color):
    #def draw_line(start, end):

        x0, y0 = start
        x1, y1 = end
        m = slope
        b = intercept

        for x in range(x0, x1 + 1):

            y = m * x + b

            surface.set_at((x, int(y)), color)

def draw_line_high(surface, start: tuple[int, int], end: tuple[int, int], slope, intercept, color):
    #def draw_line(start, end):
    

        x0, y0 = start
        x1, y1 = end
        m = slope
        b = intercept

        for y in range(y0, y1 + 1):

            #y = m * x + b
            x = (y - b) / m

            surface.set_at((int(x), y), color)

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
        draw_line_high(screen, (x0, y0), (x1, y1), m, b, color)
    else:
        draw_line_low(screen, (x0, y0), (x1, y1), m, b, color)

if __name__ == "__main__":
    
    pygame.init()

    screen_width = 1000

    screen_height = 800

    screen = pygame.display.set_mode((screen_width,

                                  screen_height))

    done = False

    white = pygame.Color(255, 255, 255)

    green = pygame.Color(0, 255, 0)

    while not done:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                done = True
        draw_line(screen, (0, 40), (500, 500), white)
        pygame.display.update()
    pygame.quit()

