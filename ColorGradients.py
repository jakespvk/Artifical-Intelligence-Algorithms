import pygame

def draw_line_low(surface, start: tuple[int, int], end: tuple[int, int], slope, intercept, start_color, end_color):
    #def draw_line(start, end):

        x0, y0 = start
        x1, y1 = end
        m = slope
        b = intercept

        for x in range(x0, x1 + 1):

            y = m * x + b

            surface.set_at((x, int(y)), pygame.Color(int(start_color.r + ((end_color.r - start_color.r) * (x / (x1 + 1)))), int(start_color.g + ((end_color.g - start_color.g) * (x / (x1 + 1)))), int(start_color.b + ((end_color.b - start_color.b) * (x / (x1 + 1))))))

def draw_line_high(surface, start: tuple[int, int], end: tuple[int, int], slope, intercept, start_color, end_color):
    #def draw_line(start, end):
    

        x0, y0 = start
        x1, y1 = end
        m = slope
        b = intercept

        for y in range(y0, y1 + 1):

            #y = m * x + b
            x = (y - b) / m

            #surface.set_at((int(x), y), start_color, end_color)
            surface.set_at((int(x), y), pygame.Color(int(start_color.r + ((end_color.r - start_color.r) * (x / (x1 + 1)))), int(start_color.g + ((end_color.g - start_color.g) * (x / (x1 + 1)))), int(start_color.b + ((end_color.b - start_color.b) * (x / (x1 + 1))))))

def draw_line(surface, start: tuple[int, int], end: tuple[int, int], start_color, end_color):

    x0, y0 = start
    x1, y1 = end
    if x0 > x1:
        x0, x1 = x1, x0
    if y0 > y1:
        y0, y1 = y1, y0
    m = (y1 - y0) / (x1 - x0) 
    b = y0 - (m * x0)
    if (abs(m) > 1):
        draw_line_high(screen, (x0, y0), (x1, y1), m, b, start_color, end_color)
    else:
        draw_line_low(screen, (x0, y0), (x1, y1), m, b, start_color, end_color)

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
        
        draw_line(screen, (0, 40), (500, 500), red, green)
        pygame.display.update()
    pygame.quit()

