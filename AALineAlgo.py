import pygame

def fpart(x):
    return x - int(x)

def rfpart(x): 
    return 1 - fpart(x)

def draw_line_aa(surface, start: tuple[int, int], end: tuple[int, int], color):
    
    x0, y0 = start
    x1, y1 = end

    steep = abs(y1 - y0) > abs(x1 - x0)

    if steep:
        x0, y0 = x1, y1
    if x0 > x1:
        swap(x0, x1)
        swap(y0, y1)

    dx = x1 - x0
    dy = y1 - y0

    if dx == 0.0:
        gradient = 1.0
    else:
        gradient = dy / dx

    xend = round(x0)
    yend = y0 + gradient * (xend - x0)
    xgap = rfpart(x0 + 0.5)
    xpxl1 = xend
    ypxl1 = int(yend)

    if steep:
        surface.set_at((ypxl1, xpxl1), 
                       pygame.Color(
                           (int(color.r * (rfpart(yend) * xgap))),
                           (int(color.g * (rfpart(yend) * xgap))),
                           (int(color.b * (rfpart(yend) * xgap)))
                           ))
        surface.set_at((ypxl1 + 1, xpxl1), 
                       pygame.Color(
                           (int(color.r * (fpart(yend) * xgap))),
                           (int(color.g * (fpart(yend) * xgap))),
                           (int(color.b * (fpart(yend) * xgap)))
                           ))
    else:
        surface.set_at((xpxl1, ypxl1), 
                       pygame.Color(
                           (color.r * (rfpart(yend) * xgap)),
                           (color.g * (rfpart(yend) * xgap)),
                           (color.b * (rfpart(yend) * xgap))
                           ))
        surface.set_at((xpxl1, ypxl1 + 1), 
                       pygame.Color(
                           (color.r * (fpart(yend) * xgap)),
                           (color.g * (fpart(yend) * xgap)),
                           (color.b * (fpart(yend) * xgap))
                           ))
    intery = yend + gradient

    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = fpart(x1 + 0.5)
    xpxl2 = xend
    ypxl2 = int(yend)

    if steep:
        surface.set_at((ypxl2, xpxl2),
                      pygame.Color(
                          (int(color.r * (rfpart(yend) * xgap))),
                          (int(color.g * (rfpart(yend) * xgap))),
                          (int(color.b * (rfpart(yend) * xgap)))
                          ))
        surface.set_at((ypxl2 + 1, xpxl2),
                       pygame.Color(
                           (int(color.r * (fpart(yend) * xgap))),
                           (int(color.g * (fpart(yend) * xgap))),
                           (int(color.b * (fpart(yend) * xgap)))
                           ))
    else:
        surface.set_at((xpxl2, ypxl2),
                      pygame.Color(
                          (int(color.r * (rfpart(yend) * xgap))),
                          (int(color.g * (rfpart(yend) * xgap))),
                          (int(color.b * (rfpart(yend) * xgap)))
                          ))
        surface.set_at((xpxl2, ypxl2 + 1),
                       pygame.Color(
                           (int(color.r * (fpart(yend) * xgap))),
                           (int(color.g * (fpart(yend) * xgap))),
                           (int(color.b * (fpart(yend) * xgap)))
                           ))

    if steep:
        for x in range(xpxl1 + 1, xpxl2):
            surface.set_at((x, int(intery)), rfpart(intery))
            surface.set_at((x, int(intery) + 1), fpart(inery))
            intery = intery + gradient

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

    screen = pygame.display.set_mode((screen_width, screen_height))

    done = False

    white = pygame.Color(255, 255, 255)

    green = pygame.Color(0, 255, 0)

    while not done:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                done = True
        draw_line(screen, (0, 40), (500, 500), white)
        draw_line_aa(screen, (0, 90), (500, 550), white)
        pygame.display.update()
    pygame.quit()

