import pygame

def draw_line_low(
    surface: pygame.Surface,
    start: tuple[int, int],
    end: tuple[int, int],
    color: pygame.Color,
):
    x0, y0 = start
    x1, y1 = end

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    m = (y1 - y0) / (x1 - x0)
    b = y0 - m * x0
    for x in range(x0, x1 + 1):
        y = m * x + b
        surface.set_at((x, int(y)), color)

def draw_line_high(
    surface: pygame.Surface,
    start: tuple[int, int],
    end: tuple[int, int],
    color: pygame.Color,
):
    x0, y0 = start
    x1, y1 = end

    if y0 > y1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    m = (y1 - y0) / (x1 - x0)
    b = y0 - m * x0

    for y in range(y0, y1 + 1):
        x = (y - b) / m
        surface.set_at((int(x), y), color)

def draw_line_vertical(
    surface: pygame.Surface,
    start: tuple[int, int],
    end: tuple[int, int],
    color: pygame.Color,
):
    x0, y0 = start
    x1, y1 = end
    for y in range(y0, y1 + 1):
        surface.set_at((x0, y), color)

def draw_line(
    surface: pygame.Surface,
    start: tuple[int, int],
    end: tuple[int, int],
    color: pygame.Color,
):
    x0, y0 = start
    x1, y1 = end
    if x0 == x1:
        draw_line_vertical(surface, start, end, color)
    else:
        m = (y1 - y0) / (x1 - x0)
        if abs(m) <= 1:
            draw_line_low(surface, start, end, color)
        else:
            draw_line_high(surface, start, end, color)

def draw_triangle(
    surface: pygame.Surface,
    point_a: tuple[int, int],
    point_b: tuple[int, int],
    point_c: tuple[int, int],
    color: pygame.Color,
):
    draw_line(surface, point_a, point_b, color)
    draw_line(surface, point_a, point_c, color)
    draw_line(surface, point_b, point_c, color)

# Scan-line fill of a triangle.
# This function is fragile; it needs special cases for vertical or horizontal edges.
def fill_triangle(
    surface: pygame.Surface,
    point_a: tuple[int, int],
    point_b: tuple[int, int],
    point_c: tuple[int, int],
    color: pygame.Color,
):
    # First, sort the vertices by y coordinate
    if point_a[1] > point_b[1]:
        point_a, point_b = point_b, point_a
    if point_a[1] > point_c[1]:
        point_a, point_c = point_c, point_a
    if point_b[1] > point_c[1]:
        point_b, point_c = point_c, point_b
    # Now, A has the smallest y coordinate, and C has the largest.

    # Draw the upper segment of the triangle: the lines connecting edge AB with part of AC.

    # First find the inverse slope of AB and AC.
    im_AB = (point_b[0] - point_a[0]) / (point_b[1] - point_a[1])
    im_AC = (point_c[0] - point_a[0]) / (point_c[1] - point_a[1])

    # We will "walk" down the lines by repeatedly adding the inverse slope
    # to an x-coordinate accumulator for each line segment, starting at point A.
    x_AB = x_AC = point_a[0]

    surface.set_at(point_a, color)
    # For the vertical range of edge AB:
    for y in range(point_a[1] + 1, point_b[1]):
        # Compute the x coordinate for edge AB and AC by moving their current coordinate
        # by their inverse slope.
        x_AB += im_AB
        x_AC += im_AC

        # Connect the two points with a horizontal line.
        # Make sure the range goes in increasing order from left to right.
        if x_AB > x_AC:
            l, r = x_AC, x_AB
        else:
            l, r = x_AB, x_AC

        for x in range(int(l), int(r) + 1):
            surface.set_at((x, y), color)

    # Repeat the process, for the lower segment: edge BC and the remainder of edge AC.
    im_BC = (point_c[0] - point_b[0]) / (point_c[1] - point_b[1])
    x_BC = point_b[0]
    for y in range(point_b[1], point_c[1]):
        x_BC += im_BC
        x_AC += im_AC

        if x_AC > x_BC:
            l, r = x_BC, x_AC
        else:
            l, r = x_AC, x_BC

        for x in range(int(l), int(r) + 1):
            surface.set_at((x, y), color)

# Bounding-box fill of a triangle. Test every pixel in the bounding box to see
# if it is inside the triangle, and set the color if so.
def fill_triangle2( surface: pygame.Surface,
    point_a: tuple[int, int],
    point_b: tuple[int, int],
    point_c: tuple[int, int],
    color: pygame.Color,
):
    # Determine the bounding box around the three vertices.
    min_x = point_a[0]
    min_y = point_a[1]
    max_x = point_a[0]
    max_y = point_a[1]
    for p in [point_b, point_c]:
        if p[0] < min_x:
            min_x = p[0]
        elif p[0] > max_x:
            max_x = p[0]
        if p[1] < min_y:
            min_y = p[1]
        elif p[1] > max_y:
            max_y = p[1]
    # the box has an upper-left of (min_x, miny), and a lower-right of (max_x, max_y).
    
    # Iterate through each pixel in the bounding box, and color if it is inside the triangle.
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if inside_bary2((x, y), point_a, point_b, point_c):
                screen.set_at((x, y), color)
                
def inside_bary2(p, a, b, c):
    s1 = c[1] - a[1] # Cy - Ay
    s2 = c[0] - a[0] # Cx - Ax
    s3 = b[1] - a[1] # By - Ay
    s4 = p[1] - a[1] # Py - Ay
    w1 = (a[0] * s1 + s4 * s2 - p[0] * s1) / (s3 * s2 - (b[0] - a[0]) * s1)
    w2 = (s4 - w1 * s3) / s1
    return w1 >= 0 and w2 >= 0 and w1 + w2 <= 1

if __name__ == "__main__":
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
        draw_triangle(screen, (200, 200), (250, 300), (90, 310), white)
        fill_triangle(screen, (500, 200), (550, 300), (390, 310), white)
        
        # The triangle below will crash with a division-by-zero exception.
        fill_triangle(screen, (500, 500), (650, 600), (700, 500), white)
        pygame.display.update()
    pygame.quit()
