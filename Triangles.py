import pygame

def draw_line_low(surface, start: tuple[int, int], end: tuple[int, int], slope, intercept, color):
    #def draw_line(start, end):

    x0, y0 = start
    x1, y1 = end
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    m = slope
    b = intercept

    for x in range(x0, x1 + 1):

        y = m * x + b

        surface.set_at((x, int(y)), color)

def draw_line_high(surface, start: tuple[int, int], end: tuple[int, int], slope, intercept, color):
    #def draw_line(start, end):
    

    x0, y0 = start
    x1, y1 = end

    if y0 > y1:
        y0, y1 = y1, y0
        x0, x1 = x1, x0
    m = slope
    b = intercept

    for y in range(y0, y1 + 1):

        #y = m * x + b
        x = (y - b) / m

        surface.set_at((int(x), y), color)

def draw_line(surface, start: tuple[int, int], end: tuple[int, int], color):

    x0, y0 = start
    x1, y1 = end
    m = (y1 - y0) / (x1 - x0) 
    b = y0 - (m * x0)
    if (abs(m) > 1):
        draw_line_high(screen, (x0, y0), (x1, y1), m, b, color)
    else:
        draw_line_low(screen, (x0, y0), (x1, y1), m, b, color)

def draw_triangle(surface, v1: tuple[int, int], v2: tuple[int, int], v3: tuple[int, int], color, tall_color):
    # int max_y_delta = max(abs(v1[1] - v3[1]), max(abs(v1[1] - v2[1]), abs(v2[1] - v3[1])))
    v1v2 = abs(v1[1] - v2[1])
    v2v3 = abs(v2[1] - v3[1])
    v3v1 = abs(v3[1] - v1[1])
    if (v1v2 > v2v3) & (v1v2 > v3v1):
        draw_line(surface, v1, v2, tall_color)
        draw_line(surface, v2, v3, color)
        draw_line(surface, v3, v1, color)
    elif (v2v3 > v3v1) & (v2v3 > v1v2):
        draw_line(surface, v2, v3, tall_color)
        draw_line(surface, v1, v2, color)
        draw_line(surface, v3, v1, color)
    else:
        draw_line(surface, v1, v3, tall_color)
        draw_line(surface, v1, v2, color)
        draw_line(surface, v2, v3, color)

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
        draw_triangle(screen, (100, 100), (200, 200), (250, 150), green, red)
        pygame.display.update()
    pygame.quit()

