import pygame
from pygame.locals import *
from OpenGL.GL import *

if __name__ == "__main__":
    pygame.init()
    screen_width = 800
    screen_height = 800
    screen = pygame.display.set_mode(
        (screen_width, screen_height),
        # Take note of the next line, which informs pygame
        # that OpenGL will do the drawing.
        DOUBLEBUF | OPENGL,
    )
    pygame.display.set_caption("OpenGL in Python")

    done = False
    red = pygame.Color(255, 0, 0)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Clear the screen to all black.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # A pair of glBegin() and glEnd() function calls enable us to draw a shape in 3 dimensions.
        # glBegin takes a drawing "mode", of which there are many.
        # The simplest is GL_LINE, for drawing lines.
        glBegin(GL_LINES)
        # Set the color of the line.
        glColor3ub(
            red.r, red.g, red.b
        )  # The "3ub" means we are passing 3 unsigned bytes [0~255].

        # We plot the endpoints of the line individually, and OpenGL will connect them.
        glVertex3f(0.5, 0.5, 0)  # These are the x, y, z coordinates of the vertex.
        glVertex3f(0, 0, 0)  # The "3f" means "3 float parameters".

        # In GL_LINES, every pair of glVertex calls forms one line.
        # A second pair, then, will draw a second line.

        # We don't really *need* Color objects if we know the literal values.
        glColor3ub(0, 255, 0)
        glVertex3f(-0.5, -0.5, 0)
        glVertex3f(0, -0.5, 0)
        glEnd()  # End this set of GL_LINES.

        # By default, OpenGL's camera shows the space of 2x2x2 cube centered at the origin.
        # The positive x-axis goes to the right.
        # The positive y-axis goes up.
        # The positive z-axis goes out of the screen.
        # All vertices then must be between -1 and 1 in each of its coordinates to be viewable.

        # To draw triangles, we use mode GL_LINE_LOOP, which connects the vertices with lines
        # in the order you define them, and then connects the last back to the first.
        glBegin(GL_LINE_LOOP)
        glColor3ub(0, 0, 255)
        glVertex3f(-0.7, 0.9, 0)
        # Giving a different color to each vertex causes OpenGL to do a linear gradient along the line.
        glColor3ub(0, 255, 0)
        glVertex3f(-0.7, 0.1, 0)
        glColor3ub(255, 0, 0)
        glVertex3f(-0.1, 0.1, 0)
        glEnd()

        # To fill a triangle, we use GL_TRIANGLES.

        # This list of vertices is just to demonstrate "glVertex3fv" below. 
        # You could certainly pass these vertex coordinates directly to each glVertex3f call.
        tri_vertices = [(0.7, -0.9, 0), (0.7, -0.1, 0), (0.1, -0.1, 0)]
        glBegin(GL_TRIANGLES)
        # If a gl function ends in "v", it means the parameter is a tuple/vector containing the expected values.
        glVertex3fv(tri_vertices[0])
        glVertex3fv(tri_vertices[1])
        glVertex3fv(tri_vertices[2])
        glEnd()

        pygame.display.flip()
    pygame.quit()
