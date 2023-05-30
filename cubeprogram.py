import pygame
from pygame.locals import *
from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Mesh3D import *

if __name__ == "__main__":
    pygame.init()
    screen_width = 800
    screen_height = 800
    screen = pygame.display.set_mode(
        (screen_width, screen_height),
        DOUBLEBUF | OPENGL,
    )
    pygame.display.set_caption("OpenGL in Python")

    # Set up OpenGL
    glEnable(GL_DEPTH_TEST)

    # Initialize the projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #glOrtho(-1, 1, -1, 1, -1, 1)
    gluPerspective(30, screen_width / screen_height, 0.1, 100)

    # Prepare to place geometry elements
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0, 0, 4, 0, 0, 0, 0, 1, 0)

    # Define the scene.
    mesh = Mesh3D.cube()
    m2 = Mesh3D.cube()

    # Loop
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Clear the screen to all black.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw the mesh.
        mesh.draw()

        pygame.display.flip()
    pygame.quit()
